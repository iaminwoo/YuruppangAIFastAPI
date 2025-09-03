import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')


async def generate_by_gemini(video_info: dict, url: str, categories: str) -> str:
    full_prompt = f"""
    Video Info: {video_info}
    Url: {url}
    Categories: {categories}

    이 영상의 Video Info를 통해서 레시피에 필요한 재료를 정리해줘.

    결과는 반드시 JSON 형태로만 출력해 줘.
    JSON 항목은 아래를 참고해줘.
    {{
        "name": "레시피의 이름",
        "description": "레시피에 대한 설명 + 예상해서 기입한 재료 + 가로줄 + 채널명과 url",
        "outputQuantity": 정수,
        "categoryId": 정수 (Categories에서 선택, 비슷한게 없으면 0으로),
        "parts": [
            {{
                "partName": "파트 이름",
                "ingredients": [
                    {{"ingredientName": "재료 이름", "quantity": 정수, "unit": "g|ml|개"}}
                ]
            }}
        ]
    }}
    - quantity가 2-3처럼 범위일 경우 평균값을 정수로 사용해주고 unit은 반드시 g, ml, 개 중 하나로 맞춰줘.
    - 만약 '한 꼬집', '적당량' 같이 정확한 수치를 알 수 없는 경우, 최대한 생각해서 알려주고 애매하면 기본값인 0g으로 해줘.
    - 그리고 description에 명시되지 않아서 예상해서 적은 재료의 이름들을 적어줘.
    - description 은 한문장마다 줄바꿈을 해주고 적당히 문단도 나눠줘.
    - 채널에 대해서 쓸때는, (출처 "채널명" : "url") 이렇게 적어줘.
    """

    response = model.generate_content(full_prompt)

    text = response.text

    if text.startswith("```json"):
        text = text[7:]  # 앞쪽 제거
    if text.endswith("```\n"):
        text = text[:-5]  # 뒤쪽 제거

    text = text.strip()  # 혹시 남은 공백 제거

    return json.loads(text)


def validate_ingredients(data):
    for part in data.get("parts", []):
        for ingredient in part.get("ingredients", []):
            name = ingredient.get("ingredientName")
            quantity = ingredient.get("quantity")
            unit = ingredient.get("unit")

            # quantity 숫자 확인
            if not isinstance(quantity, (int, float)):
                print(f"[경고] '{name}'의 수량이 숫자가 아닙니다: {quantity}")
                ingredient["unit"] = "g"
                ingredient["quantity"] = 0

            # unit 검증
            if unit not in ["g", "ml", "개"]:
                print(f"[주의] '{name}'의 단위가 표준 단위가 아닙니다: '{unit}'")
                ingredient["unit"] = "g"
                ingredient["quantity"] = 0