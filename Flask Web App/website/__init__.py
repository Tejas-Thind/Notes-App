from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, current_user

# Initialize the database instance
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Random Words'  # Set a secret key for session management
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # Configure the database URI
    db.init_app(app)  # Initialize the database with the app

    from .views import views  # Import the views blueprint
    from .auth import auth  # Import the auth blueprint

    # Register the blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note  # Import the models

    # Ensure the database is created before returning the app
    with app.app_context():
        create_database()

    # Set up the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Define the view for login
    login_manager.init_app(app)  # Initialize the login manager with the app

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))  # Load the user by ID

    return app

def create_database():
    if not path.exists('website/' + DB_NAME):  # Check if the database file does not exist
        db.create_all()  # Create the database and tables
        print('Created Database!')  # Print a confirmation message
    else:
        print('Database Already Exists!')