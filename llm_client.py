# llm_client.py
import os
from dotenv import load_dotenv
from groq import Groq

# Load API key from .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("Please set GROQ_API_KEY in your .env file")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

class LLMClient:
    def __init__(self, model_name="llama-3.3-70b-versatile"):
        self.model_name = model_name
        self.client = client

    def generate(self, prompt: str, max_tokens: int = 512):
        """
        Generates text using Groq LLM.
        Returns the output text.
        """
        response = self.client.generate(
            model=self.model_name,
            prompt=prompt,
            max_tokens=max_tokens
        )
        return response.text
