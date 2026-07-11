from typing import Any

from app.db import Database
from app.user_context import UserContext


DEFAULT_LIMIT = 50
MAX_LIMIT = 100


def normalize_pagination(limit: int, offset: int) -> tuple[int, int]:
    normalized_limit = limit if limit > 0 else DEFAULT_LIMIT
    return min(normalized_limit, MAX_LIMIT), max(offset, 0)


class PatientRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    async def can_access_patient(self, context: UserContext, patient_id: str) -> bool:
        if context.has_global_patient_read:
            return True
        if not context.username:
            return False

        query = """
            SELECT EXISTS (
                SELECT 1
                FROM user_patient_assignments
                WHERE username = $1
                  AND patient_id = $2
                  AND active = TRUE
            )
        """
        async with self._database.pool.acquire() as connection:
            return bool(await connection.fetchval(query, context.username, patient_id))

    async def get_patient(self, context: UserContext, patient_id: str) -> dict[str, Any] | None:
        if not await self.can_access_patient(context, patient_id):
            return None

        query = """
            SELECT patient_id, full_name, birth_date, gender, city, state, cpf, cns
            FROM patients
            WHERE patient_id = $1
        """
        async with self._database.pool.acquire() as connection:
            row = await connection.fetchrow(query, patient_id)
            return dict(row) if row else None

    async def search_patients(
        self,
        context: UserContext,
        search_text: str,
        limit: int,
        offset: int,
    ) -> list[dict[str, Any]]:
        limit, offset = normalize_pagination(limit, offset)
        pattern = f"%{search_text.strip()}%"

        if context.has_global_patient_read:
            query = """
                SELECT patient_id, full_name, birth_date, gender, city, state, cpf, cns
                FROM patients
                WHERE $1 = '%%'
                   OR full_name ILIKE $1
                   OR patient_id ILIKE $1
                   OR cpf ILIKE $1
                   OR cns ILIKE $1
                ORDER BY full_name
                LIMIT $2 OFFSET $3
            """
            params = (pattern, limit, offset)
        else:
            query = """
                SELECT p.patient_id, p.full_name, p.birth_date, p.gender, p.city, p.state, p.cpf, p.cns
                FROM patients p
                INNER JOIN user_patient_assignments upa
                    ON upa.patient_id = p.patient_id
                   AND upa.username = $2
                   AND upa.active = TRUE
                WHERE $1 = '%%'
                   OR p.full_name ILIKE $1
                   OR p.patient_id ILIKE $1
                   OR p.cpf ILIKE $1
                   OR p.cns ILIKE $1
                ORDER BY p.full_name
                LIMIT $3 OFFSET $4
            """
            params = (pattern, context.username, limit, offset)

        async with self._database.pool.acquire() as connection:
            rows = await connection.fetch(query, *params)
            return [dict(row) for row in rows]

    async def list_encounters(
        self,
        context: UserContext,
        patient_id: str,
        limit: int,
        offset: int,
    ) -> list[dict[str, Any]] | None:
        if not await self.can_access_patient(context, patient_id):
            return None

        limit, offset = normalize_pagination(limit, offset)
        query = """
            SELECT encounter_id, patient_id, start_date, end_date, encounter_type, department
            FROM encounters
            WHERE patient_id = $1
            ORDER BY start_date DESC
            LIMIT $2 OFFSET $3
        """
        async with self._database.pool.acquire() as connection:
            rows = await connection.fetch(query, patient_id, limit, offset)
            return [dict(row) for row in rows]

    async def list_clinical_events(
        self,
        context: UserContext,
        patient_id: str,
        encounter_id: str,
        event_type: str,
        limit: int,
        offset: int,
    ) -> list[dict[str, Any]] | None:
        if not await self.can_access_patient(context, patient_id):
            return None

        limit, offset = normalize_pagination(limit, offset)
        query = """
            SELECT event_id, patient_id, encounter_id, event_type, code, description, value, unit, event_date
            FROM clinical_events
            WHERE patient_id = $1
              AND ($2 = '' OR encounter_id = $2)
              AND ($3 = '' OR event_type = $3)
            ORDER BY event_date DESC
            LIMIT $4 OFFSET $5
        """
        async with self._database.pool.acquire() as connection:
            rows = await connection.fetch(query, patient_id, encounter_id, event_type, limit, offset)
            return [dict(row) for row in rows]
