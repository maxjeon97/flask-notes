"""Flask app for adopt app."""

import os

from flask import Flask, redirect, render_template, flash, session

from models import db, connect_db, User

from forms import RegisterUserForm, LoginUserForm

USERNAME = 'username'

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "postgresql:///notes")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.get('/')
def redirect_to_register():
    """Redirects to register page"""
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def add_user():
    """Show register form and handle user registration"""

    form = RegisterUserForm()

    if form.validate_on_submit():

        #TODO: handle username/email uniqueness validation

        new_user = User.register(
            username=form.username.data,
            password=form.password.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )

        db.session.add(new_user)
        db.session.commit()

        session[USERNAME] = new_user.username

        flash("Registration successful!")
        return redirect(f"/users/{new_user.username}")

    else:
        return render_template("register_form.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Shows login form and handles user login"""

    form = LoginUserForm()

    if form.validate_on_submit():

        user = User.authenticate(
            username=form.username.data,
            password=form.password.data
        )

        if user:
            session[USERNAME] = user.username

            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ['Invalid username/password.']

    else:
        return render_template('login_form.html')

#TODO: create login_form template.


