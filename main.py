from agents import Agent, Runner, function_tool
from connection import config
import requests

@function_tool
def get_product(query):
    try:
        response = requests.get("https://hackathon-apis.vercel.app/api/products")
        response.raise_for_status()
        products = response.json()

        query_lower = query.lower()
        exact, substrings, related = [], [], []

        for item in products:
            name_lower = item["name"].lower()
            if query_lower == name_lower:
                exact.append(item)
            elif query_lower in name_lower:
                substrings.append(item)
            elif all(word in name_lower for word in query_lower.split()):
                related.append(item)

        if exact:
            return {"status": "ok", "match_type": "exact", "products": exact}
        if substrings:
            return {"status": "ok", "match_type": "substring", "products": substrings}
        if related:
            return {"status": "ok", "match_type": "related", "products": related}

        return {"status": "none", "message": "No matching product found."}

    except requests.RequestException as e:
        return {"status": "error", "message": f"Request failed: {e}"}
    
shopping_agent = Agent(
    name="Shopping Assistant Agent",
    instructions="""
        You are a professional and friendly shopping assistant. Your role is to help users
        find product information, such as prices, names, and details.

        Your primary tool is `get_product`. Always use this tool to search the product catalog.

        ### How to respond:
        1. **Exact Match Found**
        - Present the product clearly with its name, price, and key details.
        - Keep the tone polite and helpful.

        2. **Partial or Related Matches**
        - If there’s no exact match, share the closest result(s).
        - Make it clear to the user that it’s a partial/related match (e.g., “I couldn’t find an exact match for X, but here’s something close…”).
        - If multiple matches are available, list the top few options.

        3. **No Matches**
        - Politely inform the user that the product was not found.
        - Encourage them to try a different name or spelling.

        4. **Errors**
        - If the tool returns an error, explain it simply (e.g., “Sorry, I’m having trouble connecting to the catalog right now.”).

        ### Style Guidelines:
        - Be concise, clear, and professional.
        - Never guess or invent product details.
        - Do not repeat raw JSON directly; instead, present results in a readable way.
        - Use a friendly, supportive tone as if assisting a customer in a real store.
        """,
    tools=[get_product]
)
def main():
    result = Runner.run_sync(
        shopping_agent, "What is the price for Zen table?", run_config=config
    )

    print(result.final_output)


if __name__ == "__main__":
    main()
