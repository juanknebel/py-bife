from fastapi import APIRouter, Path, Body, status, Depends, HTTPException
from sqlalchemy.orm import Session

from py_bife.database.database import get_db
from py_bife.model import user_command
from .user_schema import ResponseUser, NewUser, UpdateUser, ResponseUserWithMessages

user_router = APIRouter(prefix="/users")


@user_router.get("/{username}", tags=["users"])
def get(
    username: str = Path(title="The username to retrieve"), db: Session = Depends(get_db)
) -> ResponseUser:
    """Get the user that belongs to the username from the path"""
    found = user_command.get_user_by_username(username=username, db=db)
    if found is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return ResponseUser(
        username=found.username, email=found.email, social_link=found.social_network
    )


@user_router.post("", status_code=status.HTTP_201_CREATED, tags=["users"])
def add(
    new_user: NewUser = Body(title="New user", description="The user to be added"),
    db: Session = Depends(get_db),
) -> ResponseUser:
    """Adds a new user to the system"""
    try:
        added = user_command.add_new_user(new_user=new_user, db=db)
    except user_command.UserErrorException:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="The user cannot be added")

    return ResponseUser(
        username=added.username, email=added.email, social_link=added.social_network
    )


@user_router.put("/{username}", tags=["users"])
def update(
    username: str = Path(title="The username to be updated"),
    user: UpdateUser = Body(title="Updated user", description="The info to be updated"),
    db: Session = Depends(get_db),
) -> ResponseUser:
    """Updates the user that belongs to the username from the path with the received data"""
    try:
        updated = user_command.update_user(username=username, user=user, db=db)
    except user_command.UserErrorException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="The user cannot be updated"
        )
    return ResponseUser(
        username=updated.username, email=updated.email, social_link=updated.social_network
    )


@user_router.get("/{username}/messages", tags=["users"])
def list_messages_sent(
    username: str = Path(title="The username of the messages"), db: Session = Depends(get_db)
) -> ResponseUserWithMessages:
    """List all the messages send by the user in the path"""
    try:
        user_messages = user_command.messages_sent_by(username, db)
    except user_command.UserErrorException as ue:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot retrieve the messages because {ue.error_type}",
        )
    return user_messages
