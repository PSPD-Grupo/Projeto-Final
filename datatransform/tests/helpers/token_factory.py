import time
import jwt

from tests.conftest import TEST_SECRET


def make_token(full=False, partial=False, anonymized=False, aggregated=False, expired=False):
    exp = int(time.time()) - 60 if expired else int(time.time()) + 3600
    payload = {
        "FULL": full, "PARTIAL": partial,
        "ANONYMIZED": anonymized, "AGGREGATED": aggregated,
        "exp": exp,
    }
    return jwt.encode(payload, TEST_SECRET, algorithm="HS256")