import os
from unittest import mock

import pytest

from config import Settings


@pytest.mark.asyncio
def test_settings():
    new_env = {
        "ADMIN_PASSWORD": "admin_password",
        "BLOG_URL": "blog_url",
        "BOT_TOKEN": "bot_token",
        "DATABASE_URL": "database_url",
        "DEBUG": "True",
        "DEBUG_SQL": "False",
        "SERVICE_URL": "service_url",
        "WEBHOOK_SECRET": "webhook_secret",
    }

    with mock.patch.dict(os.environ, new_env, clear=True):
        settings = Settings()

    assert settings.admin_password == "admin_password"
    assert settings.blog_url == "blog_url"
    assert settings.bot_token == "bot_token"
    assert settings.database_url == "database_url"
    assert settings.debug is True
    assert settings.debug_sql is False
    assert settings.service_url == "service_url"
    assert settings.webhook_secret == "webhook_secret"
