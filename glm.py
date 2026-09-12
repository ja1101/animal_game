import os
import requests
import json

def call_gpt(p):
  response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": "Bearer " + os.environ["OPENROUTER_API_KEY"],
    "Content-Type": "application/json",
  },
  data=json.dumps({
    "model": "z-ai/glm-5.3-flash",
    "messages": [
        {
          "role": "user",
          "content": p
        }
      ],
    "reasoning": {"enabled": True}
  })
  )
  response = response.json()
  return response['choices'][0]['message']