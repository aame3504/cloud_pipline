from fastapi import APIRouter
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile

from app.imagerag.schema import ImageRagResponse
from app.imagerag.service import analyze_image


router = APIRouter(
    prefix="/api/imagerag",
    tags=["Image RAG"],
)


@router.post(
    "/search",
    response_model=ImageRagResponse,
)
async def image_rag_search(
    image: UploadFile = File(...),
):

    if not image.content_type:
        raise HTTPException(
            status_code=400,
            detail="이미지 파일을 업로드해주세요.",
        )

    if not image.content_type.startswith(
        "image/"
    ):
        raise HTTPException(
            status_code=400,
            detail="이미지만 업로드할 수 있습니다.",
        )

    try:
        image_bytes = await image.read()

        if not image_bytes:
            raise HTTPException(
                status_code=400,
                detail="빈 이미지 파일입니다.",
            )

        return analyze_image(
            image_bytes=image_bytes,
            filename=image.filename or "image.jpg",
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )