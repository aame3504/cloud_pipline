from fastapi import APIRouter
from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.auth.schema import LoginRequest
from app.auth.schema import LoginResponse
from app.auth.schema import MessageResponse
from app.auth.schema import SignupRequest
from app.auth.schema import UserResponse
from app.auth.service import create_login_session
from app.auth.service import create_user
from app.auth.service import delete_login_session
from app.auth.service import get_user_by_email
from app.auth.service import get_user_by_id
from app.auth.service import get_user_by_username
from app.auth.service import validate_login_session
from app.auth.service import verify_password
from app.database.database import get_db


router = APIRouter(
    prefix="/api/auth",
    tags=[
        "Auth"
    ],
)


def get_bearer_token(
    authorization:
        str | None
        = Header(
            default=None
        ),
) -> str:
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail=
                "인증 토큰이 없습니다.",
        )

    parts = (
        authorization
        .split(
            " ",
            1,
        )
    )

    if (
        len(parts) != 2
        or parts[0].lower()
        != "bearer"
    ):
        raise HTTPException(
            status_code=401,
            detail=
                "Bearer 토큰 형식이 올바르지 않습니다.",
        )

    return parts[1]


@router.post(
    "/signup",
    response_model=
        UserResponse,
    status_code=201,
)
def signup(
    request:
        SignupRequest,
    db:
        Session
        = Depends(
            get_db
        ),
):
    email = (
        request.email
        .lower()
        .strip()
    )

    username = (
        request.username
        .strip()
    )

    existing_email = (
        get_user_by_email(
            db,
            email,
        )
    )

    if existing_email:
        raise HTTPException(
            status_code=409,
            detail=
                "이미 가입된 이메일입니다.",
        )

    existing_username = (
        get_user_by_username(
            db,
            username,
        )
    )

    if existing_username:
        raise HTTPException(
            status_code=409,
            detail=
                "이미 사용 중인 사용자명입니다.",
        )

    return create_user(
        db=
            db,
        email=
            email,
        username=
            username,
        password=
            request.password,
    )


@router.post(
    "/login",
    response_model=
        LoginResponse,
)
def login(
    request:
        LoginRequest,
    db:
        Session
        = Depends(
            get_db
        ),
):
    email = (
        request.email
        .lower()
        .strip()
    )

    user = (
        get_user_by_email(
            db,
            email,
        )
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail=
                "이메일 또는 비밀번호가 올바르지 않습니다.",
        )

    if not verify_password(
        request.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=401,
            detail=
                "이메일 또는 비밀번호가 올바르지 않습니다.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail=
                "비활성화된 계정입니다.",
        )

    try:
        token = (
            create_login_session(
                user
            )
        )

    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail=
                "Redis 로그인 세션 생성에 실패했습니다.",
        ) from error

    return LoginResponse(
        access_token=
            token,
        token_type=
            "bearer",
        user=
            UserResponse.model_validate(
                user
            ),
    )


@router.get(
    "/me",
    response_model=
        UserResponse,
)
def get_me(
    token:
        str
        = Depends(
            get_bearer_token
        ),
    db:
        Session
        = Depends(
            get_db
        ),
):
    try:
        payload = (
            validate_login_session(
                token
            )
        )

    except ValueError as error:
        raise HTTPException(
            status_code=401,
            detail=
                str(error),
        ) from error

    user_id = payload.get(
        "sub"
    )

    try:
        user_id = int(
            user_id
        )

    except (
        TypeError,
        ValueError,
    ) as error:
        raise HTTPException(
            status_code=401,
            detail=
                "유효하지 않은 사용자 정보입니다.",
        ) from error

    user = (
        get_user_by_id(
            db,
            user_id,
        )
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail=
                "사용자를 찾을 수 없습니다.",
        )

    return user


@router.post(
    "/logout",
    response_model=
        MessageResponse,
)
def logout(
    token:
        str
        = Depends(
            get_bearer_token
        ),
):
    try:
        delete_login_session(
            token
        )

    except ValueError as error:
        raise HTTPException(
            status_code=401,
            detail=
                str(error),
        ) from error

    return MessageResponse(
        success=True,
        message=
            "로그아웃되었습니다.",
    )