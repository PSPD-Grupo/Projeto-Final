import grpc

from proto import auth_pb2
from proto import auth_pb2_grpc


class AuthClient:
    def __init__(self, address="localhost:50051"):
        self.channel = grpc.insecure_channel(address)
        self.stub = auth_pb2_grpc.AuthStub(self.channel)

    def login(self, username: str, password: str):
        request = auth_pb2.Credentials(
            username=username,
            password=password
        )

        return self.stub.Login(request)

    def refresh_token(self, refresh_token: str):
        request = auth_pb2.RefreshRequest(
            refresh_token=refresh_token
        )

        return self.stub.RefreshToken(request)

    def logout(self, refresh_token: str):
        request = auth_pb2.LogoutRequest(
            refresh_token=refresh_token
        )

        return self.stub.Logout(request)