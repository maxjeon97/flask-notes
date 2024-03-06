"""Flask app for adopt app."""

import os

from flask import Flask, redirect, render_template, flash, session

from models import db, connect_db, User, Note

from forms import RegisterUserForm, LoginUserForm, CSRFProtectForm, AddNoteForm
from forms import EditNoteForm

USERNAME_KEY = 'username'

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

        new_user = User.register(
            username=form.username.data,
            password=form.password.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )

        # want commit in view function so that if we do other database operations after adding user, we can use just a single commit total
        db.session.add(new_user)
        db.session.commit()

        session[USERNAME_KEY] = new_user.username

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
            session[USERNAME_KEY] = user.username

            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ['Invalid username/password.']
            return render_template('login_form.html', form=form)


    else:
        return render_template('login_form.html', form=form)


@app.get('/users/<username>')
def display_user_info(username):
    """Displays user info (excluding password)"""
    if USERNAME_KEY not in session:
        flash('You must be logged in to view user information!')
        return redirect('/login')

    if session[USERNAME_KEY] == username:
        user = User.query.get_or_404(username)
        notes = user.notes
        form = CSRFProtectForm()
        return render_template('user.html', user=user, notes=notes, form=form)

    else:
        # could add functionality to throw error page for nonexisting users
        flash("Cannot access other user's information!")
        return redirect(f'/users/{session[USERNAME_KEY]}')


@app.post('/logout')
def logout():
    """Logs out current user in session"""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop(USERNAME_KEY, None)

        flash('Successfully logged out!')
        return redirect('/login')


@app.post('/users/<username>/delete')
def delete_user(username):
    """Deletes user"""

    if USERNAME_KEY not in session:
        flash('Must be logged in to view this page!')
        return redirect('/login')

    if session[USERNAME_KEY] != username:
        flash('You can only delete your own page!')
        return redirect(f'/users/{session[USERNAME_KEY]}')


    form = CSRFProtectForm()

    if form.validate_on_submit():

        user = User.query.get_or_404(username)

        # could use .delete() instead of .all() to do it instantly by deleting
        # everything in the query itself
        notes = Note.query.filter_by(owner_username=username).all()
        for note in notes:
            db.session.delete(note)

        db.session.delete(user)
        db.session.commit()

        session.pop(USERNAME_KEY, None)

        flash("User deleted!")
        return redirect('/')


@app.route('/users/<username>/notes/add', methods=['GET', 'POST'])
def add_note(username):
    """Shows add note form and handles add note form submission"""

    if USERNAME_KEY not in session:
        flash('Must be logged in to view this page!')
        return redirect('/login')

    if session[USERNAME_KEY] != username:
        flash('You can only add notes to your own page!')
        return redirect(f'/users/{session[USERNAME_KEY]}')

    form = AddNoteForm()

    if form.validate_on_submit():
        new_note = Note(
            title=form.title.data,
            content=form.content.data,
            owner_username=username)

        db.session.add(new_note)
        db.session.commit()

        flash('Note added!')
        return redirect(f'/users/{username}')

    else:
        return render_template('add_note_form.html', form=form)


@app.route('/notes/<int:note_id>/update', methods=['GET', 'POST'])
def edit_note(note_id):
    """Shows add note form and handles add note form submission"""

    if USERNAME_KEY not in session:
        flash('Must be logged in to view this page!')
        return redirect('/login')

    note = Note.query.get_or_404(note_id)

    if session[USERNAME_KEY] != note.owner_username:
        flash('You can only update your own notes!')
        return redirect(f'/users/{session[USERNAME_KEY]}')

    form = EditNoteForm(obj=note)

    if form.validate_on_submit():

        note.title = form.title.data
        note.content = form.content.data

        db.session.commit()

        flash("Note updated!")
        return redirect(f"/users/{note.owner_username}")

    else:
        return render_template("edit_note_form.html", form=form, note=note)


@app.post('/notes/<int:note_id>/delete')
def delete_note(note_id):
    """Deletes note"""

    if USERNAME_KEY not in session:
        flash('Must be logged in to view this page!')
        return redirect('/login')

    note = Note.query.get_or_404(note_id)

    if session[USERNAME_KEY] != note.owner_username:
        flash('You can only delete your own notes!')
        return redirect(f'/users/{session[USERNAME_KEY]}')

    form = CSRFProtectForm()

    if form.validate_on_submit():

        db.session.delete(note)
        db.session.commit()

        flash("Note deleted!")
        return redirect(f'/users/{note.owner_username}')
