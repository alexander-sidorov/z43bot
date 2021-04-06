from pydantic import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    bot_token: str = Field(..., env="BOT_TOKEN")
    debug: bool = Field(env="DEBUG", default=False)
    python_path: str = Field(..., env="PYTHONPATH")
    service_url: str = Field(..., env="SERVICE_URL")

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"
        fields = {
            "from_": "from",
        }


settings: Settings = Settings()

if __name__ == "__main__":
    from z43bot.util import debug

    debug(settings)
