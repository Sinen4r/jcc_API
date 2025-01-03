from datetime import timedelta
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_smorest import Api
from db import db
from flask_cors import CORS

from resources.movies import blpM
from resources.programs import blpProg
from resources.venues import blpVen
from resources.agenda import blp
from resources.authentication import blpAuth

from flask_jwt_extended import JWTManager

def create_app(db_url=None):
    app = Flask(__name__)
    CORS(app) 
    app.config["API_TITLE"] = "TBS REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:test@db:5432/jcc_festival'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["JWT_SECRET_KEY"]="5e884898da28047151d0e56f8dc6292773603d0d6aabbddc73e06ef7ff70e2c4"
    db.init_app(app)
    api = Api(app)
    jwt = JWTManager(app)
    app.config['JWT_COOKIE_SECURE'] = False
    app.config['JWT_ACCESS_COOKIE_PATH'] = '/' 
    app.config['JWT_COOKIE_CSRF_PROTECT'] = True
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=2) 
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://myuser:mypassword@db:5432/mydatabase')


            
    api.register_blueprint(blp)
    api.register_blueprint(blpProg)
    api.register_blueprint(blpM)
    api.register_blueprint(blpVen)
    api.register_blueprint(blpAuth)
    return app


# app.register_blueprint(movies_bp, url_prefix='/movies')
# app.register_blueprint(programs_bp, url_prefix='/programs')
# app.register_blueprint(venues_bp, url_prefix='/venues')
from sqlalchemy import inspect
from sqlalchemy import create_engine

# Create an engine using your DATABASE URI
engine = create_engine('postgresql://postgres:test@db:5432/jcc_festival')

# Try connecting to the database
try:
    connection = engine.connect()
    print("Connected to the database successfully!")
    connection.close()
except Exception as e:
    print(f"Failed to connect to the database: {e}")
# Get an inspector object
inspector = inspect(engine)

# List all schemas (useful to confirm if `jcc_festival` exists)
schemas = inspector.get_schema_names()
print(schemas)

# List all tables within the `jcc_festival` schema
tables = inspector.get_table_names(schema='jcc_festival')  # Replace with your actual schema name
print(tables)