import pytest
from flask.testing import FlaskClient

from .utils import _test_post, _test_get, _test_assertions


@pytest.fixture(scope='function')
def user_data() -> dict:
    data = {
        "username": "username",
        "password": "password12",
        "confirm_password": "password12",
        "email": "johnny@wp.pl",
        "first_name": "Johnny",
        "last_name": "Cash"
    }
    return data


@pytest.fixture
def expected_data() -> list:
    return [b'Login', b'Register', b'Home', b'<h3 class="title">Registration page</h3>']


def _test_case(client: FlaskClient, data: dict, additional_expected_data: list) -> None:
    response = client.post('/auth/register', data=data, follow_redirects=True)
    expected_data = [b'Login', b'Register', b'Home',
                     b'<h3 class="title">Registration page</h3>'] + additional_expected_data
    _test_assertions(response, expected_data)


def test_register_template(client: FlaskClient) -> None:
    response = client.get('/auth/register')
    expected_data = [b'<h3 class="title">Registration page</h3>', b'username', b'email', b'password',
                     b'confirm_password', b'first_name', b'last_name']
    _test_assertions(response, expected_data)


def test_register_with_valid_data(client: FlaskClient, user_data: dict) -> None:
    _test_post(client, '/auth/register', user_data,
               [b'Login', b'Register', b'Home', b'<h3 class="title">Login page</h3>'])


def test_register_with_empty_fields(client: FlaskClient, user_data: dict, expected_data: list) -> None:
    _test_post(client, '/auth/register', {},
               expected_data + [b'<span style="color:red; margin:10px;">This field is required.</span>'])


def test_register_with_different_passwords(client: FlaskClient, user_data: dict, expected_data: list) -> None:
    user_data['password'] = f"{user_data['password']}1"
    _test_post(client, '/auth/register', user_data,
               expected_data + [b'<span style="color:red; margin:10px;">Field must be equal to password.</span>'])


def test_register_with_invalid_first_name(client: FlaskClient, user_data: dict, expected_data: list) -> None:
    user_data['first_name'] = "d"
    _test_post(client, '/auth/register', user_data, expected_data + [
        b'<span style="color:red; margin:10px;">Field must be between 2 and 64 characters long.</span>'])


def test_register_with_invalid_last_name(client: FlaskClient, user_data: dict, expected_data: list) -> None:
    user_data['last_name'] = "d"
    _test_post(client, '/auth/register', user_data, expected_data + [
        b'<span style="color:red; margin:10px;">Field must be between 2 and 64 characters long.</span>'])


def test_login_template(client: FlaskClient, user_data: dict) -> None:
    _test_get(client, '/auth/login', {}, [b'<h3 class="title">Login page</h3>', b'username', b'password'])


def test_login_with_valid_data_and_logout(client: FlaskClient) -> None:
    _test_post(client, '/auth/login', {"username": "test_user", "password": "password12"},
               [b'<a href="/auth/logout">Logout</a>'])
    _test_get(client, '/auth/logout', {}, [b'<h3 class="title">Login page</h3>'])
