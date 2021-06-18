from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)  # set up a blueprint inside the app

@auth.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            # to check if password match the record
            if check_password_hash(user.passworkd, password):
                flash('logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template('login.html', user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign_up', methods=['POST','GET'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email = email).first()
        if user:
            flash('This email has been used. Go to login page to log in', category='error')

        elif len(email)<4:
            flash('Email needs to be at least 4 characters long.', category='error')
        elif len(firstName)<2:
            flash('First name needs to be at least 2 characters long.' , category='error')
        elif password1 != password2:
            flash('Password not match.', category='error')
        elif len(password1) < 3:
            flash('Password needs to be at least 3 characters long.', category='error')
        else:
            # to create a new user
            new_user = User(email=email, first_name = firstName, passworkd = generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!' , category='success')
            # login the user
            login_user(new_user,remember=True)
            return redirect(url_for('views.home'))


    return render_template('sign_up.html', user = current_user)