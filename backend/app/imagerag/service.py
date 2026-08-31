import base64
import json
import mimetypes

from openai import OpenAI

from app.config import OPENAI_API_KEY
from app.imagerag.schema import ImageRagResponse, ImageRagResult
from app.storage.s3 import (
    get_image_url,
    list_categories,
    list_images,
)


client = OpenAI(
    api_key=OPENAI_API_KEY
)


def get_food_categories() -> list[str]:
    try:
        return list_categories()

    except Exception as error:
        raise RuntimeError(
            f"S3 음식 카테고리 조회 실패: {error}"
        ) from error


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

    extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    }

    try:
        s3_images = list_images(
            food_name
        )

    except Exception as error:
        raise RuntimeError(
            f"S3 참고 이미지 목록 조회 실패: {error}"
        ) from error

    valid_images = [
        image
        for image in s3_images
        if (
            "." + image["filename"]
            .rsplit(".", 1)[-1]
            .lower()
        ) in extensions
    ]

    valid_images.sort(
        key=lambda image: image["key"]
    )

    reference_images = []

    for image in valid_images[:limit]:
        try:
            url = get_image_url(
                image["relative_key"],
                expires_in=3600,
            )

            reference_images.append(
                url
            )

        except Exception as error:
            raise RuntimeError(
                f"S3 Presigned URL 생성 실패 "
                f"({image['relative_key']}): {error}"
            ) from error

    return reference_images


def find_matching_folder(
    predicted_food: str,
    categories: list[str],
) -> str | None:

    predicted_food = predicted_food.strip()

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
        category_normalized = (
            category
            .replace(" ", "")
            .lower()
        )

        if (
            category_normalized in normalized
            or normalized in category_normalized
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
            "S3 images/ 경로에 음식 카테고리가 없습니다."
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

    result_text = (
        response.output_text
        .strip()
    )

    if result_text.startswith("```"):
        result_text = (
            result_text
            .replace(
                "```json",
                "",
            )
            .replace(
                "```",
                "",
            )
            .strip()
        )

    try:
        result_json = json.loads(
            result_text
        )

    except json.JSONDecodeError as error:
        raise RuntimeError(
            f"OpenAI 응답 JSON 파싱 실패: {result_text}"
        ) from error

    predicted_food = str(
        result_json.get(
            "food_name",
            "",
        )
    ).strip()

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

    confidence = result_json.get(
        "confidence",
        0.0,
    )

    try:
        confidence = float(
            confidence
        )

    except (
        TypeError,
        ValueError,
    ):
        confidence = 0.0

    confidence = max(
        0.0,
        min(
            1.0,
            confidence,
        ),
    )

    return ImageRagResponse(
        success=True,
        result=ImageRagResult(
            food_name=predicted_food,
            confidence=confidence,
            description=str(
                result_json.get(
                    "description",
                    "",
                )
            ),
            matched_folder=matched_folder,
            reference_images=reference_images,
        ),
    )