from app import schemas
from jose import jwt
from app.config import settings

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




def test_login_user_error(client):
    client.post("/users/", json={"email": "clarence@gmail.com", "password": "12345"})

    #invalid username/nonexistant user
    res_invalid_username = client.post("/login", data={"username": "mary@outlook.com", "password": "12345"})
    assert res_invalid_username.status_code == 403
    assert res_invalid_username.json() == {"detail": "Invalid Credentials"}

    #invalid password
    res_invalid_password = client.post("/login", data={"username": "clarence@gmail.com", "password": "not_the_password"})
    assert res_invalid_password.status_code == 403
    assert res_invalid_password.json() == {"detail": "Invalid Credentials"}

    #no login data
    res_invalid_login = client.post("/login", data={"username": "", "password": ""})
    assert res_invalid_login.status_code == 422