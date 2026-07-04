from app import AuthService
import pytest
import jwt

class TestGenerateToken:
    def test_generateTokenSuccessfull(self, authService):
        token = authService._generateToken(["FULL"])
        assert token != ""
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        assert payload["FULL"] is True
        assert payload["ANONYMIZED"] is False
        assert payload["AGGREGATED"] is False
        assert payload["PARTIAL"] is False

    def test_generateTokenWithoutPermissions(self, authService):
        token = authService._generateToken([])
        assert token == ""
    
    @pytest.mark.parametrize("valor_invalido", [
        "string",
        123,
        {"a": 1},
        None,
    ])
    def test_generate_token_rejeita_tipos_invalidos(self, authService, valor_invalido):
        with pytest.raises(TypeError):
            authService._generateToken(permissions=valor_invalido)