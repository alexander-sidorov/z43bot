from .types import Message
from .types import SendMessage
from .util import invoke_api_method


async def send_message(chat_id: int, text: str) -> Message:
    reply = SendMessage(
        chat_id=chat_id,
        text=text,
    )

    message = await invoke_api_method("sendMessage", reply, Message)

    return message
