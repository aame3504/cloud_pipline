from datetime import datetime
from datetime import timedelta
from datetime import timezone
from uuid import uuid4

import bcrypt
import jwt
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.model import User
from app.config import JWT_ALGORITHM
from app.config import JWT_EXPIRE_MINUTES
from app.config import JWT_SECRET_KEY
from app.database.redis import redis_client


def hash_password(
    password: str,
) -> str:
    password_bytes = password.encode(
        "utf-8"
    )

    hashed_password = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt(),
    )

    return hashed_password.decode(
        "utf-8"
    )


def verify_password(
    password: str,
    password_hash: str,
) -> bool:
    return bcrypt.checkpw(
        password.encode(
            "utf-8"
        ),
        password_hash.encode(
            "utf-8"
        ),
    )


def get_user_by_id(
    db: Session,
    user_id: int,
) -> User | None:
    statement = (
        select(User)
        .where(
            User.id == user_id
        )
    )

    return (
        db.execute(
            statement
        )
        .scalar_one_or_none()
    )


def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:
    statement = (
        select(User)
        .where(
            User.email
            == email
        )
    )

    return (
        db.execute(
            statement
        )
        .scalar_one_or_none()
    )


def get_user_by_username(
    db: Session,
    username: str,
) -> User | None:
    statement = (
        select(User)
        .where(
            User.username
            == username
        )
    )

    return (
        db.execute(
            statement
        )
        .scalar_one_or_none()
    )


def create_user(
    db: Session,
    email: str,
    username: str,
    password: str,
) -> User:
    user = User(
        email=
            email.lower().strip(),
        username=
            username.strip(),
        password_hash=
            hash_password(
                password
            ),
        is_active=True,
    )

    db.add(
        user
    )

    db.commit()

    db.refresh(
        user
    )

    return user


def create_login_session(
    user: User,
) -> str:
    jti = str(
        uuid4()
    )

    now = datetime.now(
        timezone.utc
    )

    expires_at = (
        now
        + timedelta(
            minutes=
                JWT_EXPIRE_MINUTES
        )
    )

    payload = {
        "sub":
            str(
                user.id
            ),
        "email":
            user.email,
        "username":
            user.username,
        "jti":
            jti,
        "iat":
            now,
        "exp":
            expires_at,
    }

    token = jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=
            JWT_ALGORITHM,
    )

    redis_key = (
        f"session:{jti}"
    )

    redis_client.hset(
        redis_key,
        mapping={
            "user_id":
                str(
                    user.id
                ),
            "email":
                user.email,
            "username":
                user.username,
        },
    )

    redis_client.expire(
        redis_key,
        JWT_EXPIRE_MINUTES
        * 60,
    )

    return token


def decode_access_token(
    token: str,
) -> dict:
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[
                JWT_ALGORITHM
            ],
        )

    except InvalidTokenError as error:
        raise ValueError(
            "유효하지 않은 인증 토큰입니다."
        ) from error

    return payload


def validate_login_session(
    token: str,
) -> dict:
    payload = decode_access_token(
        token
    )

    jti = payload.get(
        "jti"
    )

    user_id = payload.get(
        "sub"
    )

    if not jti:
        raise ValueError(
            "세션 ID가 없는 토큰입니다."
        )

    if not user_id:
        raise ValueError(
            "사용자 ID가 없는 토큰입니다."
        )

    redis_key = (
        f"session:{jti}"
    )

    session = (
        redis_client.hgetall(
            redis_key
        )
    )

    if not session:
        raise ValueError(
            "로그인 세션이 만료되었거나 로그아웃되었습니다."
        )

    return payload


def delete_login_session(
    token: str,
) -> bool:
    payload = decode_access_token(
        token
    )

    jti = payload.get(
        "jti"
    )

    if not jti:
        return False

    redis_key = (
        f"session:{jti}"
    )

    deleted_count = (
        redis_client.delete(
            redis_key
        )
    )

    return (
        deleted_count > 0
    )