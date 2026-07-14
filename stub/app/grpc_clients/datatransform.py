import grpc
from fastapi import HTTPException
import json
from ..config import settings
from ..grpc_generated import datatransform_pb2, datatransform_pb2_grpc

class DataTransformClient:
    def __init__(self, target: str | None = None):
        self.target = target or settings.servidor_datatransform_host

    def transform(self, token: str, patient: dict, encounters: list = None, events: list = None):
        if encounters is None:
            encounters = []
        if events is None:
            events = []
            
        with grpc.insecure_channel(self.target) as channel:
            stub = datatransform_pb2_grpc.DataTransformStub(channel)
            
            try:
                # Convert dicts to protobuf objects
                p_msg = datatransform_pb2.Patient(
                    patient_id=patient.get("id", ""),
                    name=patient.get("name", ""),
                    birth_date=patient.get("dob", ""),
                    gender=patient.get("gender", ""),
                    city=patient.get("city", ""),
                    state=patient.get("state", ""),
                    cpf=patient.get("cpf", ""),
                    cns=patient.get("cns", "")
                )
                
                enc_msgs = []
                for e in encounters:
                    enc_msgs.append(datatransform_pb2.Encounter(
                        encounter_id=e.get("id", ""),
                        patient_id=e.get("patientId", ""),
                        start_date=e.get("date", ""),
                        end_date=e.get("endDate", ""),
                        encounter_type=e.get("type", ""),
                        department=e.get("department", "")
                    ))
                    
                evt_msgs = []
                for evt in events:
                    evt_msgs.append(datatransform_pb2.ClinicalEvent(
                        event_id=evt.get("id", ""),
                        patient_id=evt.get("patientId", patient.get("id", "")),
                        encounter_id=evt.get("encounterId", ""),
                        event_type=evt.get("type", ""),
                        event_code=evt.get("code", ""),
                        description=evt.get("description", ""),
                        event_date=evt.get("date", ""),
                        value=evt.get("value", ""),
                        unit=evt.get("unit", "")
                    ))

                request = datatransform_pb2.TransformRequest(
                    patient=p_msg,
                    encounters=enc_msgs,
                    clinical_events=evt_msgs
                )
                
                response = stub.Transform(
                    request, metadata=[("authorization", f"Bearer {token}")]
                )
                
                return {"fhir_bundle": json.loads(response.fhir_bundle_json)}
            except grpc.RpcError as e:
                self._handle_error(e)

    def transform_aggregate(self, token: str, cohort_code: str, patients: list = None, events: list = None):
        if patients is None:
            patients = []
        if events is None:
            events = []
            
        with grpc.insecure_channel(self.target) as channel:
            stub = datatransform_pb2_grpc.DataTransformStub(channel)
            
            try:
                p_msgs = []
                for patient in patients:
                    p_msgs.append(datatransform_pb2.Patient(
                        patient_id=patient.get("id", ""),
                        name=patient.get("name", ""),
                        birth_date=patient.get("dob", ""),
                        gender=patient.get("gender", ""),
                        city=patient.get("city", ""),
                        state=patient.get("state", ""),
                        cpf=patient.get("cpf", ""),
                        cns=patient.get("cns", "")
                    ))
                    
                evt_msgs = []
                for evt in events:
                    evt_msgs.append(datatransform_pb2.ClinicalEvent(
                        event_id=evt.get("id", ""),
                        patient_id=evt.get("patientId", ""),
                        encounter_id=evt.get("encounterId", ""),
                        event_type=evt.get("type", ""),
                        event_code=evt.get("code", ""),
                        description=evt.get("description", ""),
                        event_date=evt.get("date", ""),
                        value=evt.get("value", ""),
                        unit=evt.get("unit", "")
                    ))
                
                request = datatransform_pb2.AggregateRequest(
                    cohort_code=cohort_code,
                    patients=p_msgs,
                    clinical_events=evt_msgs
                )
                
                response = stub.TransformAggregate(
                    request, metadata=[("authorization", f"Bearer {token}")]
                )
                
                return {"fhir_bundle": json.loads(response.fhir_bundle_json)}
            except grpc.RpcError as e:
                self._handle_error(e)

    @staticmethod
    def _handle_error(e: grpc.RpcError):
        code = e.code()
        details = e.details()
        if code == grpc.StatusCode.UNAUTHENTICATED:
            raise HTTPException(status_code=401, detail=details or "Não autenticado")
        elif code == grpc.StatusCode.PERMISSION_DENIED:
            raise HTTPException(status_code=403, detail=details or "Sem permissão")
        elif code == grpc.StatusCode.NOT_FOUND:
            raise HTTPException(status_code=404, detail=details or "Não encontrado")
        elif code == grpc.StatusCode.UNAVAILABLE:
            raise HTTPException(status_code=503, detail="Serviço de transformação indisponível")
        else:
            raise HTTPException(status_code=500, detail=f"Erro interno: {code.name} - {details}")