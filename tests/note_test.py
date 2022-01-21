from flask.testing import FlaskClient

from src.models import Note
from .utils import _test_get, _test_post


def test_note_routes_are_protected(client: FlaskClient) -> None:
    response = client.get('/notes/', follow_redirects=True)
    assert response.status_code == 401

    response = client.get('/notes/create')
    assert response.status_code == 401

    response = client.get('/notes/1')
    assert response.status_code == 401

    response = client.post('/notes/update/1')
    assert response.status_code == 401


def test_note_list(client_with_logged_in_user: FlaskClient) -> None:
    expected_data = []
    for i in range(10):
        expected_data.append(f'Title {i}'.encode())
    _test_get(client_with_logged_in_user, '/notes/', {}, expected_data)


def test_note_index(client_with_logged_in_user: FlaskClient) -> None:
    note = Note.query.first()
    expected_data = [note.title.encode(), note.description.encode()]
    _test_get(client_with_logged_in_user, f'/notes/{note.id}', {}, expected_data)


def test_create_note_with_valid_data(client_with_logged_in_user: FlaskClient) -> None:
    data = {'title': 'Test title', 'description': 'Lorem ipsum desc'}
    _test_post(client_with_logged_in_user, f'/notes/create', data, [b'Test title'])


def test_create_note_with_invalid_data(client_with_logged_in_user: FlaskClient) -> None:
    data = {'title': 'Te', 'description': 'desc'}
    _test_post(client_with_logged_in_user, f'/notes/create', data,
               [b'<span style="color: red;margin: 10px">[Field must be between 4 and 128 characters long.]</span>',
                b'<span style="color: red; margin: 10px">[Field must be at least 10 characters long.]</span>'])


def test_update_note_with_valid_data(client_with_logged_in_user: FlaskClient) -> None:
    note = Note.query.first()
    data = {'title': 'Test title', 'description': 'Lorem ipsum desc'}
    _test_post(client_with_logged_in_user, f'/notes/update/{note.id}', data,
               [b'<h3 class="title">Test title</h3>', b'<p>Lorem ipsum desc</p>'])


def test_update_note_with_invalid_data(client_with_logged_in_user: FlaskClient) -> None:
    note = Note.query.first()
    data = {'title': 'Te', 'description': 'Lsc'}
    _test_post(client_with_logged_in_user, f'/notes/update/{note.id}', data, [
        b'<span style="color: red; margin: 10px">[Field must be between 4 and 128 characters long.]</span>',
        b'<span style="color: red; margin: 10px">[Field must be at least 10 characters long.]</span>'])


def test_update_note_if_note_doesnt_exists(client_with_logged_in_user) -> None:
    response = client_with_logged_in_user.get('/notes/update/439439349349')
    assert response.status_code == 404
