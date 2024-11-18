import os
from langchain import OpenAI

def get_llm():
    return OpenAI(temperature=0.7, api_key=os.getenv('OPENAI_API_KEY'))
