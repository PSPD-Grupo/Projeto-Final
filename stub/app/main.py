from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, SecretStr
import grpc.aio
import asyncio
import time
import os

from app.config import settings
from app.grpc_clients.servidor_auth import AuthClient

app = FastAPI(title="Stub FastAPI gRPC", version="0.1.0")

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    username: str
    password: SecretStr  # evita que a senha apareça em logs/repr acidentalmente

@app.post("/auth/login")
def login(credentials: LoginRequest):
    return AuthClient().login(username=credentials.username,
                              password=credentials.password.get_secret_value())


@app.post("/auth/refresh_token")
def refresh_token(token):
    return AuthClient().refreshToken(
        token=token
    )
