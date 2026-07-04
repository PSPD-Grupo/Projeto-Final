import pytest
from app.AuthService import AuthService

@pytest.fixture(scope="function")
def user_repository():
    """
    Repositório de usuários isolado por teste.

    Se o AuthServicer depender de um banco real, aqui é o lugar de
    subir uma conexão de teste (ex: sqlite em memória, container
    Postgres via testcontainers, etc.) e popular dados fixos.
    """
    from app.Memory import InMemoryUserRepository

    repo = InMemoryUserRepository()
    repo.create_user(username="user", password="senha123", permission=("FULL"))
    yield repo
    repo.clear()

@pytest.fixture(scope="function")
def auth_service(user_repository):
    return AuthService(user_repository) 