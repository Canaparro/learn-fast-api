import time
from unittest import mock
from uuid import UUID

from sqlalchemy import delete
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from token_store.persistence.models import TokenModel, TokenPermissionModel
from token_store.service.dto import TokenDTO, PermissionsEnum
from token_store.service.transformers import from_token_dto_to_model, from_permission_dto_to_model

import pytest


@pytest.fixture
def clear_db(session: Session):
    """
    Clear the database
    :param session:
    :return:
    """
    session.execute(delete(TokenPermissionModel))
    session.execute(delete(TokenModel))
    session.commit()


@pytest.fixture
def create_two_tokens(session: Session) -> list[TokenModel]:
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

        session.add(token_entity)

        permissions = from_permission_dto_to_model(token.permissions, token_entity)
        token_entity.permissions.extend(permissions)
        tokens.append(token_entity)
        session.commit()
    return tokens


def test_get_token_empty_response(client: TestClient, clear_db):
    response = client.get("/platform/facebook/tokens/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_token_two_tokens(client: TestClient, create_two_tokens):
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


def test_create_token(client: TestClient):
    response = client.post("/platform/facebook/tokens/", json={
        "token": "test_token",
        "instance_id": "test_instance_id",
        "client_id": "test_client_id",
        "account_id": "test_account_id",
        "expire_at": int(time.time()),
        "permissions": ["read", "write"],
    })
    assert response.status_code == 201
    assert UUID(response.json(), version=4)


def test_update_token(client: TestClient, create_two_tokens, session: Session):
    token = create_two_tokens[0]
    response = client.put(f"/platform/facebook/tokens/{token.id}", json={
        "token": "test_token_updated",
        "instance_id": "test_instance_id_updated",
        "client_id": "test_client_id_updated",
        "account_id": "test_account_id_updated",
        "expire_at": int(time.time()),
        "permissions": ["delete"],
    })
    assert response.status_code == 200
    assert response.json() is True

    # Session was created before the update so it's not aware of the changes, so we need to refresh the internal cache
    session.refresh(token)

    updated_token = session.get(TokenModel, token.id)
    assert updated_token.token == "test_token_updated"
    assert updated_token.instance_id == "test_instance_id_updated"
    assert updated_token.client_id == "test_client_id_updated"
    assert updated_token.account_id == "test_account_id_updated"
    assert [permission.name for permission in updated_token.permissions] == ["delete"]
