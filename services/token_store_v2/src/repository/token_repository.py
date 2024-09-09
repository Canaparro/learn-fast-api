from typing import Annotated, List
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..persistence.database import database_session_factory
from ...src.persistence.models import TokenModel
from ...src.repository.protocol import TokenRepositoryProtocol
from ...src.repository.transformers import (
    from_permission_dto_to_model,
    from_token_dto_to_model,
    token_model_to_dto,
)
from services.token_store_v2.src.service.dto import Token


class TokenRepository:
    def __init__(
        self, session: Annotated[AsyncSession, Depends(database_session_factory)]
    ):
        self.session = session

    async def find_all(self, client_id: str | None) -> List[Token]:
        query = select(TokenModel)
        if client_id:
            query = query.where(TokenModel.client_id == client_id)
        tokens = await self.session.scalars(query)
        return [token_model_to_dto(token) for token in tokens]

    async def create_token(self, token: Token) -> UUID:
        token.id = None
        token_entity = from_token_dto_to_model(token)
        self.session.add(token_entity)
        permissions = from_permission_dto_to_model(token.permissions, token_entity)
        token_entity.permissions.extend(permissions)
        token_id = token_entity.id
        await self.session.commit()
        return token_id

    async def update_token(self, token_id: UUID, token: Token) -> bool:
        token_entity = await self.session.get(TokenModel, token_id)
        if not token_entity:
            raise TokenNotFoundError("Token not found")
        token_entity.instance_id = token.instance_id
        token_entity.client_id = token.client_id
        token_entity.account_id = token.account_id
        token_entity.token = token.token
        token_entity.expire_at = token.expire_at
        token_entity.permissions = from_permission_dto_to_model(
            token.permissions, token_entity
        )
        await self.session.commit()
        return True


class TokenNotFoundError(Exception):
    pass


TokenRepositoryDep = Annotated[TokenRepositoryProtocol, Depends(TokenRepository)]
