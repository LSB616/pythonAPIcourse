import pytest
from app.oauth2 import create_access_token

# # creates test user and authorization token
# @pytest.fixture(scope="module")
# def test_user(client):
#     user_data = {"email": "exampleuser@gmail.com", "password": "12345"}
#     res = client.post("/users/", json=user_data)
#     assert res.status_code == 201

#     new_user = res.json()
#     new_user['password'] = user_data['password']
#     return new_user

#Creates authorization token for user

@pytest.fixture(scope="module")
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture(scope="module")
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client