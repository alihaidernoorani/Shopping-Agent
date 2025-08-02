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

        # 1. Exact match
        for item in products:
            if query_lower == item["name"].lower():
                return item

        # 2. Substring match
        for item in products:
            if query_lower in item["name"].lower():
                return {
                    "note": f"No exact match found. Showing partial match: '{item['name']}'",
                    **item
                }

        # 3. Token match (all query words appear somewhere in name)
        query_words = query_lower.split()
        for item in products:
            name_words = item["name"].lower()
            if all(word in name_words for word in query_words):
                return {
                    "note": f"No exact or substring match. Showing related match: '{item['name']}'",
                    **item
                }

        return {"message": "No matching product found."}

    except requests.RequestException as e:
        return {"error": f"Request failed: {e}"}
    
agent = Agent(
    name="Assistant agent",
    instructions="""
        You are a helpful and honest assistant trained to help users search for product prices.

        Your primary task is to use the `get_product` tool to find and return product information. If the user's query does not exactly match a product name, attempt to find close or partial matches. You may suggest the closest result if the exact one is not available.

        Guidelines:
        - Always prefer using the `get_product` tool to fetch product details.
        - If no exact match is found, look for similar or partially matching product names.
        - If still no relevant match is available, politely inform the user that the product could not be found.
        - Do NOT fabricate or guess product details under any circumstances.
        - Maintain a professional, friendly tone in all responses.
        """,
    tools=[get_product]
)

result = Runner.run_sync(
    agent, "Cutlery", run_config=config
)

def main():
    print(result.final_output)


if __name__ == "__main__":
    main()
