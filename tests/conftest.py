import pytest
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from token_store.app import app
from token_store.persistence.models import Base


@pytest.fixture(scope="session")
def engine() -> Engine:
    """
    Creates a new database connection before running all the tests
    then closes the connection after the tests are done
    It uses psycopg as the database driver to avoid issues with asyncpg in different event loops

    This is a session scoped fixture, so it will only be created once before all the tests
    :return:
    """
    engine = create_engine(
        "postgresql+psycopg://postgres:mysecretpassword@localhost:5432/postgres"
    )
    yield engine
    engine.dispose()


@pytest.fixture(scope="session")
def create(engine: Engine):
    """
    Creates the tables in the database before running all the tests
    then drops the tables after the tests are done

    Because the scope is session, this fixture will run only once before all the tests
    :param engine:
    :return:
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def session(engine: Engine, create) -> Session:
    """
    Creates a new session for each test
    This makes sure the session is closed after the test is done

    :param engine:
    :param create:
    :return session:
    """
    with Session(engine) as session:
        yield session


@pytest.fixture(scope="session")
def client() -> TestClient:
    """
    Creates a test client for the FastAPI application

    This is a session scoped fixture, so it will only be created once before all the tests
    :return client:
    """
    with TestClient(app=app) as client:
        yield client

