from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
import os

db = SQLAlchemy()
db_path = os.path.realpath("website/database")

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app, resources={r"/foo": {"origins": "http://127.0.0.1:5000/"}})
    
    login_manager = LoginManager()
    login_manager.init_app(app)

    from .model import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
 
    from .view import view
    from .auth import auth
    from .post_movie import post_movie
    app.register_blueprint(view, url_prefix="/")
    app.register_blueprint(post_movie, url_prefix="/movies")
    app.register_blueprint(auth, url_prefix="/auth")


    db.init_app(app)
    create_db(app)
    return app

def create_db(app):
    if not os.path.exists(f"sqlite:///{db_path}/movies.db"):
        with app.app_context():
            db.create_all()
            print("Database created successfully.")