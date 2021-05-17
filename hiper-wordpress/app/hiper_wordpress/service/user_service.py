
from app.hiper_wordpress.domain.User import User
from werkzeug.security import generate_password_hash
from app import db, app
import os

def create_user(user):
    db.session.add(user)
    db.session.commit()
    print('Usuário criado.')

def update_pass(new_pass):
    User.query.filter(User.login==os.environ.get('ADMIN_USER')).update({'password' : generate_password_hash(new_pass, method='sha256')})
    db.session.commit()
    print('Senha atualizada.')

def create_admin_user():
    admin_user =  { 'login' : os.environ.get('ADMIN_USER'), 'pass' : os.environ.get('ADMIN_PASS')}
    with app.app_context():
        user = User.query.filter_by(login=admin_user['login']).first()
        if user is None:
            new_admin_user = User(login=admin_user['login'], password=generate_password_hash(admin_user['pass'], method='sha256'))
            db.session.add(new_admin_user)
            db.session.commit()
            print('Administrador criado.')