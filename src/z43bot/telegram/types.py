from pydantic import BaseModel
from pydantic import Field


class SendMessage(BaseModel):
    chat_id: int = Field(...)
    text: str = Field(...)


class Chat(BaseModel):
    id: int  # noqa: A003


class Message(BaseModel):
    message_id: int
    chat: Chat
    date: int
    text: str

    class Config:
        fields = {
            "from_": "from",
        }


class Update(BaseModel):
    update_id: int
    message: Message
