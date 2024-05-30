from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

# Hashing function is a one way function that does not have an inverse function
#

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST']) # going to the url is a GET request, pressing submit button is a POST request
def login():
    data = request.form
    print(data)
    return render_template("login.html", boolean=True)

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
       email = request.form.get('email')
       firstName = request.form.get('firstName') 
       password1 = request.form.get('password1') 
       password2 = request.form.get('password2')

       counter = 0
       for i in range(len(password1)):
           if password1[i].isdigit():
               counter+=1

       if len(email) < 4:
           flash('Email must be greater than 3 characters.', category='error')
       elif len(firstName) < 2:
           flash('First name must be greater than 1 character.', category='error')
       elif password1 != password2:
           flash('Passwords don\'t match.', category='error')
       elif len(password1) < 7:
           flash('Password must be at least 7 characters.', category='error')
       elif counter == 0:
           flash('Password must contain a number.', category='error')
       else:
           new_user = User(email=email, firstName=firstName, password=generate_password_hash(password1, method='sha256'))
           db.session.add(new_user)
           db.session.commit()
           flash('Account created!', category='success')
           return redirect(url_for('views.home'))
           
    return render_template("sign up.html")
