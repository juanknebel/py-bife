from flask import Blueprint, request, jsonify
from py_bife.model.user import User, add_user
from schematics.models import Model
from schematics.types import StringType, EmailType


class UserDto(Model):
    username = StringType(required=True)
    email = EmailType(required=True)


user_api_bp = Blueprint("user_api", __name__)


@user_api_bp.get("/<int:user_id>")
def get(user_id: int):
    user_found = User.query.filter_by(id=user_id).first_or_404()
    return jsonify(user_found.to_dict()), 200


@user_api_bp.post("")
def add():
    if not request.headers.get("Content-Type") == "application/json":
        return jsonify({}), 400
    user_dto = UserDto(request.get_json())
    user_dto.validate()
    new_user = add_user(User(username=user_dto.username, email=user_dto.email))

    return jsonify(new_user.to_dict()), 201


@user_api_bp.get("/<int:user_id>/messages")
def list_messages(user_id: int):
    user_found = User.query.filter_by(id=user_id).first_or_404()

    return jsonify([m.to_dict() for m in user_found.sent_messages]), 200
