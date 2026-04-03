import requests
import json
import base64 
lol = "MMZHG5DCGNEXIZDKIV2E43KFPFGXUTJQJV5GG6SZNJBGYTKUJE2VUR2FGNHVIWTMLJKE2MK2NJAXQWL2MN4VUV2ZPJHUOUTILFLVKM2NGJKTIT2EMMZU6RCSNJHVIUTKLJCFM3KNNVMTKTRSIU2VUV22NVHUCPJ5"
strr = base64.b64decode('0Y8g0YDQtdGI0LDRjiDQt9Cw0LTQsNGH0YMg0L3QsCDQsNC90LDQu9C40Lcg0LTQsNC90L3Ri9GFINGH0LXRgNC10LcgcGFuZGFzLg==').decode()
def ai(prompt: str) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {base64.b64decode(base64.b32decode(lol)).decode()}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "qwen/qwen3-32b", # qwen/qwen3-32b , deepseek/deepseek-v3.2, google/gemini-2.5-flash-lite
        "messages": [{"role": "user", "content": prompt}],
    }

    response = requests.post(url, headers=headers, json=payload, timeout=60)
    data = response.json()

    print("status:", response.status_code)

    if response.status_code != 200:
        raise RuntimeError(data)

    return data["choices"][0]["message"]["content"]

print(ai('напиши только 1 больше ничего'))
