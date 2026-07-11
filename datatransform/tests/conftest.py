import pytest

TEST_SECRET = "test-secret"
TEST_SALT = "test-salt"


@pytest.fixture
def jwt_secret():
    return TEST_SECRET


@pytest.fixture
def pseudonymize_salt():
    return TEST_SALT