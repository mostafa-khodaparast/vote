from fastapi.security import HTTPBearer
from fastapi import Request, status
from fastapi import HTTPException
from fastapi.security.http import HTTPAuthorizationCredentials

from .utils import decode_token


class AccessTokenBearer(HTTPBearer):

    def __init__(self, auto_error=False):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict | None:
        creds: HTTPAuthorizationCredentials | None = await super().__call__(request)

        if creds is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Authorization header missing or invalid"
            )

        token = creds.credentials
        # print('token::::::::', token)
        token_data = decode_token(token)

        # print("Token data:", token_data)

        if not token_data or not self.token_valid(token_data):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token"
            )

        if token_data.get('refresh'):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token"
            )

        return token_data

    def token_valid(self, token: str) -> bool:
        token_data = decode_token(token)
        return True if token_data is not None else False
