from app import schemas
from jose import jwt
from app.config import settings
import pytest

def test_login_user(client):
    #create test user
    new_user = client.post("/users/", json={"email": "mary@gmail.com", "password": "12345"})
    new_user_data = new_user.json()
    assert new_user.status_code == 201

    res = client.post("/login", data={"username": "mary@gmail.com", "password": "12345"})
    login_response = schemas.Token(**res.json())
    assert res.status_code == 200
    assert type(login_response.access_token) == str
    assert type(login_response.token_type) == str
    assert login_response.token_type == 'bearer'

    #decode token to ensure user ids match
    payload = jwt.decode(login_response.access_token, settings.secret_key, algorithms=[settings.algorithm])
    assert new_user_data.get("id") == payload.get("user_id")



@pytest.mark.parametrize("email, password, status_code",[
    ("wrongemail@gmail.com", "12345", 403),
    ("exampleuser@gmail.com", "wrongpassword", 403),
    ("wrongemail@gmail.com", "wrongpassword", 403),
    (None, "12345", 422),
    ("exampleuser@gmail.com", None, 422)
])
def test_login_user_error(client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})

    assert res.status_code == status_code

    if res.status_code == 403:
        assert res.json().get("detail") == "Invalid Credentials"