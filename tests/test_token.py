import time
from unittest import mock
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from token_store.app import app
from token_store.persistence.models import TokenModel, PermissionModel


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
async def clear_db():
    await TokenModel.all().delete()
    await PermissionModel.all().delete()


@pytest.fixture
async def create_two_tokens() -> list[TokenModel]:
    tokens = []
    for i in range(1, 3):
        token = await TokenModel.create(
            token=f"test_token_{i}",
            instance_id=f"test_instance_id_{i}",
            client_id=f"test_client_id_{i}",
            account_id=f"test_account_id_{i}",
            expire_at=int(time.time()),
        )
        permission_read = await PermissionModel.create(name="read")
        permission_write = await PermissionModel.create(name="write")
        await token.permissions.add(permission_read)
        await token.permissions.add(permission_write)
        tokens.append(token)
    return tokens


async def test_get_token_empty_response(client, clear_db):
    response = client.get("/platform/facebook/tokens")
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


def test_create_token(client):
    response = client.post("/platform/facebook/tokens", json={
        "token": "test_token",
        "instance_id": "test_instance_id",
        "client_id": "test_client_id",
        "account_id": "test_account_id",
        "expire_at": int(time.time()),
        "permissions": ["read", "write"],
    })
    assert response.status_code == 201
    assert UUID(response.json(), version=4)
