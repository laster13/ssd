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
    allow_self_registration: bool = True

    streamfusion_public_base_url: str = "https://streamfusion.lastharo.eu"

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

        return self


settings = Settings()