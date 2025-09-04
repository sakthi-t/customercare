import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_llm():
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env")
    return ChatOpenAI(model=model, temperature=0.3, api_key=api_key)

def call_llm(prompt: str, model: str = "gpt-4o-mini") -> str:
    """Call OpenAI with a prompt and return text."""
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a careful, safety-aware customer support SQL assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    return resp.choices[0].message.content
