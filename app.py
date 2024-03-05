"""Flask app for adopt app."""

import os

from flask import Flask, redirect, render_template, flash, session

from models import db, connect_db, User



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
