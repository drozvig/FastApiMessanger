from pydantic import BaseModel


class Message_ALL(BaseModel):
    text_message: str
    author: str
