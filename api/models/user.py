from api import db, Config, ma
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import URLSafeTimedSerializer as Serializer
from itsdangerous import URLSafeSerializer, BadSignature


class UserModel(db.Model):
    # __name = "User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128))
    notes = db.relationship('NoteModel', backref='author', lazy='dynamic')
    role = db.Column(db.String(32), nullable=False, server_default="simple_user", default="simple_user")

    def __init__(self, username, password, role="simple_user"):
        self.username = username
        self.role = role
        self.hash_password(password)

    def get_roles(self):
        return self.role

    def hash_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self):
        s = URLSafeSerializer(Config.SECRET_KEY)
        return s.dumps({'id': self.id})

    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.rollback()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def verify_auth_token(token):
        s = URLSafeSerializer(Config.SECRET_KEY)
        try:
            data = s.loads(token)
        except BadSignature:
            return None  # invalid token
        user = UserModel.query.get(data['id'])
        return user
