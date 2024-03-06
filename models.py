"""Models for notes app."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Website User"""

    __tablename__ = "users"

    username = db.Column(
        db.String(20),
        primary_key=True
    )

    hashed_password = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    first_name = db.Column(
        db.String(30),
        nullable=False
    )

    last_name = db.Column(
        db.String(30),
        nullable=False
    )

    notes = db.relationship("Note", backref="user")

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user with hashed password and return user instance"""

        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        user = cls(
            username=username,
            hashed_password=hashed,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        return user

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists and that the associated password is correct
        Return user if valid; else return False"""

        user = cls.query.filter_by(username=username).one_or_none()

        if user and bcrypt.check_password_hash(user.hashed_password, password):
            return user
        else:
            return False


class Note(db.Model):
    """User's notes"""

    __tablename__ = "notes"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    owner_username = db.Column(
        db.String(20),
        db.ForeignKey("users.username"),
        nullable=False
    )

