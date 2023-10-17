from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from py_bife.database.database import Base
from .message import Message


class User(Base):
    """
    This object represents a user in a relational model.
    """

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    social_network = Column(String(1000), unique=True, nullable=False)

    sent_messages = relationship(
        "Message", back_populates="from_user", foreign_keys=[Message.from_user_id]
    )
    received_messages = relationship(
        "Message", back_populates="to_user", foreign_keys=[Message.to_user_id]
    )
