import os
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from .models import db
from .routes import *
from config import application_configurations

migrate = Migrate()

def create_app():
    """function to create app
    and register extensions and blueprints
    """
    app = Flask(__name__)
    app.config.from_object(application_configurations[os.getenv("FLASK_ENV")])
    CORS(app)
    db.init_app(app)
    db.app = app
    migrate.init_app(app, db)
    app.register_blueprint(resume_blueprint, url_prefix="/api/profile")
    return app