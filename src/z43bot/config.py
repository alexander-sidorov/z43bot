from pydantic import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    admin_password: str = Field(..., env="ADMIN_PASSWORD")
    bot_token: str = Field(..., env="BOT_TOKEN")
    debug: bool = Field(env="DEBUG", default=False)
    service_url: str = Field(..., env="SERVICE_URL")

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings: Settings = Settings()
