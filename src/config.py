from pydantic import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    admin_password: str = Field(..., env="ADMIN_PASSWORD")
    blog_url: str = Field(..., env="BLOG_URL")
    bot_token: str = Field(..., env="BOT_TOKEN")
    database_url: str = Field(..., env="DATABASE_URL")
    debug: bool = Field(env="DEBUG", default=False)
    debug_sql: bool = Field(env="DEBUG_SQL", default=False)
    service_url: str = Field(..., env="SERVICE_URL")

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings: Settings = Settings()
