import json
from concurrent import futures
import grpc
import pytest

import datatransform_pb2
import datatransform_pb2_grpc
from grpc_service import DataTransformServicer
from auth.interceptor import JwtAuthInterceptor
from tests.helpers.token_factory import make_token
from tests.conftest import TEST_SECRET, TEST_SALT


@pytest.fixture(scope="module")
def grpc_channel():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=4),
        interceptors=[JwtAuthInterceptor(TEST_SECRET)],
    )
    datatransform_pb2_grpc.add_DataTransformServicer_to_server(
        DataTransformServicer(pseudonymize_salt=TEST_SALT), server
    )
    port = server.add_insecure_port("[::]:0")
    server.start()
    channel = grpc.insecure_channel(f"localhost:{port}")
    yield channel
    server.stop(None)


def _auth_metadata(token):
    return [("authorization", f"Bearer {token}")]


def test_transform_paciente_completo(grpc_channel):
    stub = datatransform_pb2_grpc.DataTransformStub(grpc_channel)
    request = datatransform_pb2.TransformRequest(
        patient=datatransform_pb2.Patient(
            patient_id="P000001", name="João da Silva",
            birth_date="1970-05-10", gender="male",
        ),
    )
    response = stub.Transform(request, metadata=_auth_metadata(make_token(full=True)))
    bundle = json.loads(response.fhir_bundle_json)
    assert bundle["entry"][0]["resource"]["resourceType"] == "Patient"


def test_transform_sem_token_retorna_unauthenticated(grpc_channel):
    stub = datatransform_pb2_grpc.DataTransformStub(grpc_channel)
    request = datatransform_pb2.TransformRequest()
    with pytest.raises(grpc.RpcError) as exc:
        stub.Transform(request)  # sem metadata nenhum
    assert exc.value.code() == grpc.StatusCode.UNAUTHENTICATED


def test_transform_token_expirado_retorna_unauthenticated(grpc_channel):
    stub = datatransform_pb2_grpc.DataTransformStub(grpc_channel)
    request = datatransform_pb2.TransformRequest()
    expired = make_token(full=True, expired=True)
    with pytest.raises(grpc.RpcError) as exc:
        stub.Transform(request, metadata=_auth_metadata(expired))
    assert exc.value.code() == grpc.StatusCode.UNAUTHENTICATED


def test_transform_sem_permissao_retorna_permission_denied(grpc_channel):
    stub = datatransform_pb2_grpc.DataTransformStub(grpc_channel)
    request = datatransform_pb2.TransformRequest()
    no_access = make_token()  # nenhuma flag true
    with pytest.raises(grpc.RpcError) as exc:
        stub.Transform(request, metadata=_auth_metadata(no_access))
    assert exc.value.code() == grpc.StatusCode.PERMISSION_DENIED


def test_aggregate_requer_nivel_aggregated(grpc_channel):
    stub = datatransform_pb2_grpc.DataTransformStub(grpc_channel)
    request = datatransform_pb2.AggregateRequest(cohort_code="Diabetes")
    with pytest.raises(grpc.RpcError) as exc:
        stub.TransformAggregate(request, metadata=_auth_metadata(make_token(full=True)))
    assert exc.value.code() == grpc.StatusCode.PERMISSION_DENIED

def test_transform_token_expirado_retorna_reason_correto(grpc_channel):
    stub = datatransform_pb2_grpc.DataTransformStub(grpc_channel)
    request = datatransform_pb2.TransformRequest()
    expired = make_token(full=True, expired=True)
    with pytest.raises(grpc.RpcError) as exc:
        stub.Transform(request, metadata=_auth_metadata(expired))
    assert exc.value.code() == grpc.StatusCode.UNAUTHENTICATED
    reason = dict(exc.value.trailing_metadata() or []).get("error-reason")
    assert reason == "TOKEN_EXPIRED"


def test_transform_sem_token_retorna_reason_missing(grpc_channel):
    stub = datatransform_pb2_grpc.DataTransformStub(grpc_channel)
    request = datatransform_pb2.TransformRequest()
    with pytest.raises(grpc.RpcError) as exc:
        stub.Transform(request)
    reason = dict(exc.value.trailing_metadata() or []).get("error-reason")
    assert reason == "TOKEN_MISSING"