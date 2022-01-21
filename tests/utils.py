from pprint import pprint

from flask.testing import FlaskClient


def _test_assertions(response, expected_data: list, status_code: int = 200) -> None:
    assert response.status_code == status_code
    for data in expected_data:
        assert data in response.data


def _test_post(client: FlaskClient, url: str, data: dict, expected_data: list) -> None:
    response = client.post(url, data=data, follow_redirects=True)
    pprint(response.data)
    _test_assertions(response, expected_data)


def _test_get(client: FlaskClient, url: str, data: dict, expected_data: list) -> None:
    response = client.get(url, data=data, follow_redirects=True)
    _test_assertions(response, expected_data)
