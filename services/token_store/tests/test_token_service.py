import uuid

import emoji
import pytest

from .utils import token_mother
from ..src.service.token_service import TokenService
from ..src.service.validation.validators import FacebookValidator, TokenValidationError, TwitterValidator


class FakeTokenRepository:
    async def find_all(self, client_id):
        return []

    async def create_token(self, token):
        return uuid.uuid4()

    async def update_token(self, token_id, token):
        return True


async def test_facebook_token_is_valid():
    token_service = TokenService(FakeTokenRepository(), FacebookValidator())
    token = token_mother.get_facebook_valid_token()

    token_id = await token_service.create_token(token)

    assert token_id is not None


async def test_facebook_token_is_invalid():
    token_service = TokenService(FakeTokenRepository(), FacebookValidator())
    token = token_mother.get_facebook_invalid_token()

    with pytest.raises(TokenValidationError) as e:
        await token_service.create_token(token)

    assert str(e.value) == emoji.emojize(":warning: Token expiration must be at least a month in the future :warning:")


async def test_twitter_token_is_valid():
    token_service = TokenService(FakeTokenRepository(), TwitterValidator())
    token = token_mother.get_valid_twitter_token()

    token_id = await token_service.create_token(token)

    assert token_id is not None


async def test_twitter_token_is_invalid():
    token_service = TokenService(FakeTokenRepository(), TwitterValidator())
    token = token_mother.get_invalid_twitter_token()

    with pytest.raises(TokenValidationError) as e:
        await token_service.create_token(token)

    assert str(e.value) == "Twitter tokens must have an expiration date of -1"
