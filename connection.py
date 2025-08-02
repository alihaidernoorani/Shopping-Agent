from agents import OpenAIChatCompletionsModel, AsyncOpenAI
from agents.run import RunConfig
import os
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv(key="GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set. "
                     "Please ensure it's defined in your .env file or system environment variables.")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash", 
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client, 
    tracing_disabled=True          
)