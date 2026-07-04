from proto import auth_pb2_grpc
from proto import auth_pb2
from concurrent import futures
import logging
import grpc


class InMemoryUserRepository:
    """Repositório simples em memória, só para exemplo/testes."""
 
    def __init__(self):
        self._users = {}
 
    def create_user(self, username: str, password: str):
        self._users[username] = password
 
    def check_credentials(self, username: str, password: str) -> bool:
        return self._users.get(username) == password
 
    def clear(self):
        self._users.clear()


class AuthService(auth_pb2_grpc.AuthServicer):
    def __init__(self, user_repository: InMemoryUserRepository = None):
        # Injeção de dependência: facilita trocar por um repo real
        # (Postgres, Redis, etc.) em produção e por um fake nos testes.
        self._repo = user_repository or InMemoryUserRepository()
    

    def Login(self, request: auth_pb2.Credentials, context: grpc.ServicerContext):
        pass

def serve(port: str = "50051"):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
 
    repo = InMemoryUserRepository()
    repo.create_user(username="user", password="senha123")  # seed de exemplo
 
    auth_pb2_grpc.add_AuthServicer_to_server(AuthService(user_repository=repo), server)
 
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logging.info("Servidor gRPC rodando na porta %s", port)
    server.wait_for_termination()


if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    serve()

