from api import app, request, multi_auth, abort
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema, UserSchema, UserRequestSchema
from utility.helpers import get_object_or_404
from flask import jsonify
from flask_apispec import doc, marshal_with, use_kwargs


@app.route("/users/<int:user_id>")
@multi_auth.login_required
@doc(summary="Get user by id", description='Get user by id for current auth User', tags=['Users'])
@marshal_with(UserSchema, code=200)
@doc(responses={"401": {"description": "Unauthorized"}})
@doc(responses={"404": {"description": "Not found"}})
@doc(responses={"403": {"description": "Forbidden"}})
@doc(security=[{"basicAuth": []}])
def get_user_by_id(user_id):
    auth_user = multi_auth.current_user()
    user = get_object_or_404(UserModel, user_id)
    if user.id == auth_user.id:
        return user, 200
    abort(403, description=f"Forbidden")



@app.route("/users")
@doc(summary="Get users", description='Get user', tags=['Users'])
@marshal_with(UserSchema(many=True), code=200)
def get_users():
    users = UserModel.query.all()
    return jsonify(users_schema.dump(users)), 200


@app.route("/users", methods=["POST"])
@multi_auth.login_required(role="admin")
@doc(summary="Create new user", description='Create new user for current auth User with role=admin', tags=['Users'])
@marshal_with(UserSchema, code=201)
@use_kwargs(UserRequestSchema, location='json')
@doc(responses={"400": {"description": "Bad request"}})
@doc(responses={"401": {"description": "Unauthorized"}})
@doc(responses={"403": {"description": "Forbidden"}})
@doc(security=[{"basicAuth": []}])
def create_user(**kwargs):
    user = UserModel(**kwargs)
    # TODO: добавить обработчик на создание пользователя с неуникальным username
    user.save()
    if user.id:
        return user, 201
    abort(400, description=f"User must be unique")


@app.route("/users/<int:user_id>", methods=["PUT"])
@multi_auth.login_required
@doc(summary="Edit user by id", description='Edit user by id for current auth User', tags=['Users'])
@marshal_with(UserSchema, code=200)
@use_kwargs(UserRequestSchema, location='json')
@doc(responses={"401": {"description": "Unauthorized"}})
@doc(responses={"403": {"description": "Forbidden"}})
@doc(responses={"404": {"description": "Not found"}})
@doc(security=[{"basicAuth": []}])
def edit_user(user_id, **kwargs):
    auth_user = multi_auth.current_user()
    user = get_object_or_404(UserModel, user_id)
    if user.id == auth_user.id:
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
    """
    Пользователя может удалять ТОЛЬКО администратор
    """
    user = get_object_or_404(UserModel, user_id)
    user.delete()
    return '', 200
