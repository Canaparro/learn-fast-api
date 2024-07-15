from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from .transformers import token_model_to_dto, from_token_dto_to_model
from ..persistence.database import get_session
from ..persistence.models import TokenModel, PermissionModel
from .dto import TokenDTO
from .validation.facebook_validator import FacebookValidatorDep


class TokenService:

    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)], validator: FacebookValidatorDep):
        self.session = session
        self.validator = validator

    async def find_all(self, client_id: str | None) -> list[TokenDTO]:
        query = select(TokenModel)

        if client_id:
            query = query.where(client_id=client_id)
        tokens = await self.session.execute(query)

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

        self.session.add_all([token_entity, *permission_entities])

        await self.session.commit()

        return token_entity.id


TokenServiceDep = Annotated[TokenService, Depends(TokenService)]
