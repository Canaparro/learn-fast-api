from typing import Annotated

from fastapi import Depends


class FacebookValidator:

    @staticmethod
    def validate(token: str):
        if not token:
            raise ValueError('Token is required')


def create_facebook_validator():
    return FacebookValidator()


FacebookValidatorDep = Annotated[FacebookValidator, Depends(create_facebook_validator)]

