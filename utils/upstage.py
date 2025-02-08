import requests
from openai import OpenAI # openai==1.52.2


def execute_ocr(api_key, file):

    #filename = file_path
    
    url = "https://api.upstage.ai/v1/document-ai/ocr"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    #files = {"document": open(filename, "rb")}
    files = {"document": file}
    response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        content = response.json().get("text", "")
        confidence = response.json().get("confidence", 0)
        return content, confidence
    else:
        print(response.json())
        return "Upstage OCR API 요청에 실패했습니다."


'''def get_answer_from_solar(api_key, content, prompt, temperature=0.7):
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.upstage.ai/v1/solar"
    )

    response = client.chat.completions.create(
        model="solar-pro",
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": content
            }
        ],
        stream=False,
        temperature=temperature
    )

    return response.choices[0].message.content'''

def get_answer_from_solar(api_key, content, prompt, temperature=0.7):
    url = "https://api.upstage.ai/v1/solar/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "solar-pro",
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": content}
        ],
        "temperature": temperature
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Error code: {response.status_code} - {response.json()}")
