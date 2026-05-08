import os
import requests

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv(
    "GROQ_API_KEY"
)

def ask_groq(question):

    url = (
        "https://api.groq.com/openai/v1/chat/completions"
    )

    headers = {

        "Authorization":
            f"Bearer {API_KEY}",

        "Content-Type":
            "application/json"
    }

    payload = {

        "model":
            "llama3-70b-8192",

        "messages": [
            {
                "role": "user",
                "content": question
            }
        ]
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    data = response.json()

    return data["choices"][0]["message"]["content"]