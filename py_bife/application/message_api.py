from fastapi import APIRouter, Path, Body, status, Depends, HTTPException
from sqlalchemy.orm import Session
from .message_schema import ResponseMessage, NewMessage

from py_bife.database.database import get_db
from py_bife.model import message_command

message_router = APIRouter(prefix="/messages")


@message_router.get("/{message_id}", tags=["messages"])
def get(
    message_id: int = Path(title="The message id to retrieve"), db: Session = Depends(get_db)
) -> ResponseMessage:
    """Get the message that belongs to the id in the path"""
    found = message_command.get(message_id=message_id, db=db)
    if found is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    return found


@message_router.post("", status_code=status.HTTP_201_CREATED, tags=["messages"])
def add(
    new_message: NewMessage = Body(title="New Message", description="The message to send"),
    db: Session = Depends(get_db),
) -> ResponseMessage:
    """Send a new message into the system"""
    try:
        added = message_command.new_message(new_message, db)
    except message_command.MessageErrorException as me:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot send the message {me.error_type}",
        )
    return added
