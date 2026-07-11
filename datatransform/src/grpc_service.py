import json
import time
import grpc

import datatransform_pb2
import datatransform_pb2_grpc
from auth.access_level import AccessLevel
from fhir.bundle import build_bundle
from aggregation.stats import aggregate_cohort
from observability.metrics import TRANSFORM_REQUESTS, TRANSFORM_ERRORS, TRANSFORM_LATENCY


class DataTransformServicer(datatransform_pb2_grpc.DataTransformServicer):
    def __init__(self, pseudonymize_salt: str):
        self._salt = pseudonymize_salt

    def Transform(self, request, context):
        start = time.monotonic()
        level = context.access_level

        bundle = build_bundle(request, level, self._salt)

        TRANSFORM_REQUESTS.labels(access_level=level.value, rpc="Transform").inc()
        TRANSFORM_LATENCY.labels(rpc="Transform").observe(time.monotonic() - start)
        return datatransform_pb2.TransformResponse(fhir_bundle_json=json.dumps(bundle))

    def TransformAggregate(self, request, context):
        start = time.monotonic()
        level = context.access_level

        if level != AccessLevel.AGGREGATED:
            TRANSFORM_ERRORS.labels(error_type="wrong_level_for_aggregate").inc()
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "TransformAggregate requer nível AGGREGATED")

        result = aggregate_cohort(request.patients, request.clinical_events, request.cohort_code)

        TRANSFORM_REQUESTS.labels(access_level=level.value, rpc="TransformAggregate").inc()
        TRANSFORM_LATENCY.labels(rpc="TransformAggregate").observe(time.monotonic() - start)
        return datatransform_pb2.AggregateResponse(fhir_bundle_json=json.dumps(result))