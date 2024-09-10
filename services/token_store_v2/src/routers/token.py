from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query

from ..service.dto import Token
from ..service.token_service import TokenServiceDep

router = APIRouter(
    prefix="/platform",
    tags=["Tokens"],
    responses={404: {"description": "Token not found"}},
)


@router.get(
    "/{social_network}/tokens",
    summary="Get all tokens",
    description="Get all tokens for a social media platform.",
)
async def get_all_tokens(
    token_service: TokenServiceDep, client_id: Annotated[str | None, Query()] = None
) -> list[Token]:
    return await token_service.find_all(client_id=client_id)


@router.post("/{social_network}/tokens", status_code=HTTPStatus.CREATED)
async def create_token(token: Token, token_service: TokenServiceDep) -> UUID:
    return await token_service.create_token(token)


@router.put("/{social_network}/tokens/{token_id}")
async def update_token(
    token_id: UUID, token: Token, token_service: TokenServiceDep
) -> bool:
    if token_id == "exception":
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="whaaat")
    return await token_service.update_token(token_id, token)


@router.get("/a_deprecated_endpoint", deprecated=True)
async def get_all_tokens_deprecated() -> list[Token]:
    return []
