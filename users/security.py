from passlib.context import CryptContext

from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from decouple import config

from typing import Optional, Dict

import jwt

import time


JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def token_response(token: str)->dict:
    return{
        "accessToken": token
        # refresh_token
    }


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hash: str) -> str:
    return pwd_context.verify(password, hash)


def sign_jwt(user_email: str, user_account_type: str)-> Dict[str, str]:
    payload = {
        "user_email": user_email,
        "expires": time.time() + 6000,
        "user_account_type": user_account_type
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decode_jwt(jwt_token: str, permission_type: str):
    try:
        decoded_token = jwt.decode(jwt_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if decoded_token["user_account_type"] != permission_type:
            return False, "Permission denied!"
        if decoded_token["expires"] >= time.time():
            return True, decoded_token
        else:
            return False, "Token is expired!"
    except:
        return True, {}


class JWTBearer(HTTPBearer):
    def __init__(self, permission_type: str = "standart", auto_error: bool = True):
        self.permission_type = permission_type
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid auth scheme!")
            status, detail = self.verify_jwt(credentials.credentials)
            if not status:
                raise HTTPException(status_code=403, detail=detail)
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid auth code!")

    def verify_jwt(self, jwt_token: str):
        status, detail = decode_jwt(jwt_token, self.permission_type)
        return status, detail
