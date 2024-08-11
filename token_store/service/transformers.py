from token_store.persistence.models import TokenModel, TokenPermissionModel
from token_store.service.dto import TokenDTO, PermissionsEnum


def from_token_dto_to_model(token: TokenDTO) -> TokenModel:
    token_entity = TokenModel(
        instance_id=token.instance_id,
        client_id=token.client_id,
        account_id=token.account_id,
        token=token.token,
        expire_at=token.expire_at,
        permissions=[]
    )
    if token.id:
        token_entity.id = token.id

    return token_entity


def from_permission_dto_to_model(permissions: list[PermissionsEnum], token_entity):
    permissions = [
        TokenPermissionModel(name=permission, token=token_entity, token_id=token_entity.id)
        for permission in permissions
    ]
    return permissions


def token_model_to_dto(token: TokenModel) -> TokenDTO:
    tokens = TokenDTO(
        id=token.id,
        instance_id=token.instance_id,
        client_id=token.client_id,
        account_id=token.account_id,
        token=token.token,
        expire_at=token.expire_at,
        permissions=[PermissionsEnum(permission.name) for permission in token.permissions]
    )

    return tokens

