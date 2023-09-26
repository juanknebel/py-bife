from sqlalchemy_serializer import SerializerMixin
from py_bife import db


class User(db.Model, SerializerMixin):
    serialize_only = ("id", "username", "email")
    serialize_rules = ()

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    sent_messages = db.relationship(
        "Message",
        backref="sent_messages",
        lazy=False,
        foreign_keys="Message.from_user_id",
    )
    received_messages = db.relationship(
        "Message",
        backref="received_messages",
        lazy=True,
        foreign_keys="Message.to_user_id",
    )


def add_user(new_user: User) -> User:
    db.session.add(new_user)
    db.session.commit()

    return new_user
