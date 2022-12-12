from api import app, docs
from config import Config
from api.handlers import auth, note, user, tag

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

# NOTES
docs.register(note.get_note_by_id)
docs.register(note.get_notes)
docs.register(note.create_note)
docs.register(note.edit_note)
docs.register(note.delete_note)

# TAGS
docs.register(tag.get_tag_by_id)
docs.register(tag.get_tags)
docs.register(tag.create_tag)
docs.register(tag.note_add_tags)

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
