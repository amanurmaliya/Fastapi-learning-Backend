from passlib.context import CryptContext

import jwt
import os
from datetime import datetime, timedelta, UTC

from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "secret123")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def generate_token(data: dict, expires_minutes: int = 60):
    to_encode = data.copy()
    
    expire = datetime.now(UTC) + timedelta(minutes = expires_minutes)
    
    to_encode.update({"exp":expire})
    return jwt.encode( to_encode, JWT_SECRET, algorithm="HS256")
