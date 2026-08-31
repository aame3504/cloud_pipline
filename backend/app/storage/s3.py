from io import BytesIO
from pathlib import Path
from typing import BinaryIO
from uuid import uuid4

import boto3
from botocore.exceptions import BotoCoreError
from botocore.exceptions import ClientError

from app.config import AWS_REGION
from app.config import S3_BUCKET_NAME
from app.config import S3_IMAGE_PREFIX


s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
)


def _normalize_prefix() -> str:
    prefix = S3_IMAGE_PREFIX.strip("/")

    if not prefix:
        return ""

    return f"{prefix}/"


def _normalize_category(category: str) -> str:
    category = category.strip().strip("/")

    if not category:
        raise ValueError("음식명(category)이 비어 있습니다.")

    return category


def _normalize_relative_key(relative_key: str) -> str:
    relative_key = relative_key.strip().lstrip("/")

    if not relative_key:
        raise ValueError("S3 상대 경로가 비어 있습니다.")

    return relative_key


def _build_key(relative_key: str) -> str:
    prefix = _normalize_prefix()
    relative_key = _normalize_relative_key(relative_key)

    return f"{prefix}{relative_key}"


def _build_category_key(
    category: str,
    filename: str,
) -> str:
    category = _normalize_category(category)

    safe_filename = Path(filename).name

    if not safe_filename:
        raise ValueError("파일 이름이 비어 있습니다.")

    relative_key = f"{category}/{safe_filename}"

    return _build_key(relative_key)


def _build_unique_category_key(
    category: str,
    filename: str,
) -> str:
    original = Path(filename)

    suffix = original.suffix.lower()
    stem = original.stem

    unique_filename = f"{stem}_{uuid4().hex}{suffix}"

    return _build_category_key(
        category=category,
        filename=unique_filename,
    )


def upload_image(
    category: str,
    file_data: bytes | BinaryIO,
    filename: str,
    content_type: str = "application/octet-stream",
    use_unique_name: bool = True,
) -> dict:
    if use_unique_name:
        key = _build_unique_category_key(
            category=category,
            filename=filename,
        )
    else:
        key = _build_category_key(
            category=category,
            filename=filename,
        )

    try:
        if isinstance(file_data, bytes):
            body = BytesIO(file_data)
        else:
            body = file_data

        s3_client.upload_fileobj(
            body,
            S3_BUCKET_NAME,
            key,
            ExtraArgs={
                "ContentType": content_type,
            },
        )

        return {
            "bucket": S3_BUCKET_NAME,
            "key": key,
            "category": _normalize_category(category),
            "filename": Path(key).name,
            "content_type": content_type,
        }

    except (ClientError, BotoCoreError) as error:
        raise RuntimeError(
            f"S3 이미지 업로드 실패: {error}"
        ) from error


def list_images(
    category: str | None = None,
) -> list[dict]:
    base_prefix = _normalize_prefix()

    if category:
        category = _normalize_category(category)
        prefix = f"{base_prefix}{category}/"
    else:
        prefix = base_prefix

    images = []

    try:
        paginator = s3_client.get_paginator(
            "list_objects_v2"
        )

        pages = paginator.paginate(
            Bucket=S3_BUCKET_NAME,
            Prefix=prefix,
        )

        for page in pages:
            contents = page.get(
                "Contents",
                [],
            )

            for item in contents:
                key = item["Key"]

                if key.endswith("/"):
                    continue

                relative_key = key

                if base_prefix and key.startswith(base_prefix):
                    relative_key = key[len(base_prefix):]

                parts = relative_key.split("/")

                detected_category = (
                    parts[0].strip()
                    if len(parts) >= 2
                    else None
                )

                images.append(
                    {
                        "key": key,
                        "relative_key": relative_key,
                        "category": detected_category,
                        "filename": Path(key).name,
                        "size": item["Size"],
                        "last_modified": item["LastModified"],
                        "etag": item.get(
                            "ETag",
                            "",
                        ).strip('"'),
                    }
                )

        return images

    except (ClientError, BotoCoreError) as error:
        raise RuntimeError(
            f"S3 이미지 목록 조회 실패: {error}"
        ) from error


def list_categories() -> list[str]:
    prefix = _normalize_prefix()

    categories = set()

    try:
        paginator = s3_client.get_paginator(
            "list_objects_v2"
        )

        pages = paginator.paginate(
            Bucket=S3_BUCKET_NAME,
            Prefix=prefix,
            Delimiter="/",
        )

        for page in pages:
            for item in page.get(
                "CommonPrefixes",
                [],
            ):
                category_prefix = item.get(
                    "Prefix",
                    "",
                )

                if prefix and category_prefix.startswith(prefix):
                    category = category_prefix[len(prefix):]
                else:
                    category = category_prefix

                category = category.strip("/").strip()

                if category:
                    categories.add(category)

        return sorted(categories)

    except (ClientError, BotoCoreError) as error:
        raise RuntimeError(
            f"S3 카테고리 목록 조회 실패: {error}"
        ) from error


def image_exists(
    relative_key: str,
) -> bool:
    key = _build_key(relative_key)

    try:
        s3_client.head_object(
            Bucket=S3_BUCKET_NAME,
            Key=key,
        )

        return True

    except ClientError as error:
        error_code = error.response.get(
            "Error",
            {},
        ).get(
            "Code"
        )

        if error_code in (
            "404",
            "NoSuchKey",
            "NotFound",
        ):
            return False

        raise RuntimeError(
            f"S3 이미지 존재 여부 확인 실패: {error}"
        ) from error


def get_image(
    relative_key: str,
) -> bytes:
    key = _build_key(relative_key)

    try:
        response = s3_client.get_object(
            Bucket=S3_BUCKET_NAME,
            Key=key,
        )

        return response["Body"].read()

    except (ClientError, BotoCoreError) as error:
        raise RuntimeError(
            f"S3 이미지 조회 실패: {error}"
        ) from error


def get_image_metadata(
    relative_key: str,
) -> dict:
    key = _build_key(relative_key)

    try:
        response = s3_client.head_object(
            Bucket=S3_BUCKET_NAME,
            Key=key,
        )

        return {
            "bucket": S3_BUCKET_NAME,
            "key": key,
            "relative_key": _normalize_relative_key(
                relative_key
            ),
            "content_length": response.get(
                "ContentLength"
            ),
            "content_type": response.get(
                "ContentType"
            ),
            "last_modified": response.get(
                "LastModified"
            ),
            "etag": response.get(
                "ETag",
                "",
            ).strip('"'),
        }

    except (ClientError, BotoCoreError) as error:
        raise RuntimeError(
            f"S3 이미지 메타데이터 조회 실패: {error}"
        ) from error


def get_image_url(
    relative_key: str,
    expires_in: int = 3600,
) -> str:
    key = _build_key(relative_key)

    try:
        return s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": S3_BUCKET_NAME,
                "Key": key,
            },
            ExpiresIn=expires_in,
        )

    except (ClientError, BotoCoreError) as error:
        raise RuntimeError(
            f"S3 이미지 URL 생성 실패: {error}"
        ) from error


def download_image(
    relative_key: str,
    destination: str | Path,
) -> Path:
    key = _build_key(relative_key)

    destination_path = Path(destination)

    if destination_path.exists() and destination_path.is_dir():
        destination_path = (
            destination_path
            / Path(relative_key).name
        )

    destination_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    try:
        s3_client.download_file(
            S3_BUCKET_NAME,
            key,
            str(destination_path),
        )

        return destination_path

    except (ClientError, BotoCoreError) as error:
        raise RuntimeError(
            f"S3 이미지 다운로드 실패: {error}"
        ) from error


def update_image(
    relative_key: str,
    file_data: bytes | BinaryIO,
    content_type: str = "application/octet-stream",
) -> dict:
    key = _build_key(relative_key)

    try:
        if isinstance(file_data, bytes):
            body = BytesIO(file_data)
        else:
            body = file_data

        s3_client.upload_fileobj(
            body,
            S3_BUCKET_NAME,
            key,
            ExtraArgs={
                "ContentType": content_type,
            },
        )

        return {
            "bucket": S3_BUCKET_NAME,
            "key": key,
            "relative_key": _normalize_relative_key(
                relative_key
            ),
            "updated": True,
        }

    except (ClientError, BotoCoreError) as error:
        raise RuntimeError(
            f"S3 이미지 수정 실패: {error}"
        ) from error


def delete_image(
    relative_key: str,
) -> dict:
    key = _build_key(relative_key)

    try:
        s3_client.delete_object(
            Bucket=S3_BUCKET_NAME,
            Key=key,
        )

        return {
            "bucket": S3_BUCKET_NAME,
            "key": key,
            "relative_key": _normalize_relative_key(
                relative_key
            ),
            "deleted": True,
        }

    except (ClientError, BotoCoreError) as error:
        raise RuntimeError(
            f"S3 이미지 삭제 실패: {error}"
        ) from error