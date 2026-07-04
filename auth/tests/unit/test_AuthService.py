from app import AuthService
import pytest
import jwt
import time 

class TestGenerateAccessToken:
    def test_generateAccessToken_Successfull(self, auth_service):
        token, expires_at = auth_service._generateAccessToken(["FULL"])
        assert token != ""
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        assert payload["FULL"] is True
        assert payload["ANONYMIZED"] is False
        assert payload["AGGREGATED"] is False
        assert payload["PARTIAL"] is False

    def test_generateAccessToken_WithoutPermissions(self, auth_service):
        token, expires_at = auth_service._generateAccessToken([])
        assert token == ""
    
    @pytest.mark.parametrize("valor_invalido", [
        "string",
        123,
        {"a": 1},
        None,
    ])
    def test_generateAccessToken_rejeita_tipos_invalidos(self, auth_service, valor_invalido):
        with pytest.raises(TypeError):
            auth_service._generateAccessToken(permissions=valor_invalido)
        