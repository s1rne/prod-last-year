from datetime import UTC, datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi import security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

from config import JWT_ALGORITHM, JWT_EXPIRATION, RANDOM_SECRET
from db import tools
from utils.utils import hash_password

security = HTTPBearer()


class JWT:
    @staticmethod
    def encode(login: str, id: str, sub: str) -> str:
        current_time = datetime.now(UTC)
        expiration = current_time + timedelta(hours=JWT_EXPIRATION)

        token_payload = {
            "login": login,
            "id": id,
            "exp": expiration.timestamp(),
            "iat": current_time.timestamp(),
            "sub": sub,
        }

        token = jwt.encode(
            token_payload,
            RANDOM_SECRET,
            algorithm=JWT_ALGORITHM
        )
        return token

    @staticmethod
    async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )
        try:
            token = credentials.credentials
            if not token:
                raise credentials_exception

            payload = jwt.decode(
                token,
                RANDOM_SECRET,
                algorithms=[JWT_ALGORITHM],
                options={
                    "verify_signature": True,
                    "verify_exp": True,
                    "verify_iat": True,
                    "require": ["exp", "iat", "login", "id", "sub"]
                }
            )
            exp_timestamp = payload.get("exp")
            if not exp_timestamp:
                raise credentials_exception

            iat_timestamp = payload.get("iat")
            if not iat_timestamp:
                raise credentials_exception

            if datetime.fromtimestamp(payload['exp']) < datetime.now():
                raise credentials_exception

            user = await tools.get_user_by_id(payload['id'])
            if not user:
                raise credentials_exception

            rel = payload.get("sub")
            if not rel:
                raise credentials_exception

            if rel != hash_password(user["passwordHash"]):
                raise credentials_exception

            return user
        except jwt.InvalidTokenError as e:
            raise credentials_exception
        except Exception as e:
            raise credentials_exception


jwt_tools = JWT
