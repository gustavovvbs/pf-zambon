from fastapi.testclient import TestClient
from app import app
import pytest
from datetime import date
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, create_engine
from database import get_session
from sqlmodel import Session

@pytest.fixture
def engine():
    eng = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(eng)
    return eng

@pytest.fixture(scope="function")
def db_session(engine):
    connection = engine.connect()
    trans = connection.begin()
    session = Session(bind=connection)

    def _override():
        yield session

    app.dependency_overrides[get_session] = _override
    try:
        yield session
    finally:
        session.close()
        trans.rollback()
        connection.close()
        app.dependency_overrides.pop(get_session, None)

@pytest.fixture(scope="function")
def client(db_session):
    return TestClient(app)

def test_get_movies(client):
    response = client.get("/movies")
    assert response.status_code == 200
    assert response.json() == []

def test_create_movie(client):
    response = client.post("/movies",
                           json={
                               "title": "Test Movie",
                               "description": "Test Description",
                               "duration": 120,
                               "director": "Test Director",
                               "dateCadastro": "2021-01-01"
                           })
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["title"] == "Test Movie"
    assert json_response["description"] == "Test Description"
    assert json_response["duration"] == 120
    assert json_response["director"] == "Test Director"
    assert json_response["dateCadastro"] == "2021-01-01"
    assert json_response["id"] is not None

def test_delete_movie(client):
    # First create a movie
    create_response = client.post("/movies",
                                  json={
                                      "title": "Test Movie to Delete",
                                      "description": "Test Description",
                                      "duration": 120,
                                      "director": "Test Director",
                                      "dateCadastro": "2021-01-01"
                                  })
    assert create_response.status_code == 200
    movie_id = create_response.json()["id"]
    
    # Then delete it
    response = client.delete(f"/movies/{movie_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Movie deleted successfully"}
