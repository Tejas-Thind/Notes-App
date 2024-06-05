from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# Create a Blueprint for authentication routes
auth = Blueprint('auth', __name__)

# Login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')  # Get email from form
        password = request.form.get('password')  # Get password from form

        user = User.query.filter_by(email=email).first()  # Query user by email
        if user:
            if check_password_hash(user.password, password):  # Check if password matches
                login_user(user, remember=True)  # Log in the user
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.home'))  # Redirect to home page
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)  # Render login template

# Logout route
@auth.route('/logout')
@login_required
def logout():
    logout_user()  # Log out the user
    flash('Logged out successfully!', category='success')
    return redirect(url_for('auth.login'))  # Redirect to login page


# Sign-up route
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')  # Get email from form
        first_name = request.form.get('firstName')  # Get first name from form
        password1 = request.form.get('password1')  # Get password from form
        password2 = request.form.get('password2')  # Get password confirmation from form

        counter = 0
        for i in range(len(password1)):
            if password1[i].isdigit():
                counter += 1

        user = User.query.filter_by(email=email).first()  # Query user by email
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif counter == 0:
            flash('Password must contain a number.', category='error')
        else:
            # Create new user with hashed password
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)  # Add new user to the database session
            db.session.commit()  # Commit the session to save the user
            login_user(new_user, remember=True)  # Log in the new user
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))  # Redirect to home page

    return render_template("sign up.html", user=current_user)  # Render sign-up template
