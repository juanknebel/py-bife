from sqlalchemy_serializer import SerializerMixin
from py_bife import db


class Message(db.Model, SerializerMixin):
    serialize_only = ()
    serialize_rules = ()

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    to_user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )
    from_user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )
    # from_user = db.relationship("User", foreign_keys=[from_user_id])
    at = db.Column(db.DateTime, nullable=False)


def add_message(new_message: Message) -> Message:
    db.session.add(new_message)
    db.session.commit()

    return new_message
