from api import app
from api.models.user import UserModel
from sqlalchemy.exc import IntegrityError

@app.cli.command('createsuperuser')
def create_superuser():
   """
   Creates a user with the admin role
   """
   username = input("Username[default 'admin']:")
   password = input("Password[default 'admin']:")
   user = UserModel(username="admin", password="admin", role="admin")
   try:
      user.save()
      print(f"Superuser create successful! id={user.id}")
   except IntegrityError:
      print(f"User must be unique.")

@app.cli.command('getusers')
def get_users():
   """
   Show users in db
   """
   users = UserModel.query.all()
   for i, user in enumerate(users, start=1):
      print(f"{i}. User id: {user.id} {user.username}")

