from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "backend"
    debug: bool = True
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/appdb"
    token_pepper: str = "change-me"

    jwt_secret_key: str = "change-this-super-secret-key"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()