from proto import auth_pb2_grpc
from proto import auth_pb2
import time, grpc, jwt, logging
from concurrent import futures
ACCESS_TOKEN_TLL_SECCOND = 30*60
REFRESH_TOKEN_TLL_SECCOND = 60*60*24
SECRET = "secret"

class InMemoryUserRepository:
    """Repositório simples em memória, só para exemplo/testes."""
 
    def __init__(self):
        self._users = {}
        self.permission = {}
 
    def create_user(self, username: str, password: str, permission: tuple):
        self._users[username] = password
        self.permission[username] = permission
 
    def check_credentials(self, username: str, password: str) -> bool:
        return self._users.get(username) == password
 
    def clear(self):
        self._users.clear()


class AuthService(auth_pb2_grpc.AuthServicer):
    def __init__(self, user_repository: InMemoryUserRepository = None):
        # Injeção de dependência: facilita trocar por um repo real
        # (Postgres, Redis, etc.) em produção e por um fake nos testes.
        self._repo = user_repository or InMemoryUserRepository()
        self._template_permission = {
            "ANONYMIZED":False,
            "AGGREGATED":False,
            "PARTIAL":False,
            "FULL":False,
        }
    

    def Login(self, request: auth_pb2.Credentials, context: grpc.ServicerContext):
        if not request.username or not request.password:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "username e password são obrigatórios")
            return auth_pb2.LoginResponse()

        isOk = self._repo.check_credentials(request.username, request.password)
        if not isOk:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "usuário ou senha errado")
            return auth_pb2.LoginResponse()

        access_token, access_expires_at = self._generateAccessToken(self._repo[request.username])
        refresh_token, refresh_expires_at = self._generateRefreshToken()





    def RefreshToken(self, request, context):
        return super().RefreshToken(request, context)
    
    def Logout(self, request, context):
        return super().Logout(request, context)
    
    def _generateAccessToken(self, permission) -> str | int:
        if not (type(permission) == tuple) and not (type(permission) == list):
            raise TypeError

        if len(permission) == 0:
            return "", 0
        
        permisao = self._template_permission.copy()
        for p in permission:
            permisao[p] = True
        encoded = jwt.encode(permisao, SECRET, algorithm="HS256")
        expires_at = int(time.time())+ACCESS_TOKEN_TLL_SECCOND

        return encoded, expires_at
    
    def _generateRefreshToken(self, username) -> str | int:
        
        expires_at = int(time.time())+REFRESH_TOKEN_TLL_SECCOND
        encoded = jwt.encode({"username":username, "expires_at":expires_at}, SECRET, algorithm="HS256")

        return encoded, expires_at
    




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

