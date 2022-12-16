import os
from api import app
from flask_apispec import doc, use_kwargs
from api.schemas.file import FileSchema
from config import Config
from flask import send_from_directory

@app.route('/files/upload', methods=["PUT"])
@doc(tags=['Files'])
@use_kwargs(FileSchema, location="files")
def upload_file(**kwargs):
   uploaded_file = kwargs["image"]
   target = Config.UPLOAD_FOLDER / uploaded_file.filename
   uploaded_file.save(target)
   return {"msg": "uploaded image successfully",
           "url": os.path.join(Config.UPLOAD_FOLDER_NAME, uploaded_file.filename)}, 200


@app.route('/upload/<path:filename>')
@doc(tags=['Files'])
def download_file(filename):
   return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)