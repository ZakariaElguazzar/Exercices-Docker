from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
import os
import time
import psycopg2
import urllib.parse

db = SQLAlchemy()
cache = Redis(host='cache', port=6379, decode_responses=True)

def wait_for_db(uri, retries=10, delay=3):
    result = urllib.parse.urlparse(uri)
    host = result.hostname
    port = result.port or 5432
    user = result.username
    password = result.password
    dbname = result.path[1:]
    
    for _ in range(retries):
        try:
            conn = psycopg2.connect(
                host=host, port=port, user=user, password=password, dbname=dbname
            )
            conn.close()
            return True
        except Exception as e:
            print("Waiting for DB...", e)
            time.sleep(delay)
    raise Exception("PostgreSQL is not available")

def create_app():
    db_uri = os.environ.get('DATABASE_URL', 'postgresql://postgres:password@db:5432/usersdb')
    
    # attendre que la DB soit prête
    wait_for_db(db_uri)
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # créer les tables
    with app.app_context():
        db.create_all()

    from .routes import bp
    app.register_blueprint(bp)

    return app

