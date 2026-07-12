import grpc

from app.config import settings
from app.grpc_generated import auth_pb2, auth_pb2_grpc
from fastapi import HTTPException


class AuthClient:
    def __init__(self, target: str | None = None):
        self.target = target or settings.servidor_auth_host

    def login(self, username, password):
        with grpc.insecure_channel(self.target) as channel:
            stub = auth_pb2_grpc.AuthStub(channel)
            try:
                response = stub.Login(auth_pb2.Credentials(username=username, password=password))
                
                return {
                    "refresh_token": response.refresh_token,
                    "access_token": response.access_token,
                    "expires_at": response.expires_at,
                }
            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.UNAUTHENTICATED:
                    raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
                elif e.code() == grpc.StatusCode.UNAVAILABLE:
                    raise HTTPException(status_code=503, detail="Serviço de autenticação indisponível")
                else:
                    print("Erro inesperado no gRPC durante login")
                    raise HTTPException(status_code=500, detail="Erro interno no servidor")
        

    def refreshToken(self, token):
        with grpc.insecure_channel(self.target) as channel:
            stub = auth_pb2_grpc.AuthStub(channel)
            try:
                response = stub.RefreshToken(auth_pb2.RefreshRequest(refresh_token=token))
                
                return {
                    "access_token": response.access_token,
                    "expires_at": response.expires_at,
                }
            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                    raise HTTPException(status_code=406, detail="Token inválido")
                elif e.code() == grpc.StatusCode.UNAUTHENTICATED:
                    raise HTTPException(status_code=406, detail="Token inválido")
                elif e.code() == grpc.StatusCode.UNAVAILABLE:
                    raise HTTPException(status_code=503, detail="Serviço de autenticação indisponível")
                else:
                    print("Erro inesperado no gRPC durante login")
                    raise HTTPException(status_code=500, detail="Erro interno no servidor")
        
    def logout(self, token):
        with grpc.insecure_channel(self.target) as channel:
            stub = auth_pb2_grpc.AuthStub(channel)
            try:
                response = stub.Logout(auth_pb2.LogoutRequest(refresh_token=token))
                return {}
            except grpc.RpcError as e:
                print('-='*50)
                print(e.code())
                print('-='*50)
                if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                    raise HTTPException(status_code=406, detail="Token inválido")
                elif e.code() == grpc.StatusCode.UNAUTHENTICATED:
                    raise HTTPException(status_code=406, detail="Token inválido")
                elif e.code() == grpc.StatusCode.UNAVAILABLE:
                    raise HTTPException(status_code=503, detail="Serviço de autenticação indisponível")
                else:
                    print("Erro inesperado no gRPC durante login")
                    raise HTTPException(status_code=500, detail="Erro interno no servidor")
