from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "backend"
    environment: str = "production"
    debug: bool = False

    database_url: str
    token_pepper: str
    jwt_secret_key: str
    totp_encryption_key: str

    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 15
    jwt_issuer: str = "ssd.lastharo.eu"
    jwt_audience: str = "ssd-api"

    allow_self_registration: bool = True

    redis_url: str = "redis://redis:6379/0"
    rate_limit_redis_prefix: str = "ssd:ratelimit"

    streamfusion_public_base_url: str = "https://streamfusion.lastharo.eu"
    streamfusion_token_ttl_seconds: int = 600
    streamfusion_session_ttl_seconds: int = 7200
    streamfusion_session_cookie_name: str = "streamfusion_session"
    streamfusion_bind_user_agent: bool = True
    streamfusion_bind_ip: bool = False

    streamfusion_database_url: str
    streamfusion_meili_url: str = "http://localhost:7700"
    streamfusion_meili_master_key: str
    torznab_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @model_validator(mode="after")
    def validate_security(self):
        bad_values = {
            "",
            "change-me",
            "change-this-super-secret-key",
            "CHANGE_ME_LONG_RANDOM_SECRET",
        }

        if self.environment == "production" and self.debug:
            raise ValueError("DEBUG must be false in production")

        if self.token_pepper in bad_values or len(self.token_pepper) < 32:
            raise ValueError("TOKEN_PEPPER must be a strong unique secret")

        if self.jwt_secret_key in bad_values or len(self.jwt_secret_key) < 32:
            raise ValueError("JWT_SECRET_KEY must be a strong unique secret")

        if not self.jwt_issuer.strip():
            raise ValueError("JWT_ISSUER must not be empty")

        if not self.jwt_audience.strip():
            raise ValueError("JWT_AUDIENCE must not be empty")

        if not self.redis_url.strip():
            raise ValueError("REDIS_URL must not be empty")

        if not self.rate_limit_redis_prefix.strip():
            raise ValueError("RATE_LIMIT_REDIS_PREFIX must not be empty")

        if not self.streamfusion_public_base_url.startswith("https://"):
            raise ValueError("STREAMFUSION_PUBLIC_BASE_URL must start with https://")

        if self.streamfusion_token_ttl_seconds < 60:
            raise ValueError("STREAMFUSION_TOKEN_TTL_SECONDS must be >= 60")

        if self.streamfusion_session_ttl_seconds < 300:
            raise ValueError("STREAMFUSION_SESSION_TTL_SECONDS must be >= 300")

        cookie_name = self.streamfusion_session_cookie_name.strip()
        if not cookie_name:
            raise ValueError("STREAMFUSION_SESSION_COOKIE_NAME must not be empty")
        self.streamfusion_session_cookie_name = cookie_name

        return self


settings = Settings()