import time
from unittest import mock
from uuid import UUID

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import delete

from token_store.app import app
from token_store.persistence.database import SessionLocal
from token_store.persistence.models import TokenModel, PermissionModel
from token_store.service.dto import TokenDTO, PermissionsEnum
from token_store.service.transformers import from_token_dto_to_model

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from token_store.persistence.models import Base


@pytest_asyncio.fixture(scope="session")
def engine():
    engine = create_async_engine(
        "sqlite:///:memory:"
    )
    yield engine
    engine.sync_engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def create(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
async def session(engine, create):
    async with AsyncSession(engine) as session:
        yield session


@pytest.fixture
async def client():
    async with AsyncClient(app=app) as client:
        yield client


@pytest.fixture
async def clear_db(session):
    await session.execute(delete(TokenModel))
    await session.execute(delete(PermissionModel))
    await session.commit()


@pytest.fixture
async def create_two_tokens() -> list[TokenModel]:
    tokens = []
    for i in range(1, 3):
        token = TokenDTO(
            token=f"test_token_{i}",
            instance_id=f"test_instance_id_{i}",
            client_id=f"test_client_id_{i}",
            account_id=f"test_account_id_{i}",
            expire_at=int(time.time()),
            permissions=[PermissionsEnum.read, PermissionsEnum.write],
        )
        token_entity = from_token_dto_to_model(token)
        permission_entities = [
            PermissionModel(name=permission) for permission in token.permissions
        ]

        session = SessionLocal()
        session.add_all([token_entity, *permission_entities])
        tokens.append(token_entity)
        await session.commit()
    return tokens


async def test_get_token_empty_response(client, clear_db):
    response = await client.get("/platform/facebook/tokens/")
    assert response.status_code == 200
    assert response.json() == []


async def test_get_token_two_tokens(client, create_two_tokens):
    response = client.get("/platform/facebook/tokens")
    assert response.status_code == 200
    assert response.json()
    assert response.json() == [
        {
            'account_id': 'test_account_id_1',
            'client_id': 'test_client_id_1',
            'expire_at': mock.ANY,
            'id': mock.ANY,
            'instance_id': 'test_instance_id_1',
            'permissions': ['read', 'write'],
            'token': 'test_token_1'
        },
        {
            'account_id': 'test_account_id_2',
            'client_id': 'test_client_id_2',
            'expire_at': mock.ANY,
            'id': mock.ANY,
            'instance_id': 'test_instance_id_2',
            'permissions': ['read', 'write'],
            'token': 'test_token_2'
        }
    ]


@pytest.mark.asyncio
async def test_create_token(client: AsyncClient):
    response = await client.post("/platform/facebook/tokens/", json={
        "token": "test_token",
        "instance_id": "test_instance_id",
        "client_id": "test_client_id",
        "account_id": "test_account_id",
        "expire_at": int(time.time()),
        "permissions": ["read", "write"],
    })
    assert response.status_code == 201
    assert UUID(response.json(), version=4)
