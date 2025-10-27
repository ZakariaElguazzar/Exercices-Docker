from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
import os

db = SQLAlchemy()
cache = Redis(host='cache', port=6379)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:password@db:5432/usersdb')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .routes import bp
    app.register_blueprint(bp)

    return app

