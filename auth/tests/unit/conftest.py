import pytest
from app import AuthService

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

@pytest.fixture(scope="function")
def AuthService(user_repository):
    authService = AuthService(user_repository)
    yield authService