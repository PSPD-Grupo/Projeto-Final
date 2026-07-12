import jwt
from dataclasses import dataclass


@dataclass
class TokenClaims:
    full: bool
    partial: bool
    anonymized: bool
    aggregated: bool
    exp: int


class InvalidTokenError(Exception):
    """Classe base — qualquer problema de decodificação do token."""
    pass


class TokenExpiredError(InvalidTokenError):
    """O token é bem formado e a assinatura é válida, mas o campo exp já passou."""
    pass


class TokenMalformedError(InvalidTokenError):
    """Assinatura inválida, formato quebrado, algoritmo errado, etc."""
    pass


def decode_token(token: str, secret: str) -> TokenClaims:
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError as e:
        raise TokenExpiredError("token expirado") from e
    except jwt.InvalidTokenError as e:
        raise TokenMalformedError("token inválido") from e

    return TokenClaims(
        full=payload.get("FULL", False),
        partial=payload.get("PARTIAL", False),
        anonymized=payload.get("ANONYMIZED", False),
        aggregated=payload.get("AGGREGATED", False),
        exp=payload.get("exp", 0),
    )