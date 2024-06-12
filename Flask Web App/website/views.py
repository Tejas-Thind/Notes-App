# Import necessary modules from Flask
import os
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, User
from . import db
import json

# Create a Blueprint named 'views'
views = Blueprint('views', __name__)

# Define a route for the home page with both GET and POST methods
@views.route('/', methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in to access this route
def home():

    # Check if the request method is POST
    if request.method == 'POST':
        # Check which button was clicked
        if 'add_note' in request.form:  # Check if the add note button was clicked
            note = request.form.get('note')
            if len(note) < 1:
                flash('Note is too short!', category='error')  
            else:
                # Create a new Note object with the form data and current user's ID
                new_note = Note(data=note, user_id=current_user.id)
                db.session.add(new_note)  
                db.session.commit()  
                flash('Note added!', category='success')  
        elif 'export_note' in request.form:  # Check if the other button was clicked
            # Query all notes from the database by the current user's ID
            notes = db.session.query(Note).all()
            user = User.query.filter_by(id=current_user.id).first()
            # Define the path to the file where the notes will be exported
            path = os.path.join('Notes', f'{user.first_name}' + ' Notes.txt')
            with open(path, 'w') as infile:
                infile.write('Notes:\n')
                infile.write('\n')
                for note in notes:
                    infile.write(note.data + '  Written at: ' + str(note.date) +'\n')
            flash('Note was successfully exported!', category='success')
        elif 'search_note' in request.form:
            search = request.form.get('search')
            if len(search) < 1:
                searched_notes=[]
                flash('Search is too short!', category='error')
            else:
                notes = db.session.query(Note).all()
                searched_notes=[]
                for note in notes:
                    if search in note.data:
                        searched_notes.append(note.data)
                if len(searched_notes) < 1:
                    flash('No notes found!', category='error')
                else:
                    flash('Search completed!', category='success')
        elif 'clear' in request.form:
            searched_notes=[]
            flash('Search cleared!', category='success')

    # Render the home.html template, passing the current user as a context variable and the searched notes if the search button was clicked
    return render_template("home.html", user=current_user, searched_notes=searched_notes if 'search_note' in request.form else None)

# Define a route for deleting a note with the POST method
@views.route('/delete-note', methods=['POST'])
def delete_note():
    # Load the note data from the request
    note = json.loads(request.data)  
    # Extract the note ID from the dictionary made in the previous line
    noteId = note['noteId'] 
    # Query the note from the database by ID
    note = Note.query.get(noteId)  
    if note:  
        if note.user_id == current_user.id: 
            db.session.delete(note) 
            db.session.commit()
            flash('Note deleted!', category='success')

    # Return an empty JSON response
    return jsonify({})
