import logging
import signal
from concurrent import futures

import grpc

from app.AuthService import AuthService
from app.Memory import InMemoryUserRepository
from proto import auth_pb2_grpc


def serve(port: str = "50051"):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    repo = InMemoryUserRepository()
    repo.create_user(
        username="user",
        password="senha123",
        permission=["FULL"]
    )

    auth_pb2_grpc.add_AuthServicer_to_server(
        AuthService(user_repository=repo),
        server,
    )

    server.add_insecure_port(f"[::]:{port}")
    server.start()

    logging.info("Servidor gRPC rodando na porta %s", port)

    def shutdown(signum, frame):
        logging.info("Recebido sinal %s.\nEncerrando servidor...", signum)
        server.stop(grace=5).wait()
        logging.info("Servidor encerrado.")

    signal.signal(signal.SIGINT, shutdown)   # Ctrl+C
    signal.signal(signal.SIGTERM, shutdown)  # kill

    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve()