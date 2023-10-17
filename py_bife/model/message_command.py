from sqlalchemy.orm import Session
from enum import Enum
from datetime import datetime
from py_bife.application.message_schema import NewMessage, ResponseMessage
from .message import Message
from .user_command import get_user_by_username


class MessageErrorType(Enum):
    USER_NOT_FOUND = 1
    MESSAGE_NOT_FOUND = 2
    MESSAGE_NOT_ADDED = 3


class MessageErrorException(Exception):
    def __init__(self, error_type: MessageErrorType):
        self.error_type = error_type
        super().__init__(f"Custom error of type {error_type.name}")


def get(message_id: int, db: Session) -> ResponseMessage:
    found = db.query(Message).filter(Message.id == message_id).first()
    return ResponseMessage(
        id=found.id,
        message=found.message,
        from_usr=found.from_user.username,
        to_usr=found.to_user.username,
        at=found.at,
    )


def new_message(the_message: NewMessage, db: Session) -> ResponseMessage:
    with db.begin():
        from_usr = get_user_by_username(the_message.from_usr, db)
        to_usr = get_user_by_username(the_message.to_usr, db)

        if from_usr is None or to_usr is None:
            raise MessageErrorException(MessageErrorType.USER_NOT_FOUND)

        message_added = Message(
            message=the_message.message,
            from_user_id=from_usr.id,
            to_user_id=to_usr.id,
            at=datetime.utcnow(),
        )
        db.add(message_added)
        db.flush()
        return ResponseMessage(
            id=message_added.id,
            message=message_added.message,
            from_usr=the_message.from_usr,
            to_usr=the_message.to_usr,
            at=message_added.at,
        )
