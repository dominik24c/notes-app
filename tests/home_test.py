from flask.testing import FlaskClient


def test_home(client: FlaskClient) -> None:
    response = client.get('/')
    assert response.status_code == 200
    assert b'<h3 class="title">Homepage</h3>' in response.data
