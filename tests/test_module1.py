from token_store.service.module1 import add


def test_add():
    assert add(1, 2) == 3
