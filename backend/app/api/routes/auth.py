from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException, status
from jose import jwt

from app.api.deps import CrudUserDepends
from app.core import security
from app.schemas import JwtToken, UserCreate, UserTelegramData

router = APIRouter(prefix="/auth", tags=["auth"])


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, "LcH6ouNfUvAhn4AdmjkwkvfzbUHn3ViVHqjt8P1umPc", algorithm="HS256"
    )
    return encoded_jwt


@router.post("", status_code=200)
async def auth_user(
    user_telegram_data: UserTelegramData,
    user_crud: CrudUserDepends,
) -> JwtToken:
    """
    Регистрация пользователя в системе.
    Для регистрация отправляются данные о его тг аккаунте и хэш для проверки валидности.
    Данные от аккаунта хешируются с ключом бота и сравниваются с хэшом для проверки.
    Переданные данные в json конвертируются в строку с добавлением \n.

    Parameters:
        user_telegram_data: UserTelegramData - данные пользователя от телеграм-аккаунта.
        user_crud:

    Returns:
        {"token": "jwt"}

    Errors:
        400 - проблемы валидации pyndatic
        401 - данные не прошли проверку
    """
    user_telegram_data_hash = user_telegram_data.hash
    data_check_list = []

    user_data_dict = user_telegram_data.model_dump()
    for key, value in sorted(user_data_dict.items()):  # Sort required!
        if key != "hash" and value is not None:
            data_check_list.append(f"{key}={value}")

    data_check_string = "\n".join(data_check_list)
    is_valid = security.verify_user_data(data_check_string, user_telegram_data_hash)

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Данные неверны",
        )

    user = await user_crud.get(id=user_telegram_data.id)

    if not user:
        await user_crud.create(
            UserCreate(
                id=user_telegram_data.id,
                username=user_telegram_data.username,
                name=user_telegram_data.first_name,
                photo_url=user_telegram_data.photo_url,
            ),
        )

    access_token_expires = timedelta(days=1)
    access_token = create_access_token(
        data={"sub": str(user_telegram_data.id)}, expires_delta=access_token_expires
    )
    return JwtToken(token=access_token)
