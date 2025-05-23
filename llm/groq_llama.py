import os
import requests

from dotenv import load_dotenv
load_dotenv(dotenv_path=".groq_env")


GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
# TEMPORARY ONLY FOR TESTING
GROQ_API_KEY = os.getenv("GROQ_API_KEY")



def get_llama_response(prompt, system_prompt=None, model="llama3-70b-8192"):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.3,
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()  
        return response.json()['choices'][0]['message']['content'].strip()
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"