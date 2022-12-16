from api import app, db, abort
from flask_babel import _

@app.errorhandler(404)
def not_found(e):
    response = {'status': 404, 'error': e.description}
    return response, 404

@app.errorhandler(403)
def not_found(e):
    response = {'status': 403, 'error': e.description}
    return response, 403

@app.errorhandler(401)
def not_found(e):
    response = {'status': 401, 'error': e.description}
    return response, 401

@app.errorhandler(400)
def not_found(e):
    response = {'status': 400, 'error': e.description}
    return response, 400


def get_object_or_404(model: db.Model, object_id: int):
    object = model.query.get(object_id)
    if object is None:
        abort(404, description=_("Object with id=%(object_id)s not found", object_id=object_id))
    if hasattr(object, 'deleted') and object.deleted:
        abort(404, description=_("Object with id=%(object_id)s not found", object_id=object_id))
    return object

