from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
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

@app.post("/auth/login")
def login(username:str, password:str):
    return AuthClient().login(username=username, password=password)
