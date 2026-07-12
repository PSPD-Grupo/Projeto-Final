from enum import Enum
from auth.jwt_decoder import TokenClaims


class AccessLevel(str, Enum):
    FULL = "FULL"
    PARTIAL = "PARTIAL"
    ANONYMIZED = "ANONYMIZED"
    AGGREGATED = "AGGREGATED"


class NoAccessLevelError(Exception):
    pass


_PRIORITY = [
    (lambda c: c.full, AccessLevel.FULL),
    (lambda c: c.partial, AccessLevel.PARTIAL),
    (lambda c: c.anonymized, AccessLevel.ANONYMIZED),
    (lambda c: c.aggregated, AccessLevel.AGGREGATED),
]


def resolve_access_level(claims: TokenClaims) -> AccessLevel:
    for check, level in _PRIORITY:
        if check(claims):
            return level
    raise NoAccessLevelError("token não concede nenhum nível de acesso")