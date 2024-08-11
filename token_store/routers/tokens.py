from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query, HTTPException
from ..service.dto import TokenDTO
from ..service.token_service import TokenServiceDep

router = APIRouter(
    prefix="/platform/facebook/tokens",
    tags=["Tokens"],
    responses={404: {"description": "Token not found"}},
)


@router.get("/",
            summary="Get all tokens",
            description="Get all tokens for a social media platform.")
async def get_all_tokens(token_service: TokenServiceDep, client_id: Annotated[str, Query()] = None) -> list[TokenDTO]:
    return await token_service.find_all(client_id=client_id)


@router.post("/", status_code=HTTPStatus.CREATED)
async def create_token(token: TokenDTO, token_service: TokenServiceDep) -> UUID:
    return await token_service.create_token(token)


@router.put("/{token_id}")
async def update_token(token_id: UUID, token: TokenDTO, token_service: TokenServiceDep) -> bool:
    if not token_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="whaaat")
    return await token_service.update_token(token_id, token)


@router.get("/a_deprecated_endpoint", deprecated=True)
async def get_all_tokens() -> list[TokenDTO]:
    return [TokenDTO()]
