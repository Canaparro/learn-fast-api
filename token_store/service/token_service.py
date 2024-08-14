from typing import Annotated
from uuid import UUID

from fastapi import Depends

from token_store.repository.token_repository import TokenRepositoryDep
from token_store.service.dto import Token
from token_store.service.validation.validators import TokenValidatorDep


class TokenService:
    def __init__(self, repository: TokenRepositoryDep, validator: TokenValidatorDep):
        self.repository = repository
        self.validator = validator

    async def find_all(self, client_id: str | None) -> list[Token]:
        return await self.repository.find_all(client_id)

    async def create_token(self, token: Token) -> UUID:
        self.validator.validate(token)
        return await self.repository.create_token(token)

    async def update_token(self, token_id: UUID, token: Token) -> bool:
        self.validator.validate(token)
        return await self.repository.update_token(token_id, token)


TokenServiceDep = Annotated[TokenService, Depends(TokenService)]
