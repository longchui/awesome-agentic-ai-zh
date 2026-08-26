import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="eplace")

from openai import OpenAI
client = OpenAI(api_key="sk-dbc3562701fb44239beefa60af196a0f",base_url="https://api.deepseek.com")
response = client.responses.create(
    model="deepseek-v4-flash",
    max_output_tokens=100,
    prompt="用一句话介绍自己",
)

text = response.text
print("回应:", text)
print("usage:", response.usage)



