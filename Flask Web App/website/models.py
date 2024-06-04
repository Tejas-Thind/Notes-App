from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Define the Note model (representing the notes table)
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the notes table
    data = db.Column(db.String(10000))  # Column to store the note data, with a maximum length of 10000 characters
    date = db.Column(db.DateTime(timezone=True), default=func.now())  # Timestamp for when the note was created, with timezone support
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Foreign key to link to the user who created the note

# Define the User model (representing the users table)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the users table
    email = db.Column(db.String(150), unique=True)  # Email column with a maximum length of 150 characters, must be unique
    password = db.Column(db.String(150))  # Password column with a maximum length of 150 characters
    first_name = db.Column(db.String(150))  # First name column with a maximum length of 150 characters
    notes = db.relationship('Note')  # Establishes a one-to-many relationship with the Note model, allowing access to all notes associated with a user