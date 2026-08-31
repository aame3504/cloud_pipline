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

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379/0",
)

JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY"
)

JWT_ALGORITHM = "HS256"

JWT_EXPIRE_MINUTES = 60 * 24


if not OPENAI_API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY가 설정되어 있지 않습니다."
    )

if not S3_BUCKET_NAME:
    raise RuntimeError(
        "S3_BUCKET_NAME이 설정되어 있지 않습니다."
    )

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL이 설정되어 있지 않습니다."
    )

if not JWT_SECRET_KEY:
    raise RuntimeError(
        "JWT_SECRET_KEY가 설정되어 있지 않습니다."
    )