import pytest

from telegram import WebhookInfo
from telegram.util import shadow_webhook_secret


@pytest.mark.asyncio
async def test_shadow_webhook_secret(mocker):
    info_unsafe = WebhookInfo(
        url="http://localhost/webhook/secret/",
        has_custom_certificate=False,
        pending_update_count=0,
    )

    mocker.patch("telegram.util.settings.webhook_secret", "secret")
    info_safe = shadow_webhook_secret(info_unsafe)

    assert info_safe.url == "http://localhost/webhook/"
