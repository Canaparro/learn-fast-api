from token_store.persistence.models import TokenModel
from token_store.service.dto import TokenDTO


def from_token_dto_to_model(token: TokenDTO) -> TokenModel:
    token_entity = TokenModel(
        instance_id=token.instance_id,
        client_id=token.client_id,
        account_id=token.account_id,
        token=token.token,
        expire_at=token.expire_at,
    )
    if token.id:
        token_entity.id = token.id

    return token_entity


def token_model_to_dto(token: TokenModel) -> TokenDTO:
    tokens = TokenDTO(
        id=token.id,
        instance_id=token.instance_id,
        client_id=token.client_id,
        account_id=token.account_id,
        token=token.token,
        expire_at=token.expire_at,
        permissions=[permission.name for permission in token.permissions]
    )

    return tokens

