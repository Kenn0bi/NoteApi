from api import app, request, multi_auth, abort
from api.models.user import UserModel
from api.models.note import NoteModel
from api.schemas.user import UserSchema, UserRequestSchema, UserPUTRequestSchema
from api.schemas.note import NoteSchema
from utility.helpers import get_object_or_404
from flask import jsonify
from flask_apispec import doc, marshal_with, use_kwargs
from sqlalchemy.exc import IntegrityError

@app.route("/users/<int:user_id>")
@doc(summary="Get user by id", description='Get user by id', tags=['Users'])
@marshal_with(UserSchema, code=200)
@doc(responses={"404": {"description": "Not found"}})
def get_user_by_id(user_id):
    user = get_object_or_404(UserModel, user_id)
    return user, 200


@app.route("/users")
@doc(summary="Get users", description='Get user', tags=['Users'])
@marshal_with(UserSchema(many=True), code=200)
def get_users():
    users = UserModel.query.all()
    return users, 200


@app.route("/users", methods=["POST"])
@doc(summary="Create new user", description='Create new user', tags=['Users'])
@marshal_with(UserSchema, code=201)
@use_kwargs(UserRequestSchema, location='json')
def create_user(**kwargs):
    user = UserModel(**kwargs)
    try:
        user.save()
    except IntegrityError:
        return "User must be unique", 400
    return user, 201


@app.route("/users/<int:user_id>", methods=["PUT"])
@multi_auth.login_required
@doc(summary="Edit user by id", description='Edit user by id for current auth User', tags=['Users'])
@marshal_with(UserSchema, code=200)
@use_kwargs(UserPUTRequestSchema, location='json')
@doc(responses={"401": {"description": "Unauthorized"}})
@doc(responses={"403": {"description": "Forbidden"}})
@doc(responses={"404": {"description": "Not found"}})
@doc(security=[{"basicAuth": []}])
def edit_user(user_id, **kwargs):
    user = multi_auth.current_user()
    if user_id == user.id:
        for key in kwargs:
            setattr(user, key, kwargs[key])
        user.save()
        return user, 200
    abort(403, description=f"Forbidden")


@app.route("/users/<int:user_id>", methods=["DELETE"])
@multi_auth.login_required(role="admin")
@doc(summary="Delete user by id", description='Delete user by id for current auth User with role=admin', tags=['Users'])
@doc(responses={"401": {"description": "Unauthorized"}})
@doc(responses={"404": {"description": "Not found"}})
@doc(responses={"403": {"description": "Forbidden"}})
@doc(security=[{"basicAuth": []}])
def delete_user(user_id):
    user = get_object_or_404(UserModel, user_id)
    user.delete()
    return '', 204


@app.route("/users/<int:user_id>/notes/", methods=["GET"])
@doc(summary="Get notes by user id", description='Get notes by user id', tags=['Users'])
@doc(responses={"404": {"description": "Not found"}})
@marshal_with(NoteSchema(many=True), code=200)
def get_user_notes(user_id):
    user = get_object_or_404(UserModel, user_id)
    return user.notes, 200
