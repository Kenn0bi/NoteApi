import marshmallow


class FileSchema(marshmallow.Schema):
   image = marshmallow.fields.Raw(type='file')