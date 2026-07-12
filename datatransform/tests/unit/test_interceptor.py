from auth.interceptor import JwtAuthInterceptor

def test_extract_token_encontra_bearer():
    metadata = [("authorization", "Bearer abc123")]
    assert JwtAuthInterceptor._extract_token(metadata) == "abc123"


def test_extract_token_retorna_none_sem_header():
    assert JwtAuthInterceptor._extract_token([]) is None


def test_extract_token_ignora_esquema_diferente():
    metadata = [("authorization", "Basic abc123")]
    assert JwtAuthInterceptor._extract_token(metadata) is None