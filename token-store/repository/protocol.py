from typing import List, Protocol
from uuid import UUID

from src.service.dto import Token


class TokenRepositoryProtocol(Protocol):
    async def find_all(self, client_id: str | None) -> List[Token]: ...

    async def create_token(self, token: Token) -> UUID: ...

    async def update_token(self, token_id: UUID, token: Token) -> bool: ...
