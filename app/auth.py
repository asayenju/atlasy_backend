from typing import Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError

from app.config import Settings, get_settings

security = HTTPBearer(auto_error=False)


def decode_supabase_jwt(token: str, settings: Settings) -> dict:
    """
    Verify a Supabase-issued access token using the project's JWT secret (HS256).

    Uses the same secret as Dashboard → Settings → API → JWT Secret.
    User session tokens typically include aud='authenticated'.
    """
    decode_kwargs: dict[str, Any] = {
        "algorithms": ["HS256"],
        "audience": "authenticated",
        "options": {
            "verify_signature": True,
            "verify_exp": True,
            "verify_aud": True,
        },
    }
    if settings.supabase_jwt_issuer:
        decode_kwargs["issuer"] = settings.supabase_jwt_issuer

    try:
        return jwt.decode(token, settings.supabase_jwt_secret, **decode_kwargs)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_claims(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    settings: Settings = Depends(get_settings),
) -> dict:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return decode_supabase_jwt(credentials.credentials, settings)
