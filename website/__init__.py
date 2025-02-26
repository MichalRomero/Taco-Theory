from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_session import Session

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'NSJ/8shj4HD.f37h~jjk8#b7' #encrypts cookies and session data.

    # Configures SQLAlchemy to use SQLite as the database. 
    # The URI format 'sqlite:///{DB_NAME}' specifies a local SQLite database file named by the DB_NAME variable.
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # Initializes the database with the app
    db.init_app(app)

    #importing blueprints
    from .views import views 
    from .auth import auth

    #registering the blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    #tells flask how to load user, looks for primary key
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    with app.app_context():
        if not path.exists(DB_NAME):  # Remove 'website/' from the path
            db.create_all()
            print('Created Database!')


