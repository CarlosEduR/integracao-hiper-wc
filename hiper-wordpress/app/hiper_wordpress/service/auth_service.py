from app import db
from app.hiper_wordpress.domain.User import User
from app import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
