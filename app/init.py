from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 
        'postgresql://postgres:postgres@localhost:5432/RGZ_RPP7'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    db.init_app(app)
    
    with app.app_context():
        from .migration.migrator import Migrator
        migrator = Migrator(db)
        migrator.run_migrations()
    
    # Регистрируем blueprint
    from . import routes
    app.register_blueprint(routes.bp)
    
    return app