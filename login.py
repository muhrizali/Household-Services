from apps import app
from flask_login import LoginManager
from sqlalchemy import select
from models import db, User, get_with_id

# initializations for login manager
login_manager = LoginManager()
login_manager.init_app(app)

# loader users from string ID

# loading admin
@login_manager.user_loader
def load_user(id):
    user = get_with_id(User, int(id))
    if user:
        return user
    else:
        return None

