import requests

def ai_request(name):
    prompt = {
    "modelUri": "gpt://b1gkrk5s55un9vdqthbj/yandexgpt-lite",
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
        "Authorization": "Api-Key AQVNxK5J_xB5_bAxUvPiHCbJdIpTPmhs9rl7LF3O"
              }


    response = requests.post(url, headers=headers, json=prompt)
    result = response.text
    return result

















# aje4lp4vu43pvmo32knj
# AQVNxK5J_xB5_bAxUvPiHCbJdIpTPmhs9rl7LF3O
# b1gkrk5s55un9vdqthbj