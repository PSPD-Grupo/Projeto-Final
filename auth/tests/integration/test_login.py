"""
Testes de integração do RPC Login.

Cobrem o caminho feliz e os principais casos de erro que a API
precisa garantir em contrato (status codes corretos, mensagens, etc.)
"""
import grpc, jwt
import pytest , time
from app.AuthService import SECRET

from proto import auth_pb2


class TestLoginSucesso:
    def test_credenciais_validas_retorna_tokens(self, grpc_stub, real_user):
        response = grpc_stub.Login(
            auth_pb2.Credentials(username=real_user["username"], password=real_user["password"])
        )
 
        assert response.access_token != ""
        assert response.refresh_token != ""
        assert response.expires_at > 0


class TestLoginFalha:
    def test_senha_incorreta_retorna_unauthenticated(self, grpc_stub, real_user):
        with pytest.raises(grpc.RpcError) as exc_info:
            grpc_stub.Login(auth_pb2.Credentials(username=real_user["username"], password="errada"))
 
        assert exc_info.value.code() == grpc.StatusCode.UNAUTHENTICATED


    def test_username_vazio_retorna_invalid_argument(self, grpc_stub, real_user):
        with pytest.raises(grpc.RpcError) as exc_info:
            grpc_stub.Login(auth_pb2.Credentials(username="", password=real_user["password"]))
 
        assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT


class TestLogout:
    def test_logout_invalida_refresh_token(self, grpc_stub, real_user):
        login = grpc_stub.Login(
            auth_pb2.Credentials(username=real_user["username"], password=real_user["password"])
        )
 
        grpc_stub.Logout(auth_pb2.LogoutRequest(refresh_token=login.refresh_token))
 
        # depois do logout, o mesmo refresh_token não deve mais funcionar
        with pytest.raises(grpc.RpcError) as exc_info:
            grpc_stub.RefreshToken(
                auth_pb2.RefreshRequest(refresh_token=login.refresh_token)
            )
 
        assert exc_info.value.code() == grpc.StatusCode.UNAUTHENTICATED
 
    def test_logout_de_token_ja_invalido_nao_quebra(self, grpc_stub):
        with pytest.raises(grpc.RpcError) as exec_er:
            response = grpc_stub.Logout(
                auth_pb2.LogoutRequest(refresh_token="token-inexistente")
            )
        assert exec_er.value.code() == grpc.StatusCode.INVALID_ARGUMENT
        assert exec_er.value.details() == "token inválido"


class TestGenerateRefreshToken:
    def test_generateRefreshToken_success(self, grpc_stub, real_user):
        login = grpc_stub.Login(
            auth_pb2.Credentials(username=real_user["username"], password=real_user["password"])
        )
        assert login.access_token != ""
        payload = jwt.decode(login.refresh_token, SECRET, algorithms=["HS256"])
        assert payload.get("username") == real_user["username"]
        assert payload.get("exp") > int(time.time()) + (60*60*23)
        
        refreshed = grpc_stub.RefreshToken(
            auth_pb2.RefreshRequest(refresh_token=login.refresh_token)
        )
        assert refreshed.access_token != ""
        payload = jwt.decode(refreshed.access_token, SECRET, algorithms=["HS256"])
        assert payload["FULL"] is True
        assert payload["ANONYMIZED"] is False
        assert payload["AGGREGATED"] is False
        assert payload["PARTIAL"] is False
        assert payload["exp"] > int(time.time())+(10*60)
    
    def test_generateRefreshToken_Fail_Loged_out(self, grpc_stub, real_user):
        login = grpc_stub.Login(
            auth_pb2.Credentials(username=real_user["username"], password=real_user["password"])
        )

        grpc_stub.Logout(auth_pb2.LogoutRequest(refresh_token=login.refresh_token))
        
        with pytest.raises(grpc.RpcError) as exec_er:
            refreshed = grpc_stub.RefreshToken(
                auth_pb2.RefreshRequest(refresh_token=login.refresh_token)
            )
        assert exec_er.value.code() == grpc.StatusCode.UNAUTHENTICATED

class TestFluxoCompleto:
    def test_login_refresh_logout_refresh_novamente(self, grpc_stub, real_user):
        """
        Simula o ciclo de vida real de uma sessão:
        login -> usa refresh -> desloga -> refresh deve falhar.
        """
        login = grpc_stub.Login(
            auth_pb2.Credentials(username=real_user["username"], password=real_user["password"])
        )
        assert login.access_token != ""
 
        refreshed = grpc_stub.RefreshToken(
            auth_pb2.RefreshRequest(refresh_token=login.refresh_token)
        )
        assert refreshed.access_token != ""
 
        grpc_stub.Logout(auth_pb2.LogoutRequest(refresh_token=login.refresh_token))
 
        with pytest.raises(grpc.RpcError) as exc_info:
            grpc_stub.RefreshToken(
                auth_pb2.RefreshRequest(refresh_token=login.refresh_token)
            )
        assert exc_info.value.code() == grpc.StatusCode.UNAUTHENTICATED

