import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
IMAGE_DIR = BASE_DIR / "images"

load_dotenv(ENV_PATH)


OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)

AWS_REGION = os.getenv(
    "AWS_REGION",
    "ap-northeast-2",
)

S3_BUCKET_NAME = os.getenv(
    "S3_BUCKET_NAME",
    "aame-s3-pipeline",
)

S3_IMAGE_PREFIX = os.getenv(
    "S3_IMAGE_PREFIX",
    "images/",
)


if not OPENAI_API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY가 설정되어 있지 않습니다."
    )

if not S3_BUCKET_NAME:
    raise RuntimeError(
        "S3_BUCKET_NAME이 설정되어 있지 않습니다."
    )