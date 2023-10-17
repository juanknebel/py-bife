from sqlalchemy.orm import Session
from .user import User
from py_bife.application.user_schema import NewUser, UpdateUser, ResponseUserWithMessages
from py_bife.application.message_schema import ResponseMessage
from enum import Enum


class UserErrorType(Enum):
    USER_NOT_FOUND = 1
    USER_ALREADY_EXIST = 2
    EMAIL_DUPLICATED = 3
    SOCIAL_DUPLICATED = 4


class UserErrorException(Exception):
    def __init__(self, error_type: UserErrorType):
        self.error_type = error_type
        super().__init__(f"Custom error of type {error_type.name}")


def get_user_by_username(username: str, db: Session) -> User:
    condition = User.username == username
    return db.query(User).filter(condition).first()


def get_user_by_email(email: str, db: Session) -> User:
    condition = User.email == email
    return db.query(User).filter(condition).first()


def user_exist(user: User, db: Session) -> bool:
    if get_user_by_username(user.username, db) is not None:
        return True
    if get_user_by_email(user.email, db) is not None:
        return True
    return False


def add_new_user(new_user: NewUser, db: Session) -> User:
    db_user = User(
        username=new_user.username,
        email=new_user.email,
        social_network=str(new_user.social_link),
    )

    if user_exist(db_user, db):
        raise UserErrorException(UserErrorType.USER_ALREADY_EXIST)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def update_user(username: str, user: UpdateUser, db: Session) -> User:
    founded = get_user_by_username(username, db)
    if founded is None:
        raise UserErrorException(UserErrorType.USER_ALREADY_EXIST)

    if user.email is not None:
        exist_with_mail = get_user_by_email(user.email, db)
        if exist_with_mail is not None:
            raise UserErrorException(UserErrorType.EMAIL_DUPLICATED)
        founded.email = user.email

    if user.social_link is not None:
        founded.social_network = str(user.social_link)
    db.commit()
    db.refresh(founded)

    return founded


def messages_sent_by(username: str, db: Session) -> ResponseUserWithMessages:
    the_user = get_user_by_username(username, db)
    if the_user is None:
        raise UserErrorException(UserErrorType.USER_NOT_FOUND)
    all_msg = [
        ResponseMessage(
            id=a_msg.id,
            at=a_msg.at,
            from_usr=a_msg.from_user.username,
            to_usr=a_msg.to_user.username,
            message=a_msg.message,
        )
        for a_msg in the_user.sent_messages
    ]
    return ResponseUserWithMessages(username=username, sent_messages=all_msg)
