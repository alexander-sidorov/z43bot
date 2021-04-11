from typing import Optional

from .types import Message
from .types import SendMessage
from .util import invoke_api_method


async def send_message(
    chat_id: int,
    text: str,
    *,
    reply_to_message_id: Optional[int] = None,
) -> Message:
    reply = SendMessage(
        chat_id=chat_id,
        reply_to_message_id=reply_to_message_id,
        text=text,
    )

    message = await invoke_api_method("sendMessage", reply, Message)

    return message
