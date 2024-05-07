from datetime import datetime, timezone, timedelta
from graphql import GraphQLError
import jwt
from app.settings.config import SECRET_KEY, ALGORITHM, TOKEN_EXPIRATION_TIME_IN_MINUTES
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from app.db.database import get_async_session
from app.db.models import User
from functools import wraps
from sqlalchemy import select

async def generate_token(email):
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRATION_TIME_IN_MINUTES)

    payload = {
        "sub": email,
        "exp": expiration_time
    }

    token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
    return token


async def hash_password(password):
    ph = PasswordHasher()
    return ph.hash(password)


async def verify_password(password_hash, password):
    ph = PasswordHasher()
    try:
        ph.verify(password_hash, password)
    except VerifyMismatchError:
        raise GraphQLError("Invalid password")


async def get_authenticated_user(context):
    request_object = context.get('request')
    auth_header = request_object.headers.get('Authorization')
    
    if not auth_header:
        raise GraphQLError("Missing authentication token")
    
    token = auth_header.split(" ")

    if token[0] != 'Bearer' or len(token) != 2:
        raise GraphQLError("Missing authentication token")
    
    token = token[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if datetime.now(timezone.utc) > datetime.fromtimestamp(payload['exp'], tz=timezone.utc):
            raise GraphQLError("Token has expired")

        session = await get_async_session()
        result = await session.execute(select(User).where(User.email == payload.get('sub')))
        user = result.scalars().first()
        await session.close()
        if not user:
            raise GraphQLError("Could not authenticate user")
        return user
    except jwt.exceptions.PyJWTError:
        raise GraphQLError("Invalid authentication token")


def admin_user(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        info = args[1]
        user = await get_authenticated_user(info.context)
        if user.role != 'admin':
            raise GraphQLError("You are not authorized to perform this action")
        return await func(*args, **kwargs)
    return wrapper


def auth_user(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        info = args[1]
        await get_authenticated_user(info.context)
        return await func(*args, **kwargs)
    return wrapper


def auth_user_same_as(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        info = args[1]
        user = await get_authenticated_user(info.context)
        user_id = kwargs.get("user_id")
        if user.id != user_id:
            raise GraphQLError("You are not authorized to perform this action")
        return await func(*args, **kwargs)
    return wrapper
