from api import app, multi_auth, request
from api.models.note import NoteModel
from api.models.user import UserModel
from api.schemas.note import note_schema, notes_schema
from utility.helpers import get_object_or_404
from flask import jsonify


@app.route("/notes/<int:note_id>", methods=["GET"])
@multi_auth.login_required
def get_note_by_id(note_id):
    # TODO: авторизованный пользователь может получить только свою заметку или публичную заметку других пользователей
    #  Попытка получить чужую приватную заметку, возвращает ответ с кодом 403
    user = multi_auth.current_user()
    note = NoteModel.query.join(NoteModel.author).filter(UserModel.id==user.id).filter(NoteModel.id==note_id).first()
    if note is None:
        return "", 404
    return note_schema.dump(note), 200


@app.route("/notes", methods=["GET"])
@multi_auth.login_required
def get_notes():
    # TODO: авторизованный пользователь получает только свои заметки и публичные заметки других пользователей
    user = multi_auth.current_user()
    notes = NoteModel.query.join(NoteModel.author).filter(UserModel.id==user.id).all()
    return jsonify(notes_schema.dump(notes)), 200


@app.route("/notes", methods=["POST"])
@multi_auth.login_required
def create_note():
    user = multi_auth.current_user()
    note_data = request.json
    note = NoteModel(author_id=user.id, **note_data)
    note.save()
    return note_schema.dump(note), 201


@app.route("/notes/<int:note_id>", methods=["PUT"])
@multi_auth.login_required
def edit_note(note_id):
    # TODO: Пользователь может редактировать ТОЛЬКО свои заметки.
    #  Попытка редактировать чужую заметку, возвращает ответ с кодом 403
    user = multi_auth.current_user()
    note = NoteModel.query.join(NoteModel.author).filter(UserModel.id == user.id).filter(NoteModel.id == note_id).first()
    if note is None:
        return '', 404
    note_data = request.json
    note.text = note_data["text"]
    note.private = note_data.get("private") or note.private
    note.save()
    return note_schema.dump(note), 200


@app.route("/notes/<int:note_id>", methods=["DELETE"])
@multi_auth.login_required
def delete_note(note_id):
    # TODO: Пользователь может удалять ТОЛЬКО свои заметки.
    #  Попытка удалить чужую заметку, возвращает ответ с кодом 403
    user = multi_auth.current_user()
    note = NoteModel.query.join(NoteModel.author).filter(UserModel.id == user.id).filter(NoteModel.id == note_id).first()
    if note is None:
        return '', 404
    note.delete()
    return '', 200
