import sys, os
import click

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import json
from sqlalchemy import create_engine, MetaData, insert, Table
from sqlalchemy.orm import sessionmaker
from config import Config, BASE_DIR
from api.models.note import NoteModel
from api.models.user import UserModel
from sqlalchemy.exc import IntegrityError

@click.command
@click.argument('file_name', default='notes.json')
def load_db(file_name):
   path_to_db = Config.SQLALCHEMY_DATABASE_URI
   file_name = BASE_DIR / "fixtures" / file_name
   engine = create_engine(path_to_db)
   meta = MetaData(bind=engine)
   DBSession = sessionmaker(bind=engine)
   session = DBSession()

   with open(file_name, "r", encoding="UTF-8") as f:
       data = json.load(f)
       for table_name, values in data.items():
           table = Table(table_name, meta, autoload=True)
           query_insert = insert(table)
           for value in values:
                query_insert = query_insert.values(value)
                try:
                    session.execute(query_insert)
                    session.commit()
                except IntegrityError:
                    pass


load_db()
