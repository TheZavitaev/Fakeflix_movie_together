from uuid import UUID

from fastapi import HTTPException, Request
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt
from starlette.status import HTTP_401_UNAUTHORIZED


class JwtUserVerify():

    async def __call__(self, request: Request, user_id: UUID):
        token = JwtUserVerify._get_jwt_token(request)   # noqa: 437
        try:
            jwt_user_id = UUID(token['user_id'])
        except KeyError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if user_id != jwt_user_id:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Invalid user_id",
                headers={"WWW-Authenticate": "Bearer"},
            )

    @staticmethod
    def _get_jwt_token(request: Request) -> dict:
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return jwt.decode(param, 'dummy', options={"verify_signature": False})
