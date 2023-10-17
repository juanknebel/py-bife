from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import Optional, List
from .message_schema import ResponseMessage


class BaseUser(BaseModel):
    """Represents basic user data"""

    username: str = Field(description="The username", min_length=3, max_length=20)


class NewUser(BaseUser):
    """Represents the creation of a new user data"""

    password: str = Field(description="The password")
    email: EmailStr = Field(description="The email of the user")
    social_link: HttpUrl = Field(description="The link to the main social network")


class UpdateUser(BaseModel):
    """Represents the attributes that could be updated to the user"""

    email: Optional[EmailStr] = Field(description="The email of the user")
    social_link: Optional[HttpUrl] = Field(description="The link to the main social network")


class ResponseUser(BaseUser):
    """Represents a user to return"""

    email: EmailStr = Field(description="The email of the user")
    social_link: HttpUrl = Field(description="The link to the main social network")


class ResponseUserWithMessages(BaseUser):
    """Represents all the messages send by one user"""

    sent_messages: List[ResponseMessage] = Field(description="The list of messages")
