from api import app, request, multi_auth, abort
from api.models.tag import TagModel
from api.schemas.tag import tag_schema, tags_schema, TagSchema, TagRequestSchema
from utility.helpers import get_object_or_404
from flask import jsonify
from flask_apispec import doc, marshal_with, use_kwargs
from sqlalchemy.exc import IntegrityError


@app.route("/tags/<int:tag_id>")
@doc(summary="Get tag by id", description='Get tag by id', tags=['Tags'])
@marshal_with(TagSchema, code=200)
@doc(responses={"404": {"description": "Not found"}})
def get_tag_by_id(tag_id):
    tag = get_object_or_404(TagModel, tag_id)
    return tag, 200



@app.route("/tags")
@doc(summary="Get tags", description='Get tags', tags=['Tags'])
@marshal_with(TagSchema(many=True), code=200)
def get_tags():
    tags = TagModel.query.all()
    # return jsonify(tags_schema.dump(tags)), 200
    return tags_schema.dump(tags), 200


@app.route("/tags", methods=["POST"])
@doc(summary="Create new tag", description='Create new tag', tags=['Tags'])
@marshal_with(TagSchema, code=201)
@use_kwargs(TagRequestSchema, location='json')
@doc(responses={"400": {"description": "Bad request"}})
def create_tag(**kwargs):
    tag = TagModel(**kwargs)
    try:
        tag.save()
    except IntegrityError:
        return "Tag must be unique", 400
    return tag, 201

