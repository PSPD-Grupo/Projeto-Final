"""
Testes de integração do RPC Login.

Cobrem o caminho feliz e os principais casos de erro que a API
precisa garantir em contrato (status codes corretos, mensagens, etc.)
"""
import grpc
import pytest

from proto import auth_pb2


class TestLoginSucesso:
    def test_credenciais_validas_retorna_tokens(self, grpc_stub):
        response = grpc_stub.Login(
            auth_pb2.Credentials(username="user", password="senha123")
        )
 
        assert response.acess_token != ""
        assert response.refresh_token != ""
        assert response.expires_at > 0


class TestLoginFalha:
    def test_senha_incorreta_retorna_unauthenticated(self, grpc_stub):
        with pytest.raises(grpc.RpcError) as exc_info:
            grpc_stub.Login(auth_pb2.Credentials(username="user", password="errada"))
 
        assert exc_info.value.code() == grpc.StatusCode.UNAUTHENTICATED


    def test_username_vazio_retorna_invalid_argument(self, grpc_stub):
        with pytest.raises(grpc.RpcError) as exc_info:
            grpc_stub.Login(auth_pb2.Credentials(username="", password="senha123"))
 
        assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT


class TestLogout:
    def test_logout_invalida_refresh_token(self, grpc_stub):
        login = grpc_stub.Login(
            auth_pb2.Credentials(username="user", password="senha123")
        )
 
        grpc_stub.Logout(auth_pb2.LogoutRequest(refresh_token=login.refresh_token))
 
        # depois do logout, o mesmo refresh_token não deve mais funcionar
        with pytest.raises(grpc.RpcError) as exc_info:
            grpc_stub.RefreshToken(
                auth_pb2.RefreshRequest(refresh_token=login.refresh_token)
            )
 
        assert exc_info.value.code() == grpc.StatusCode.UNAUTHENTICATED
 
    def test_logout_de_token_ja_invalido_nao_quebra(self, grpc_stub):
        # logout deve ser idempotente: chamar duas vezes não deve dar erro
        response = grpc_stub.Logout(
            auth_pb2.LogoutRequest(refresh_token="token-inexistente")
        )
        assert response == auth_pb2.LogoutResponse()


class TestFluxoCompleto:
    def test_login_refresh_logout_refresh_novamente(self, grpc_stub):
        """
        Simula o ciclo de vida real de uma sessão:
        login -> usa refresh -> desloga -> refresh deve falhar.
        """
        login = grpc_stub.Login(
            auth_pb2.Credentials(username="user", password="senha123")
        )
        assert login.acess_token != ""
 
        refreshed = grpc_stub.RefreshToken(
            auth_pb2.RefreshRequest(refresh_token=login.refresh_token)
        )
        assert refreshed.acess_token != ""
 
        grpc_stub.Logout(auth_pb2.LogoutRequest(refresh_token=login.refresh_token))
 
        with pytest.raises(grpc.RpcError) as exc_info:
            grpc_stub.RefreshToken(
                auth_pb2.RefreshRequest(refresh_token=login.refresh_token)
            )
        assert exc_info.value.code() == grpc.StatusCode.UNAUTHENTICATED

