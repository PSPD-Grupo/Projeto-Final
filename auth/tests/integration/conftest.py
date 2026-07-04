"""
Fixtures compartilhadas para toda a suite de testes.

Este arquivo é carregado automaticamente pelo pytest e disponibiliza
as fixtures `grpc_server`, `grpc_channel` e `grpc_stub` para qualquer
teste dentro de tests/, sem precisar importar nada.
"""
import grpc
import pytest
from concurrent import futures

from proto import auth_pb2_grpc
from app import AuthService


# ---------------------------------------------------------------------------
# Fixture de "fake" dependências (banco, cache, etc.)
# Troque isso pela sua implementação real de repositório/DB de teste.
# ---------------------------------------------------------------------------
@pytest.fixture(scope="function")
def user_repository():
    """
    Repositório de usuários isolado por teste.

    Se o AuthServicer depender de um banco real, aqui é o lugar de
    subir uma conexão de teste (ex: sqlite em memória, container
    Postgres via testcontainers, etc.) e popular dados fixos.
    """
    from app.AuthService import InMemoryUserRepository

    repo = InMemoryUserRepository()
    repo.create_user(username="user", password="senha123")
    yield repo
    repo.clear()


# ---------------------------------------------------------------------------
# Fixtures de infraestrutura gRPC
# ---------------------------------------------------------------------------
@pytest.fixture(scope="function")
def grpc_server(user_repository):
    """Sobe um servidor gRPC real numa porta livre, isolado por teste."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    servicer = AuthService(user_repository=user_repository)
    auth_pb2_grpc.add_AuthServicer_to_server(servicer, server)

    port = server.add_insecure_port("localhost:0")
    server.start()

    yield f"localhost:{port}"

    server.stop(grace=None)


@pytest.fixture(scope="function")
def grpc_channel(grpc_server):
    """Canal gRPC conectado ao servidor de teste."""
    channel = grpc.insecure_channel(grpc_server)
    try:
        grpc.channel_ready_future(channel).result(timeout=5)
    except grpc.FutureTimeoutError:
        pytest.fail("Servidor gRPC de teste não ficou pronto a tempo")

    yield channel
    channel.close()


@pytest.fixture(scope="function")
def grpc_stub(grpc_channel):
    """Stub pronto para uso nos testes."""
    return auth_pb2_grpc.AuthStub(grpc_channel)


# ---------------------------------------------------------------------------
# Helper de metadata (ex: para testes que exigem token/autenticação)
# ---------------------------------------------------------------------------
@pytest.fixture
def auth_metadata():
    def _make(token: str):
        return (("authorization", f"Bearer {token}"),)
    return _make