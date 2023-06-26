import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import get_db, Base

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

@pytest.fixture(scope="module")
def test_user(client):
    user_data = {"email": "exampleuser@gmail.com", "password": "12345"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201