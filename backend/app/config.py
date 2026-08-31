import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = BASE_DIR / ".env"

IMAGE_DIR = BASE_DIR / "images"


load_dotenv(ENV_PATH)


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


if not OPENAI_API_KEY:
    raise RuntimeError(
        f"OPENAI_API_KEY가 설정되어 있지 않습니다. "
        f".env 파일을 확인하세요: {ENV_PATH}"
    )