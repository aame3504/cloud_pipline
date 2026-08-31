from pydantic import BaseModel


class ImageRagResult(BaseModel):
    food_name: str
    confidence: float
    description: str
    matched_folder: str | None
    reference_images: list[str]


class ImageRagResponse(BaseModel):
    success: bool
    result: ImageRagResult