from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from token_store.persistence.database import get_session
from token_store.persistence.models import TokenModel
from token_store.service.dto import TokenDTO
from token_store.service.transformers import from_token_dto_to_model, token_model_to_dto, from_permission_dto_to_model
from token_store.service.validation.facebook_validator import FacebookValidatorDep


class TokenService:

    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)], validator: FacebookValidatorDep):
        self.session = session
        self.validator = validator

    async def find_all(self, client_id: str | None) -> list[TokenDTO]:
        query = select(TokenModel).options(selectinload(TokenModel.permissions))

        if client_id:
            query = query.where(client_id=client_id)
        tokens = await self.session.execute(query)
        tokens = tokens.scalars().all()

        return [token_model_to_dto(token) for token in tokens]

    async def create_token(self, token: TokenDTO) -> TokenDTO:
        token.id = None

        self.validator.validate(token)

        token_entity = from_token_dto_to_model(token)

        self.session.add(token_entity)

        permissions = from_permission_dto_to_model(token.permissions, token_entity)
        token_entity.permissions.extend(permissions)

        entity_id = token_entity.id

        await self.session.commit()

        return entity_id


TokenServiceDep = Annotated[TokenService, Depends(TokenService)]
