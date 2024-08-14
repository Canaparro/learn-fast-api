from datetime import datetime, timedelta

from token_store.service.dto import Token


def get_facebook_valid_token():
    return Token(
        token="test_token",
        instance_id="test_instance_id",
        client_id="test_client_id",
        account_id="test_account_id",
        expire_at=int((datetime.now() + timedelta(days=31)).timestamp()),
        permissions=["READ", "WRITE"],
    )


def get_facebook_invalid_token():
    return Token(
        token="test_token",
        instance_id="test_instance_id",
        client_id="test_client_id",
        account_id="test_account_id",
        expire_at=int(datetime.now().timestamp()),
        permissions=["READ", "WRITE"],
    )


def get_valid_twitter_token():
    return Token(
        token="test_token",
        instance_id="test_instance_id",
        client_id="test_client_id",
        account_id="test_account_id",
        expire_at=-1,
        permissions=["READ", "WRITE"],
    )


def get_invalid_twitter_token():
    return Token(
        token="test_token",
        instance_id="test_instance_id",
        client_id="test_client_id",
        account_id="test_account_id",
        expire_at=int(datetime.now().timestamp()),
        permissions=["READ", "WRITE"],
    )
