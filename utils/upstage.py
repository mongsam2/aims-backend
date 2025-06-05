import os
import requests
from django.conf import settings

UPSTAGE_API_URL = "https://api.upstage.ai/v1/chat/completions"
UPSTAGE_MODEL = "solar-pro"


def call_upstage_llm(prompt_filename: str, user_text: str) -> str:
    """
    prompt 파일명과 사용자 입력을 받아 LLM에 요청하고 응답을 리턴.
    """
    prompt_path = os.path.join(settings.BASE_DIR, "prompts", prompt_filename)
    
    with open(prompt_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    headers = {
        "Authorization": f"Bearer {settings.UPSTAGE_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": UPSTAGE_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }

    response = requests.post(UPSTAGE_API_URL, json=body, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Upstage LLM API 오류: {response.status_code} {response.text}")
    
    return response.json()["choices"][0]["message"]["content"]
