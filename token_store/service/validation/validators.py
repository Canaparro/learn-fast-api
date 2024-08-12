import time
from datetime import datetime, timedelta
from typing import Annotated, Protocol

from fastapi import Depends

from token_store.service.dto import Token


class TokenValidationError(Exception):
    pass


class ValidatorProtocol(Protocol):

    @staticmethod
    def validate(token: Token):
        ...


class FacebookValidator:

    @staticmethod
    def validate(token: Token):
        one_month_future_timestamp = int((datetime.now() + timedelta(days=30)).timestamp())
        if token.expire_at < one_month_future_timestamp:
            raise TokenValidationError('Token expiration must be at least a month in the future')


class TwitterValidator:

    @staticmethod
    def validate(token: Token):
        if token.expire_at != -1:
            raise TokenValidationError('Twitter tokens must have an expiration date of -1')


def validator_factory(social_network: str) -> ValidatorProtocol:
    validator_map = {
        'facebook': FacebookValidator,
        'twitter': TwitterValidator,
    }
    validator = validator_map.get(social_network, None)
    if validator:
        return validator()
    else:
        raise ValueError(f'Validator for {social_network} is not implemented')


TokenValidatorDep = Annotated[ValidatorProtocol, Depends(validator_factory)]
