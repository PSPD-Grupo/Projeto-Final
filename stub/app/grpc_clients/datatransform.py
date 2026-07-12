import grpc

from app.config import settings
from app.grpc_generated import datatransform_pb2, datatransform_pb2_grpc
from fastapi import HTTPException


class DataTransformClient:
    def __init__(self, target: str | None = None):
        self.target = target or settings.servidor_datatransform_host

    def transform(self, token, patient=None, encounters=None, clinical_events=None):
        with grpc.insecure_channel(self.target) as channel:
            stub = datatransform_pb2_grpc.DataTransformStub(channel)
            try:
                request = datatransform_pb2.TransformRequest(
                    patient=patient,
                    encounters=encounters or [],
                    clinical_events=clinical_events or [],
                )
                response = stub.Transform(
                    request, metadata=[("authorization", f"Bearer {token}")]
                )
                return {"fhir_bundle": response.fhir_bundle_json}
            except grpc.RpcError as e:
                self._handle_error(e)

    def transform_aggregate(self, token, cohort_code, patients=None, clinical_events=None):
        with grpc.insecure_channel(self.target) as channel:
            stub = datatransform_pb2_grpc.DataTransformStub(channel)
            try:
                request = datatransform_pb2.AggregateRequest(
                    cohort_code=cohort_code,
                    patients=patients or [],
                    clinical_events=clinical_events or [],
                )
                response = stub.TransformAggregate(
                    request, metadata=[("authorization", f"Bearer {token}")]
                )
                return {"fhir_bundle": response.fhir_bundle_json}
            except grpc.RpcError as e:
                self._handle_error(e)

    @staticmethod
    def _handle_error(e: grpc.RpcError):
        reason = dict(e.trailing_metadata() or []).get("error-reason")

        if reason == "TOKEN_EXPIRED":
            raise HTTPException(status_code=401, detail="Token expirado")
        elif reason == "TOKEN_INVALID":
            raise HTTPException(status_code=401, detail="Token inválido")
        elif reason == "TOKEN_MISSING":
            raise HTTPException(status_code=401, detail="Token não enviado")
        elif reason == "NO_ACCESS_LEVEL":
            raise HTTPException(status_code=403, detail="Sem permissão de acesso")
        elif e.code() == grpc.StatusCode.UNAVAILABLE:
            raise HTTPException(status_code=503, detail="Serviço de transformação indisponível")
        else:
            print("Erro inesperado no gRPC durante Transform/TransformAggregate")
            raise HTTPException(status_code=500, detail="Erro interno no servidor")