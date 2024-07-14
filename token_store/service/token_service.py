from typing import Annotated

from fastapi import Depends
from tortoise.transactions import in_transaction

from .transformers import token_model_to_dto, from_token_dto_to_model
from ..persistence.models import TokenModel, PermissionModel
from .dto import TokenDTO
from .validation.facebook_validator import FacebookValidatorDep


class TokenService:

    def __init__(self, validator: FacebookValidatorDep):
        self.validator = validator

    @staticmethod
    async def find_all(client_id: str | None) -> list[TokenDTO]:
        query_model = TokenModel.all()

        if client_id:
            query_model = query_model.filter(client_id=client_id)

        tokens = await query_model

        for token in tokens:
            await token.fetch_related("permissions")

        return [token_model_to_dto(token) for token in tokens]

    async def create_token(self, token: TokenDTO) -> TokenDTO:
        self.validator.validate(token)

        token.id = None

        token_entity = from_token_dto_to_model(token)

        permission_entities = [
            PermissionModel(name=permission) for permission in token.permissions
        ]

        async with in_transaction():
            await token_entity.save()
            for permission_entity in permission_entities:
                await permission_entity.save()
                await token_entity.permissions.add(permission_entity)
            return token_entity.id


TokenServiceDep = Annotated[TokenService, Depends(TokenService)]
