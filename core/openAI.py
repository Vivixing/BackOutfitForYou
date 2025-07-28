from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))