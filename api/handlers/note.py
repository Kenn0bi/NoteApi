from api import app, multi_auth, request, abort
from api.models.note import NoteModel
from api.models.user import UserModel
from api.models.tag import TagModel
from api.schemas.note import NoteSchema, NoteRequestSchema
from utility.helpers import get_object_or_404
from flask_apispec import doc, marshal_with, use_kwargs
from webargs import fields


@app.route("/notes/<int:note_id>", methods=["GET"])
@multi_auth.login_required
@doc(summary="Get note by id", description='Get note by id for current auth User or other public note', tags=['Notes'])
@marshal_with(NoteSchema, code=200)
@doc(responses={"401": {"description": "Unauthorized"}})
@doc(responses={"404": {"description": "Not found"}})
@doc(responses={"403": {"description": "Forbidden"}})
@doc(security=[{"basicAuth": []}])
def get_note_by_id(note_id):
    #  авторизованный пользователь может получить только свою заметку или публичную заметку других пользователей
    #  Попытка получить чужую приватную заметку, возвращает ответ с кодом 403
    user = multi_auth.current_user()
    note = get_object_or_404(NoteModel, note_id)
    notes = NoteModel.query.join(NoteModel.author).filter((UserModel.id==user.id) | (NoteModel.private==False))
    if note in notes:
        return note, 200
    return '', 403


@app.route("/notes", methods=["GET"])
@multi_auth.login_required
@doc(summary="Get notes", description='Get notes for current auth User or other public notes', tags=['Notes'])
@marshal_with(NoteSchema(many=True), code=200)
@doc(responses={"401": {"description": "Unauthorized"}})
@doc(security=[{"basicAuth": []}])
def get_notes():
    # авторизованный пользователь получает только свои заметки и публичные заметки других пользователей
    user = multi_auth.current_user()
    notes = NoteModel.query.join(NoteModel.author).filter((UserModel.id==user.id) | (NoteModel.private==False))
    return notes, 200


@app.route("/notes", methods=["POST"])
@multi_auth.login_required
@doc(summary="Create new note", description='Create new note for current auth User', tags=['Notes'])
@marshal_with(NoteSchema, code=201)
@use_kwargs(NoteRequestSchema, location='json')
@doc(responses={"401": {"description": "Unauthorized"}})
@doc(security=[{"basicAuth": []}])
def create_note(**kwargs):
    user = multi_auth.current_user()
    note = NoteModel(author_id=user.id, **kwargs)
    note.save()
    return note, 201


@app.route("/notes/<int:note_id>", methods=["PUT"])
@multi_auth.login_required
@doc(summary="Edit note by id", description='Edit note by id for current auth User', tags=['Notes'])
@marshal_with(NoteSchema, code=200)
@use_kwargs(NoteRequestSchema, location='json')
@doc(responses={"401": {"description": "Unauthorized"}})
@doc(responses={"404": {"description": "Not found"}})
@doc(responses={"403": {"description": "Forbidden"}})
@doc(security=[{"basicAuth": []}])
def edit_note(note_id, **kwargs):
    #  Пользователь может редактировать ТОЛЬКО свои заметки.
    #  Попытка редактировать чужую заметку, возвращает ответ с кодом 403
    user = multi_auth.current_user()
    note = get_object_or_404(NoteModel, note_id)
    if note.author_id == user.id:
        for key in kwargs:
            setattr(note, key, kwargs[key])
            note.save()
            return note, 200
    abort(403, description=f"Forbidden")

@app.route("/notes/<int:note_id>", methods=["DELETE"])
@multi_auth.login_required
@doc(summary="Delete note by id", description='Delete note by id for current auth User', tags=['Notes'])
@doc(responses={"401": {"description": "Unauthorized"}})
@doc(responses={"404": {"description": "Not found"}})
@doc(responses={"403": {"description": "Forbidden"}})
@doc(security=[{"basicAuth": []}])
def delete_note(note_id):
    #  Пользователь может удалять ТОЛЬКО свои заметки.
    #  Попытка удалить чужую заметку, возвращает ответ с кодом 403
    user = multi_auth.current_user()
    note = get_object_or_404(NoteModel, note_id)
    if note.author_id == user.id:
        note.delete()
        return '', 204
    abort(403, description=f"Forbidden")


@app.route("/notes/filter", methods=["GET"])
@multi_auth.login_required
@doc(summary="Get auth user notes by tags", description='Get auth user notes by tags', tags=['Notes'])
@marshal_with(NoteSchema(many=True), code=200)
@doc(responses={"401": {"description": "Unauthorized"}})
@doc(security=[{"basicAuth": []}])
@use_kwargs({"tag": fields.Str()}, location=('query'))
def get_user_notes_by_tag(**kwargs):
    # авторизованный пользователь получает только свои заметки с указанным тегом
    user = multi_auth.current_user()
    notes = NoteModel.query.filter((NoteModel.author_id==user.id) & (NoteModel.tags.any(name=kwargs['tag']) ))
    return notes, 200


@app.route("/notes/search", methods=["GET"])
@doc(summary="Get public notes by username", description='Get public notes by username', tags=['Notes'])
@marshal_with(NoteSchema(many=True), code=200)
@use_kwargs({"username": fields.Str()}, location=('query'))
def get_user_public_notes(**kwargs):
    # получение публичных заметок пользователя с указанным именем
    notes = NoteModel.query.join(NoteModel.author).filter((UserModel.username==kwargs['username']) & (NoteModel.private==False))
    return notes, 200

@app.route("/notes/<int:note_id>/tags", methods=["PUT"])
@multi_auth.login_required
@doc(summary="Set tags to Note for auth user", description='Set tags to Note for auth user', tags=['Notes'])
@marshal_with(NoteSchema, code=200)
@use_kwargs({"tags": fields.List(fields.Int())}, location=('json'))
@doc(responses={"404": {"description": "Not found"}})
@doc(responses={"401": {"description": "Unauthorized"}})
@doc(security=[{"basicAuth": []}])
def note_add_tags(note_id, **kwargs):
    user = multi_auth.current_user()
    note = get_object_or_404(NoteModel, note_id)
    if note.author_id == user.id:
        for id in kwargs['tags']:
            tag = get_object_or_404(TagModel, id)
            note.tags.append(tag)
        note.save()
        return note, 200
    abort(403, description=f"Forbidden")

@app.route("/notes/<int:note_id>/tags", methods=["DELETE"])
@multi_auth.login_required
@doc(summary="Delete tags from Note", description='Delete tags from Note', tags=['Notes'])
@marshal_with(NoteSchema, code=200)
@use_kwargs({"tags": fields.List(fields.Int())}, location=('json'))
@doc(responses={"404": {"description": "Not found"}})
@doc(responses={"401": {"description": "Unauthorized"}})
@doc(security=[{"basicAuth": []}])
def note_delete_tags(note_id, **kwargs):
    user = multi_auth.current_user()
    note = get_object_or_404(NoteModel, note_id)
    if note.author_id == user.id:
        for id in kwargs['tags']:
            try:
                tag = TagModel.query.get(id)
                if tag:
                    note.tags.remove(tag)
            except ValueError:
                pass
        note.save()
        return note, 200
    abort(403, description=f"Forbidden")

@app.route("/notes/public", methods=["GET"])
@doc(summary="Get all public notes", description='Get all public notes', tags=['Notes'])
@marshal_with(NoteSchema(many=True), code=200)
def get_all_public_notes():
    # получение публичных заметок всех пользователей
    notes = NoteModel.query.filter(NoteModel.private==False)
    return notes, 200
