from flask import Blueprint, request, jsonify
from datetime import datetime
from py_bife.model.message import Message, add_message
from schematics.models import Model
from schematics.types import StringType, IntType, DateTimeType


class MessageDto(Model):
    text = StringType(required=True)
    to_user = IntType(required=True)
    from_user = IntType(required=True)


message_api_bp = Blueprint("mesasge_api", __name__)


@message_api_bp.get("/<int:message_id>")
def get(message_id: int):
    message_found = Message.query.filter_by(id=message_id).first_or_404()
    return jsonify(message_found.to_dict()), 200


@message_api_bp.post("")
def add():
    if not request.headers.get("Content-Type") == "application/json":
        return jsonify({}), 400
    message_dto = MessageDto(request.get_json())
    message_dto.validate()
    new_message = add_message(
        Message(
            message=message_dto.text,
            to_user_id=message_dto.to_user,
            from_user_id=message_dto.from_user,
            at=datetime.utcnow(),
        )
    )

    return jsonify(new_message.to_dict()), 201
