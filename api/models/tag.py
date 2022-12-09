from api import db, abort
from sqlalchemy.exc import IntegrityError

class TagModel(db.Model):
   __tablename__ = 'tag'
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(255), unique=True, nullable=False)

   def save(self):
      db.session.add(self)
      db.session.commit()
      db.session.rollback()

   def delete(self):
      db.session.delete(self)
      db.session.commit()
