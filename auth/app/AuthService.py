import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.Memory import *
from proto import auth_pb2_grpc, auth_pb2

import time, grpc, jwt
from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
load_dotenv() 

ACCESS_TOKEN_TLL_SECCOND = 30*60
REFRESH_TOKEN_TLL_SECCOND = 60*60*24
SECRET = os.getenv('SECRET')



class AuthService(auth_pb2_grpc.AuthServicer):
    def __init__(self, user_repository: MemoryInterface = None):
        # Injeção de dependência: facilita trocar por um repo real
        # (Postgres, Redis, etc.) em produção e por um fake nos testes.
        self._repo = user_repository or InMemoryUserRepository()
        self._template_permission = {
            "ANONYMIZED":False,
            "AGGREGATED":False,
            "PARTIAL":False,
            "FULL":False,
        }
        self._revoked_refresh_tokens = set()
    

    def Login(self, request: auth_pb2.Credentials, context: grpc.ServicerContext):
        if not request.username or not request.password:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "username e password são obrigatórios")
            return auth_pb2.LoginResponse()

        isOk = self._repo.check_credentials(request.username, request.password)
        if not isOk:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "usuário ou senha errado")
            return auth_pb2.LoginResponse()
        access_token, access_expires_at = self._generateAccessToken(self._repo.getPermissions(request.username), request.username)
        if access_token == "" or access_expires_at == 0:
            context.abort(grpc.StatusCode.INTERNAL, "usuário sem permissão")
            return auth_pb2.LoginResponse()
        refresh_token, refresh_expires_at = self._generateRefreshToken(request.username)
        if refresh_token == "" or refresh_expires_at == 0:
            context.abort(grpc.StatusCode.INTERNAL, "erro na criação do token")
            return auth_pb2.LoginResponse()

        return auth_pb2.LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=access_expires_at
        )


    def RefreshToken(self, request, context):
        if not request.refresh_token:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "refresh token inválido")
            return auth_pb2.RefresResponse()

        if request.refresh_token in self._revoked_refresh_tokens:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "refresh token inválido ou revogado")
            return auth_pb2.RefresResponse()

        try:
            payload = jwt.decode(request.refresh_token, SECRET, algorithms=["HS256"])
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "refresh token inválido ou expirado")
            return auth_pb2.RefresResponse()

        username = payload.get("username")
        if not username or not self._repo.check_user_exists(username) or request.refresh_token in self._revoked_refresh_tokens:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "refresh token inválido")
            return auth_pb2.RefresResponse()

        access_token, expires_at = self._generateAccessToken(self._repo.getPermissions(username), username)
        return auth_pb2.RefresResponse(access_token=access_token, expires_at=expires_at)
    
    def Logout(self, request, context):
        try:
            payload = jwt.decode(request.refresh_token, SECRET, algorithms=["HS256"])
            if not self._repo.check_user_exists(payload.get("username")):
                context.abort(grpc.StatusCode.INVALID_ARGUMENT, "token inválido")
                return auth_pb2.LogoutRequest()
        except:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "token inválido")
            return auth_pb2.LogoutRequest()

        if request.refresh_token:
            self._revoked_refresh_tokens.add(request.refresh_token)
        return auth_pb2.LogoutResponse()
    
    def _generateAccessToken(self, permission, username) -> tuple[str, int]:
        if not (type(permission) == tuple) and not (type(permission) == list):
            raise TypeError

        if len(permission) == 0:
            return "", 0
        
        permisao = self._template_permission.copy()
        for p in permission:
            permisao[p] = True
            
        role = ""
        if "FULL" in permission: role = "MEDICO"
        elif "PARTIAL" in permission: role = "ESTAGIARIO"
        elif "AGREGATED" in permission: role = "PESQUISADOR"

        expires_at = int(time.time())+ACCESS_TOKEN_TLL_SECCOND
        permisao["exp"] = expires_at
        permisao["sub"] = username
        permisao["role"] = role
        permisao["username"] = username
        encoded = jwt.encode(permisao, SECRET, algorithm="HS256")

        return encoded, expires_at
    
    def _generateRefreshToken(self, username) -> tuple[str, int]:
        if not self._repo.check_user_exists(username):
            raise UserNotFoundError(username)
        expires_at = int(time.time())+REFRESH_TOKEN_TLL_SECCOND
        encoded = jwt.encode({"username":username, "exp":expires_at}, SECRET, algorithm="HS256")

        return encoded, expires_at
    





