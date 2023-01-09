import os

import openai
from dotenv import load_dotenv

load_dotenv()
# Set the API key for the OpenAI API
openai.api_key = os.getenv("CHATGPT_API_KEY")


def generate_gpt_response(prompt):
    return openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        temperature=0.5,
    ).text
