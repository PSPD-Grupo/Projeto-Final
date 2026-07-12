from concurrent import futures
import logging
import grpc

import datatransform_pb2_grpc
from grpc_service import DataTransformServicer
from auth.interceptor import JwtAuthInterceptor
from config import Settings
from observability.metrics import start_metrics_server

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def serve():
    settings = Settings()
    start_metrics_server(settings.metrics_port)
    log.info("Métricas Prometheus em :%s/metrics", settings.metrics_port)

    interceptors = [JwtAuthInterceptor(settings.jwt_secret)]

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=interceptors,
    )
    datatransform_pb2_grpc.add_DataTransformServicer_to_server(
        DataTransformServicer(settings.pseudonymize_salt), server
    )
    server.add_insecure_port(f"[::]:{settings.grpc_port}")
    server.start()
    log.info("Data Transform Service ouvindo em :%s", settings.grpc_port)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()