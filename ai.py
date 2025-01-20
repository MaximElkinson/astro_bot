import requests

def ai_request(name):
    prompt = {
    "modelUri": "gpt://Token/yandexgpt-lite",
    "completionOptions": {
    "stream": False,
    "temperature": 0.6,
    "maxTokens": "5000"
    },
      "messages": [
    {
      "role": "system",
      "text": "Дай общие советы для знака задиака"
    },
    {
      "role": "user",
      "text": f"{name}"
    }
    ]
    }


    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "API"
              }


    response = requests.post(url, headers=headers, json=prompt)
    result = response.text
    return result