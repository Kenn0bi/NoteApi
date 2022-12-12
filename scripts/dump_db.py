import sys, os
import click

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import json
from sqlalchemy import create_engine, MetaData
from config import Config, BASE_DIR
from api.models.note import NoteModel
from api.models.user import UserModel
from api.models.tag import TagModel

@click.command
@click.argument('file_name', default='data.json')
def dump_db(file_name):
   path_to_db = Config.SQLALCHEMY_DATABASE_URI
   models_only=[UserModel, NoteModel, TagModel]
   file_name = BASE_DIR / "fixtures" / file_name
   engine = create_engine(path_to_db)
   meta = MetaData()
   meta.reflect(bind=engine)
   result = {}
   for table in meta.sorted_tables:
       if models_only and table.name not in [model.__tablename__ for model in models_only]:
           continue
       result[table.name] = [dict(row) for row in engine.execute(table.select())]

   with open(file_name, "w", encoding="UTF-8") as f:
       json.dump(result, f, ensure_ascii=False, indent=4)


dump_db()