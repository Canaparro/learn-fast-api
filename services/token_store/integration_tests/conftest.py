import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from ..src.app import app
from src.persistence.database import get_database_env_values
from ..src.persistence.models import Base


@pytest.fixture(scope="session", autouse=True)
def postgres_container():
    user = "test_user"
    password = "test_password"
    os.environ["POSTGRES_USERNAME"] = user
    os.environ["POSTGRES_PASSWORD"] = password
    with PostgresContainer(
        "postgres:latest", username=user, password=password
    ) as postgres:
        database_host = postgres.get_container_host_ip()
        database_port = postgres.get_exposed_port(5432)
        os.environ["POSTGRES_HOST"] = database_host
        os.environ["POSTGRES_PORT"] = str(database_port)
        yield


@pytest.fixture(scope="session")
def engine() -> Engine:
    """
    Creates a new database connection before running all the tests
    then closes the connection after the tests are done
    It uses psycopg as the database driver to avoid issues
    with trying to use asyncpg in different event loops

    This is a session scoped fixture therefore
    it will only be created once before all the tests
    :return:
    """

    database, host, password, port, username = get_database_env_values()
    engine = create_engine(
        f"postgresql+psycopg://{username}:{password}@{host}:{port}/{database}"
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

    This is a session scoped fixture therefore
    it will only be created once before all the tests
    :return client:
    """
    with TestClient(app=app) as client:
        yield client
