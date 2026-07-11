import asyncio
import logging

import grpc
import uvicorn

from app.config import get_settings
from app.db import Database
from app.grpc_codegen import ensure_grpc_generated
from app.http_app import create_http_app
from app.repositories import PatientRepository


async def serve() -> None:
    ensure_grpc_generated()

    from app.grpc_service import register_patient_data_service

    settings = get_settings()
    logging.basicConfig(level=settings.log_level)

    database = Database(settings)
    await database.connect()

    grpc_server = grpc.aio.server()
    repository = PatientRepository(database)
    register_patient_data_service(grpc_server, repository, settings)
    grpc_server.add_insecure_port(settings.grpc_bind_address)

    http_app = create_http_app(database)
    http_config = uvicorn.Config(
        http_app,
        host=settings.http_host,
        port=settings.http_port,
        log_level=settings.log_level.lower(),
    )
    http_server = uvicorn.Server(http_config)

    try:
        await grpc_server.start()
        logging.info("gRPC server listening on %s", settings.grpc_bind_address)

        http_task = asyncio.create_task(http_server.serve())
        await grpc_server.wait_for_termination()
        await http_task
    finally:
        await grpc_server.stop(grace=5)
        await database.close()


def main() -> None:
    asyncio.run(serve())


if __name__ == "__main__":
    main()
