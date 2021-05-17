from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import os, atexit

db = SQLAlchemy()
login_manager = LoginManager()
app = Flask(__name__)

def create_app(config_class=Config):
    Bootstrap(app)
    app.config.from_object(config_class)
    db.init_app(app)
    
    login_manager.login_view = 'hiper_wordpress.login'
    login_manager.login_message = 'Faça login para acessar a página.'
    login_manager.init_app(app)

    from app.hiper_wordpress import bp as integration_bp
    app.register_blueprint(integration_bp)
    db.create_all(app=app)
    app.jinja_env.auto_reload = True

    create_admin_user()

    return app

def create_admin_user():
    from app.hiper_wordpress.service import user_service
    user_service.create_admin_user()
