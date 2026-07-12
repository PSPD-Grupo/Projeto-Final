import pytest
from auth.jwt_decoder import decode_token, InvalidTokenError, TokenExpiredError, TokenMalformedError
from tests.helpers.token_factory import make_token
from tests.conftest import TEST_SECRET


def test_decodifica_token_valido():
    token = make_token(full=True)
    claims = decode_token(token, TEST_SECRET)
    assert claims.full is True


def test_token_expirado_gera_erro():
    token = make_token(full=True, expired=True)
    with pytest.raises(InvalidTokenError):
        decode_token(token, TEST_SECRET)


def test_secret_errado_gera_erro():
    token = make_token(full=True)
    with pytest.raises(InvalidTokenError):
        decode_token(token, "another-wrong-secret-32-bytes-xx")

def test_token_expirado_gera_token_expired_error():
    token = make_token(full=True, expired=True)
    with pytest.raises(TokenExpiredError):
        decode_token(token, TEST_SECRET)


def test_secret_errado_gera_token_malformed_error():
    token = make_token(full=True)
    with pytest.raises(TokenMalformedError):
        decode_token(token, "another-wrong-secret-32-bytes-xx")