from fastapi import FastAPI, Response, status

from app.db import Database


def create_http_app(database: Database) -> FastAPI:
    app = FastAPI(title="Patient Data Service", version="0.1.0")

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/ready")
    async def ready(response: Response) -> dict[str, str]:
        try:
            is_ready = await database.ping()
        except Exception:
            is_ready = False

        if not is_ready:
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            return {"status": "not_ready"}
        return {"status": "ready"}

    return app
