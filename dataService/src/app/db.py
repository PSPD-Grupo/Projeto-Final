import asyncpg
from app.config import Settings


class Database:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._pool: asyncpg.Pool | None = None

    @property
    def pool(self) -> asyncpg.Pool:
        if self._pool is None:
            raise RuntimeError("Database pool has not been initialized")
        return self._pool

    async def connect(self) -> None:
        print("DB_HOST:", self._settings.db_host)
        print("DB_PORT:", self._settings.db_port)
        print("DATABASE_DSN:", self._settings.database_dsn.replace(self._settings.db_password, "******"))

        

        self._pool = await asyncpg.create_pool(
            dsn=self._settings.database_dsn,
            min_size=self._settings.db_pool_min_size,
            max_size=self._settings.db_pool_max_size,            
        )

    async def close(self) -> None:
        if self._pool is not None:
            await self._pool.close()
            self._pool = None

    async def ping(self) -> bool:
        async with self.pool.acquire() as connection:
            return await connection.fetchval("SELECT 1") == 1
