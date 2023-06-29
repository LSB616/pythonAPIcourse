import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


#creates a session class which will delete old tables first, create fresh tables, run the tests therefore preventing errors from duplicate entries. 
# Also, allows you to include -x statement in pytest so that tables remain for inspection if a failure occurs.
#scope="module" allows all tests to be run before test database is dropped. Scope can be changed, see documents.

@pytest.fixture(scope="module")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


#creates test user
@pytest.fixture(scope="module")
def test_user(client):
    user_data = {"email": "exampleuser@gmail.com", "password": "12345"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

#creates seondary user for error testing
@pytest.fixture(scope="module")
def test_user_2(client):
    user_data = {"email": "alternativeuser@gmail.com", "password": "12345"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

#Create test posts

@pytest.fixture(scope="module")
def test_posts(test_user, session, test_user_2):
    posts_data = [
        {"title": "1st title",
         "content": "1st content",
         "owner_id": test_user['id']},
        {"title": "2nd title",
         "content": "2nd content",
         "owner_id": test_user['id']},
        {"title": "3rd title",
         "content": "3rd content",
         "owner_id": test_user['id']},
        {"title": "4th title",
         "content": "4th content",
         "owner_id": test_user_2['id']},
        {"title": "5th title",
         "content": "5th content",
         "owner_id": test_user_2['id']}
        ]
    
    def create_post_model(post):
        return models.Post(**post)

    post_list = list(map(create_post_model, posts_data))

    session.add_all(post_list)
    session.commit()
    posts = session.query(models.Post).all()
    return posts
