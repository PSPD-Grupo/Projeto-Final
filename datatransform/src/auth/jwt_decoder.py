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
    pass

def decode_token(token: str, secret: str) -> TokenClaims:
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError as e:
        raise InvalidTokenError("Token expirado") from e
    except jwt.InvalidTokenError as e:
        raise InvalidTokenError("Token expirado") from e
    
    return TokenClaims(
        full=payload.get("FULL", False),
        partial=payload.get("PARTIAL", False),
        anonymized=payload.get("ANONYMIZED", False),
        aggregated=payload.get("AGGREGATED", False),
        exp=payload.get("exp", 0),
    )