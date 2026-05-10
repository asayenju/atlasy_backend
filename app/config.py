from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Supabase Dashboard → Settings → API → JWT Secret (signing secret for user JWTs)
    supabase_jwt_secret: str

    # Optional: e.g. https://<project-ref>.supabase.co/auth/v1 — if set, `iss` is verified
    supabase_jwt_issuer: str | None = None

    # Comma-separated origins for Expo / web dev (e.g. Metro, Expo Go)
    cors_origins: str = (
        "http://localhost:8081,"
        "http://localhost:19006,"
        "http://127.0.0.1:8081,"
        "http://127.0.0.1:19006"
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
