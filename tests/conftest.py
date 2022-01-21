import pytest
from flask import Flask
from flask.testing import FlaskClient

from src import create_app
from src.db import db
from src.models import User, Note


def create_notes(user: User, number_of_notes: int = 10) -> list[Note]:
    notes = []
    for i in range(number_of_notes):
        note = Note(title=f'Title {i}', description=f'Description {i}')
        note.user = user
        notes.append(note)
    return notes


@pytest.fixture
def app() -> Flask:
    app = create_app('testing')

    with app.app_context():
        db.create_all()
        user = User(username="test_user", password="password12", email="test@test.pl",
                    first_name="test", last_name='test')
        db.session.add(user)
        notes = create_notes(user)
        for note in notes:
            db.session.add(note)
        db.session.commit()
    yield app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    with app.test_client() as client:
        yield client


@pytest.fixture
def client_with_logged_in_user(app: Flask) -> FlaskClient:
    with app.test_client() as client:
        client.post('/auth/login', data={'username': 'test_user', 'password': 'password12'}, follow_redirects=True)
        yield client
