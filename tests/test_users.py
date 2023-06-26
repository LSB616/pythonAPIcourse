from app import schemas
from .database import session, client
from datetime import datetime

def test_create_user(client):
    res = client.post("/users/", json={"email": "james@gmail.com", "password": "12345"})
    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201
    assert new_user.email == "james@gmail.com"
    assert type(new_user.id) == int
    assert type(new_user.created_at) == datetime

def test_create_user_error(client):
    res_no_data = client.post("/users/", json={})
    assert res_no_data.status_code == 422
    res_incorrect_type = client.post("/users/", json={"email": 345, "password": True})
    assert res_incorrect_type.status_code == 422

def test_get_user(client):
    user = client.post("/users/", json={"email": "henry@gmail.com", "password": "12345"})
    new_user = schemas.UserOut(**user.json())
    res = client.get(f"/users/{new_user.id}/")
    found_user = schemas.UserOut(**res.json())
    assert res.status_code == 200
    assert new_user == found_user

    user2 = client.post("/users/", json={"email": "liam@gmail.com", "password": "54321"})
    comparison_user = schemas.UserOut(**user2.json())
    assert new_user != comparison_user

def test_get_user_error(client):
    res_no_user = client.get("/users/1000/")
    assert res_no_user.status_code == 404
    assert res_no_user.json() == {"detail": "User with ID: 1000 Does Not Exist"}
    res_wrong_data = client.get("/users/asdhgh/")
    assert res_wrong_data.status_code == 422
