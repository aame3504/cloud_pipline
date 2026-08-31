import base64
import json
import mimetypes

from openai import OpenAI

from app.config import IMAGE_DIR, OPENAI_API_KEY
from app.imagerag.schema import ImageRagResponse, ImageRagResult


client = OpenAI(
    api_key=OPENAI_API_KEY
)


def get_food_categories() -> list[str]:
    if not IMAGE_DIR.exists():
        return []

    return sorted(
        folder.name
        for folder in IMAGE_DIR.iterdir()
        if folder.is_dir()
    )


def encode_image(
    image_bytes: bytes,
) -> str:
    return base64.b64encode(
        image_bytes
    ).decode("utf-8")


def find_reference_images(
    food_name: str,
    limit: int = 5,
) -> list[str]:

    folder = IMAGE_DIR / food_name

    if not folder.exists():
        return []

    extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    }

    images = [
        file
        for file in folder.iterdir()
        if (
            file.is_file()
            and file.suffix.lower() in extensions
        )
    ]

    images.sort()

    return [
        f"/images/{food_name}/{file.name}"
        for file in images[:limit]
    ]


def find_matching_folder(
    predicted_food: str,
    categories: list[str],
) -> str | None:

    if predicted_food in categories:
        return predicted_food

    normalized = (
        predicted_food
        .replace(" ", "")
        .lower()
    )

    for category in categories:
        category_normalized = (
            category
            .replace(" ", "")
            .lower()
        )

        if normalized == category_normalized:
            return category

    for category in categories:
        if (
            category in predicted_food
            or predicted_food in category
        ):
            return category

    return None


def analyze_image(
    image_bytes: bytes,
    filename: str,
) -> ImageRagResponse:

    categories = get_food_categories()

    if not categories:
        raise RuntimeError(
            f"음식 이미지 폴더가 없습니다: {IMAGE_DIR}"
        )

    mime_type, _ = mimetypes.guess_type(
        filename
    )

    if mime_type is None:
        mime_type = "image/jpeg"

    encoded_image = encode_image(
        image_bytes
    )

    category_text = ", ".join(
        categories
    )

    prompt = f"""
업로드된 음식 이미지를 분석하세요.

사용 가능한 음식 카테고리는 다음과 같습니다.

{category_text}

반드시 위 목록 중 가장 가까운 음식 하나를 선택하세요.

다음 JSON 형식으로만 응답하세요.

{{
    "food_name": "음식명",
    "confidence": 0.95,
    "description": "판단 이유"
}}

confidence는 0.0 ~ 1.0 사이 숫자입니다.
food_name은 반드시 제공된 카테고리 중 하나여야 합니다.
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": prompt,
                    },
                    {
                        "type": "input_image",
                        "image_url": (
                            f"data:{mime_type};base64,"
                            f"{encoded_image}"
                        ),
                    },
                ],
            }
        ],
    )

    result_text = response.output_text.strip()

    if result_text.startswith("```"):
        result_text = (
            result_text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

    try:
        result_json = json.loads(
            result_text
        )

    except json.JSONDecodeError:
        raise RuntimeError(
            f"OpenAI 응답 JSON 파싱 실패: {result_text}"
        )

    predicted_food = result_json.get(
        "food_name",
        "",
    )

    matched_folder = find_matching_folder(
        predicted_food,
        categories,
    )

    reference_images = []

    if matched_folder:
        reference_images = find_reference_images(
            matched_folder,
            limit=5,
        )

    return ImageRagResponse(
        success=True,
        result=ImageRagResult(
            food_name=predicted_food,
            confidence=float(
                result_json.get(
                    "confidence",
                    0.0,
                )
            ),
            description=result_json.get(
                "description",
                "",
            ),
            matched_folder=matched_folder,
            reference_images=reference_images,
        ),
    )