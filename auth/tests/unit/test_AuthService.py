from app.Memory import SECRET 
from app.Memory import UserNotFoundError
import pytest
import jwt
import time 

class TestGenerateAccessToken:
    def test_generateAccessToken_Successfull(self, auth_service):
        token, expires_at = auth_service._generateAccessToken(["FULL"])
        assert token != ""
        assert expires_at > int(time.time())+(10*60)
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        assert payload["FULL"] is True
        assert payload["ANONYMIZED"] is False
        assert payload["AGGREGATED"] is False
        assert payload["PARTIAL"] is False
        assert payload["exp"] > int(time.time())+(10*60)
        

    def test_generateAccessToken_WithoutPermissions(self, auth_service):
        token, expires_at = auth_service._generateAccessToken([])
        assert token == ""
        assert expires_at == 0
    
    @pytest.mark.parametrize("valor_invalido", [
        "string",
        123,
        {"a": 1},
        None,
    ])
    def test_generateAccessToken_rejeita_tipos_invalidos(self, auth_service, valor_invalido):
        with pytest.raises(TypeError):
            auth_service._generateAccessToken(valor_invalido)

class TestGenerateRefreshToken:
    def test_GenerateRefreshToken_Success(self, auth_service):
        auth_service._repo.login("user")
        token, expires_at = auth_service._generateRefreshToken("user")
        assert token != ""
        assert expires_at > int(time.time())+(60*60*23)

        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        assert payload["username"] == "user"
        assert payload["exp"] > int(time.time())+(60*60*23)
    
    def test_GenerateRefreshToken_Fail_UserNoExists(self, auth_service):
        with pytest.raises(UserNotFoundError):
            token, expires_at = auth_service._generateRefreshToken("")
    
    def test_GenerateRefreshToken_Fail_UserNotLogded_in(self, auth_service):
        with pytest.raises(PermissionError):
            token, expires_at = auth_service._generateRefreshToken("user")


