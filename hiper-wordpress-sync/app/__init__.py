from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import os, atexit

db = SQLAlchemy()
app = Flask(__name__)

def create_app(config_class=Config):
    app.config.from_object(config_class)
    db.init_app(app)    
    create_scheduler()

    return app

def create_scheduler():
    from app.hiper_wordpress.service import produtos_service
    jobstore = {
        'default' : SQLAlchemyJobStore(url=os.environ.get('DATABASE_URL').replace('postgres', 'postgresql'))
    }
    scheduler = BackgroundScheduler(jobstore=jobstore, daemon=True)
    scheduler.remove_all_jobs()
    scheduler.add_job(produtos_service.exportar_todos_clientes, 'interval', minutes=5, id='exportar_produtos')
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
