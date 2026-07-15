from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from pydantic import BaseModel, SecretStr
import grpc.aio
import asyncio
import time
import os

from .config import settings
from .grpc_clients.servidor_auth import AuthClient
from .grpc_clients.patient_data import PatientDataClient
from .grpc_clients.datatransform import DataTransformClient

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

security = HTTPBearer()

async def _extract_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    return credentials.credentials

@app.post("/auth/login")
def login(credentials: LoginRequest):
    return AuthClient().login(username=credentials.username,
                              password=credentials.password.get_secret_value())


@app.post("/auth/refresh_token")
def refresh_token(token: str = Depends(_extract_token)):
    return AuthClient().refreshToken(
        token=token
    )

@app.post("/auth/logout")
def logout(token: str = Depends(_extract_token)):
    return AuthClient().logout(
        token=token
    )

@app.get("/patients")
async def get_patients(token: str = Depends(_extract_token)):
    res = PatientDataClient().get_patients(token=token)
    return res

@app.get("/patients/{patient_id}")
async def get_patient_details(patient_id: str, token: str = Depends(_extract_token)):
    res = PatientDataClient().get_patient_details(token=token, patient_id=patient_id)
    return res

@app.get("/cohorts")
async def get_cohort_data(code: str, projectId: str, token: str = Depends(_extract_token)):
    res = PatientDataClient().get_cohorts(token=token, project_id=projectId, cohort_code=code)
    return res

@app.get("/projects")
async def get_projects(token: str = Depends(_extract_token)):
    res = PatientDataClient().get_projects(token=token)
    return res

@app.get("/fhir/{resource_type}/{resource_id}")
async def get_fhir(resource_type: str, resource_id: str, token: str = Depends(_extract_token)):
    # Fake call to Transform service to simulate FHIR resource fetch
    res = DataTransformClient().transform(token=token, patient={"id": resource_id})
    return res.get("fhir_bundle", {})
