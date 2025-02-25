import openai
import base64
import requests

with open("api_key.txt", "r") as file:
    api_key = file.read().strip()


def fit_prompt_to_api_calls(text_prompt):
    contents = [{"type": "text"}]
    contents[0]["text"] = text_prompt

    format = [{"role": "user"}]
    format[0]["content"] = contents
    return format


def gen_AI_call(call):

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    payload = {
        "model": "gpt-4o-mini",
        "messages": call,
        "max_tokens": 600,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )
    try:
        return response.json()["choices"][0]["message"]["content"]
    except:
        print("Maybe you should try again..!")
