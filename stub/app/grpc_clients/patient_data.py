import jwt
import grpc
from fastapi import HTTPException
from ..config import settings
from ..grpc_generated import patient_data_pb2, patient_data_pb2_grpc
from google.protobuf.json_format import MessageToDict

def _get_metadata(token: str):
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        username = payload.get("sub", "")
        role = payload.get("role", "")
        return [
            ("authorization", f"Bearer {token}"),
            ("x-user-username", username),
            ("x-user-roles", role),
            ("x-user-scopes", "patient:read")
        ]
    except Exception:
        return [("authorization", f"Bearer {token}")]

class PatientDataClient:
    def __init__(self, target: str | None = None):
        self.target = target or settings.servidor_b_host

    def _handle_error(self, e: grpc.RpcError):
        code = e.code()
        details = e.details()
        if code == grpc.StatusCode.UNAUTHENTICATED:
            raise HTTPException(status_code=401, detail=details or "Não autenticado")
        elif code == grpc.StatusCode.PERMISSION_DENIED:
            raise HTTPException(status_code=403, detail=details or "Acesso Negado")
        elif code == grpc.StatusCode.NOT_FOUND:
            raise HTTPException(status_code=404, detail=details or "Não encontrado")
        elif code == grpc.StatusCode.UNAVAILABLE:
            raise HTTPException(status_code=503, detail="Serviço indisponível")
        else:
            raise HTTPException(status_code=500, detail=f"Erro interno: {code.name} - {details}")

    def get_patients(self, token: str):
        with grpc.insecure_channel(self.target) as channel:
            stub = patient_data_pb2_grpc.PatientDataServiceStub(channel)
            try:
                response = stub.SearchPatients(
                    patient_data_pb2.SearchPatientsRequest(query="", limit=100, offset=0),
                    metadata=_get_metadata(token)
                )
                return [MessageToDict(p, preserving_proto_field_name=True) for p in response.patients]
            except grpc.RpcError as e:
                self._handle_error(e)

    def get_patient_details(self, token: str, patient_id: str):
        with grpc.insecure_channel(self.target) as channel:
            stub = patient_data_pb2_grpc.PatientDataServiceStub(channel)
            try:
                p_resp = stub.GetPatient(
                    patient_data_pb2.GetPatientRequest(patient_id=patient_id),
                    metadata=_get_metadata(token)
                )
                enc_resp = stub.ListEncounters(
                    patient_data_pb2.ListEncountersRequest(patient_id=patient_id, limit=100, offset=0),
                    metadata=_get_metadata(token)
                )
                evt_resp = stub.ListClinicalEvents(
                    patient_data_pb2.ListClinicalEventsRequest(patient_id=patient_id, limit=100, offset=0),
                    metadata=_get_metadata(token)
                )
                
                return {
                    "patient": MessageToDict(p_resp.patient, preserving_proto_field_name=True) if p_resp.patient else None,
                    "encounters": [MessageToDict(e, preserving_proto_field_name=True) for e in enc_resp.encounters],
                    "events": [MessageToDict(e, preserving_proto_field_name=True) for e in evt_resp.events]
                }
            except grpc.RpcError as e:
                self._handle_error(e)

    def get_cohorts(self, token: str, project_id: str, cohort_code: str):
        with grpc.insecure_channel(self.target) as channel:
            stub = patient_data_pb2_grpc.PatientDataServiceStub(channel)
            try:
                response = stub.GetCohortStats(
                    patient_data_pb2.GetCohortStatsRequest(project_id=project_id),
                    metadata=_get_metadata(token)
                )
                return MessageToDict(response, preserving_proto_field_name=True)
            except grpc.RpcError as e:
                self._handle_error(e)

    def get_projects(self, token: str):
        with grpc.insecure_channel(self.target) as channel:
            stub = patient_data_pb2_grpc.PatientDataServiceStub(channel)
            try:
                response = stub.ListResearchProjects(
                    patient_data_pb2.ListResearchProjectsRequest(),
                    metadata=_get_metadata(token)
                )
                return [MessageToDict(p, preserving_proto_field_name=True) for p in response.projects]
            except grpc.RpcError as e:
                self._handle_error(e)
