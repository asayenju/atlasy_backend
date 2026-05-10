from typing import Any

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth import get_current_claims
from app.config import get_settings

settings = get_settings()

app = FastAPI(title="Atlasy API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    """Public liveness check."""
    return {"status": "ok"}


@app.get("/me")
def me(claims: dict[str, Any] = Depends(get_current_claims)) -> dict[str, Any]:
    """Returns JWT claims for the authenticated Supabase user."""
    sub = claims.get("sub")
    return {
        "sub": sub,
        "email": claims.get("email"),
        "role": claims.get("role"),
        "claims": claims,
    }
