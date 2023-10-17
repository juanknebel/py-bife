from pydantic import BaseModel, Field
from datetime import datetime


class BaseMessage(BaseModel):
    message: str = Field(
        description="The text representing the message", min_length=1, max_length=800
    )


class NewMessage(BaseMessage):
    from_usr: str = Field(description="The user who sends the message")
    to_usr: str = Field(description="The user who receives the message")


class ResponseMessage(NewMessage):
    id: int = Field(description="The message id")
    at: datetime = Field(description="The timestamp the message was sent")
