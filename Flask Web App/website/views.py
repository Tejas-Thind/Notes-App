# Import necessary modules from Flask
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note  
from . import db 
import json

# Create a Blueprint named 'views'
views = Blueprint('views', __name__)

# Define a route for the home page with both GET and POST methods
@views.route('/', methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in to access this route
def home():
    if request.method == 'POST': 
        note = request.form.get('note') 
        if len(note) < 1:  
            flash('Note is too short!', category='error')  
        else:
            # Create a new Note object with the form data and current user's ID
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)  
            db.session.commit()  
            flash('Note added!', category='success')  

    # Render the home.html template, passing the current user as a context variable
    return render_template("home.html", user=current_user)

# Define a route for deleting a note with the POST method
@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)  
    noteId = note['noteId'] 
    note = Note.query.get(noteId)  
    if note:  # Check if the note exists
        if note.user_id == current_user.id: 
            db.session.delete(note) 
            db.session.commit()

    return jsonify({})  # Return an empty JSON response
