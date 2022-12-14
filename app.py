from api import app, docs, db
from api.models.note import NoteModel
from api.models.user import UserModel
from api.models.note import TagModel
from config import Config
from api.handlers import auth, note, user, tag, file
from flask import render_template, send_from_directory

# CRUD

# Create --> POST
# Read --> GET
# Update --> PUT
# Delete --> DELETE

# USERS
docs.register(user.get_user_by_id)
docs.register(user.get_users)
docs.register(user.create_user)
docs.register(user.edit_user)
docs.register(user.delete_user)
docs.register(user.get_user_notes)

# NOTES
docs.register(note.get_note_by_id)
docs.register(note.get_notes)
docs.register(note.create_note)
docs.register(note.edit_note)
docs.register(note.archive_note)
docs.register(note.restore_note)
docs.register(note.get_user_notes_by_tag)
docs.register(note.get_user_public_notes)
docs.register(note.note_add_tags)
docs.register(note.note_delete_tags)
docs.register(note.get_all_public_notes)
docs.register(note.get_deleted_notes)
docs.register(note.change_note_importance)


# TAGS
docs.register(tag.get_tag_by_id)
docs.register(tag.get_tags)
docs.register(tag.create_tag)
docs.register(tag.edit_tag)
docs.register(tag.delete_tag)

# FILES
docs.register(file.upload_file)
docs.register(file.download_file)


@app.shell_context_processor
def make_shell_context():
   return {'db': db, 'NoteModel': NoteModel, 'UserModel': UserModel, 'TagModel': TagModel}


if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
