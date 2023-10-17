from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from py_bife.database.database import Base


class Message(Base):
    """
    This object represents a message in a relational model.
    """

    __tablename__ = "message"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String(800), nullable=False)
    at = Column(DateTime, nullable=False)
    from_user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    to_user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    from_user = relationship("User", foreign_keys=[from_user_id], back_populates="sent_messages")
    to_user = relationship("User", foreign_keys=[to_user_id], back_populates="received_messages")
