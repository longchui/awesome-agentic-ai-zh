import sys, json
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(api_key="sk-dbc3562701fb44239beefa60af196a0f",base_url="https://api.deepseek.com")

SYSTEM_PROMPTS = {
    "可爱老师": "你是温柔可爱的老师，回答问题要俏皮可爱，卡哇伊",
    "专业人士": "你是专业的金融交易员，将用最严谨客观的话回答",
    "JSON 机器": "你只回 JSON。schema: {\"answer\": string, \"confidence\": float}",
}

USER_MSG = "请帮我解释什么是租赁合约"

outputs = {}
for label, system in SYSTEM_PROMPTS.items():
    r = client.chat.completions.create(
        model="deepseek-v4-flash",
        max_tokens=200,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": USER_MSG},
        ]
    )
    outputs[label] =r.choices[0].message.content
    print(f"\n---[{label}]---")
    print(outputs[label])