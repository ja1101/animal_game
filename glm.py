import os
import requests
import json

def call_gpt(p, messages=None):
  if messages is None:
    messages = [{"role": "user", "content": p}]
  elif isinstance(messages, str):
    messages = [{"role": "user", "content": messages}]
  response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": "Bearer " + os.environ["OPENROUTER_API_KEY"],
    "Content-Type": "application/json",
  },
  data=json.dumps({
    "model": "z-ai/glm-5.3-flash",
    "messages": messages,
    "reasoning": {"enabled": True}
  })
  )
  response = response.json()
  #print(response)
  return response['choices'][0]['message']