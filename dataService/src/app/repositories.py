from collections import defaultdict
from typing import Any

from app.db import Database
from app.user_context import AccessLevel, UserContext


DEFAULT_LIMIT = 50
MAX_LIMIT = 100


def normalize_pagination(limit: int, offset: int) -> tuple[int, int]:
    normalized_limit = limit if limit > 0 else DEFAULT_LIMIT
    return min(normalized_limit, MAX_LIMIT), max(offset, 0)


class PatientRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    # Requisito: validar se o usuario pode acessar um paciente identificado.
    # MEDICO recebe FULL quando o paciente esta sob sua responsabilidade.
    # ESTAGIARIO recebe PARTIAL quando o paciente esta ligado ao seu supervisor.
    async def patient_access_level(
        self,
        context: UserContext,
        patient_id: str,
    ) -> AccessLevel | None:
        if not context.username or not context.can_read_identified_patients:
            return None

        if context.is_medico:
            query = """
                SELECT EXISTS (
                    SELECT 1
                    FROM user_patient_assignments
                    WHERE username = $1
                      AND patient_id = $2
                      AND assignment_type = 'ATTENDING'
                      AND active = TRUE
                )
            """
            async with self._database.pool.acquire() as connection:
                allowed = await connection.fetchval(query, context.username, patient_id)
            if allowed:
                return AccessLevel.FULL

        if context.is_estagiario:
            query = """
                SELECT EXISTS (
                    SELECT 1
                    FROM user_patient_assignments
                    WHERE username = $1
                      AND patient_id = $2
                      AND assignment_type = 'TRAINEE'
                      AND supervisor_username IS NOT NULL
                      AND active = TRUE
                )
            """
            async with self._database.pool.acquire() as connection:
                allowed = await connection.fetchval(query, context.username, patient_id)
            if allowed:
                return AccessLevel.PARTIAL

        return None

    # Requisito: recuperar os dados cadastrais de um paciente respeitando FULL/PARTIAL.
    async def get_patient(
        self,
        context: UserContext,
        patient_id: str,
    ) -> tuple[dict[str, Any], AccessLevel] | None:
        access_level = await self.patient_access_level(context, patient_id)
        if access_level is None:
            return None

        query = """
            SELECT patient_id, full_name, birth_date, gender, city, state, cpf, cns
            FROM patients
            WHERE patient_id = $1
        """
        async with self._database.pool.acquire() as connection:
            row = await connection.fetchrow(query, patient_id)
            return (dict(row), access_level) if row else None

    # Requisito: localizar os pacientes associados a um medico.
    # Requisito: localizar os pacientes supervisionados por um estagiario.
    # A mesma busca muda a query de acordo com a role recebida no contexto.
    async def search_patients(
        self,
        context: UserContext,
        search_text: str,
        limit: int,
        offset: int,
    ) -> list[tuple[dict[str, Any], AccessLevel]]:
        if not context.can_read_identified_patients:
            return []

        limit, offset = normalize_pagination(limit, offset)
        pattern = f"%{search_text.strip()}%"

        if context.is_medico:
            query = """
                SELECT p.patient_id, p.full_name, p.birth_date, p.gender, p.city, p.state, p.cpf, p.cns,
                       'FULL' AS access_level
                FROM patients p
                INNER JOIN user_patient_assignments upa
                    ON upa.patient_id = p.patient_id
                   AND upa.username = $2
                   AND upa.assignment_type = 'ATTENDING'
                   AND upa.active = TRUE
                WHERE $1 = '%%'
                   OR p.full_name ILIKE $1
                   OR p.patient_id ILIKE $1
                   OR p.cpf ILIKE $1
                   OR p.cns ILIKE $1
                ORDER BY p.full_name
                LIMIT $3 OFFSET $4
            """
        else:
            query = """
                SELECT p.patient_id, p.full_name, p.birth_date, p.gender, p.city, p.state, p.cpf, p.cns,
                       'PARTIAL' AS access_level
                FROM patients p
                INNER JOIN user_patient_assignments upa
                    ON upa.patient_id = p.patient_id
                   AND upa.username = $2
                   AND upa.assignment_type = 'TRAINEE'
                   AND upa.supervisor_username IS NOT NULL
                   AND upa.active = TRUE
                WHERE $1 = '%%'
                   OR p.full_name ILIKE $1
                   OR p.patient_id ILIKE $1
                ORDER BY p.full_name
                LIMIT $3 OFFSET $4
            """

        async with self._database.pool.acquire() as connection:
            rows = await connection.fetch(query, pattern, context.username, limit, offset)
            return [(dict(row), AccessLevel(row["access_level"])) for row in rows]

    # Requisito: recuperar os atendimentos de um paciente.
    async def list_encounters(
        self,
        context: UserContext,
        patient_id: str,
        limit: int,
        offset: int,
    ) -> tuple[list[dict[str, Any]], AccessLevel] | None:
        access_level = await self.patient_access_level(context, patient_id)
        if access_level is None:
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
            return [dict(row) for row in rows], access_level

    # Requisito: recuperar diagnosticos, exames e medicamentos.
    # event_type aceita CONDITION, OBSERVATION ou MEDICATION.
    async def list_clinical_events(
        self,
        context: UserContext,
        patient_id: str,
        encounter_id: str,
        event_type: str,
        limit: int,
        offset: int,
    ) -> tuple[list[dict[str, Any]], AccessLevel] | None:
        access_level = await self.patient_access_level(context, patient_id)
        if access_level is None:
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
            return [dict(row) for row in rows], access_level

    # Requisito: recuperar informacoes relacionadas aos projetos de pesquisa.
    async def list_research_projects(
        self,
        context: UserContext,
        status: str,
    ) -> list[dict[str, Any]]:
        if not context.can_read_research_data:
            return []

        query = """
            SELECT project_id, title, researcher_username, target_condition_code, status, valid_until
            FROM projects
            WHERE researcher_username = $1
              AND ($2 = '' OR status = $2)
            ORDER BY valid_until DESC, title
        """
        async with self._database.pool.acquire() as connection:
            rows = await connection.fetch(query, context.username, status)
            return [dict(row) for row in rows]

    # Apoio aos requisitos de pesquisa: garante que o projeto pertence ao pesquisador,
    # esta aprovado e ainda esta dentro da validade.
    async def _get_active_project(
        self,
        context: UserContext,
        project_id: str,
    ) -> dict[str, Any] | None:
        if not context.can_read_research_data:
            return None

        query = """
            SELECT project_id, title, researcher_username, target_condition_code, status, valid_until
            FROM projects
            WHERE project_id = $1
              AND researcher_username = $2
              AND status = 'APPROVED'
              AND valid_until >= CURRENT_DATE
        """
        async with self._database.pool.acquire() as connection:
            row = await connection.fetchrow(query, project_id, context.username)
            return dict(row) if row else None

    # Requisito: recuperar os pacientes pertencentes a uma determinada coorte.
    # A coorte e definida pelo target_condition_code do projeto.
    # O retorno ainda contem patient_id real internamente; a anonimização acontece no mapper.
    async def list_research_cohort_patients(
        self,
        context: UserContext,
        project_id: str,
        limit: int,
        offset: int,
    ) -> list[dict[str, Any]] | None:
        project = await self._get_active_project(context, project_id)
        if project is None:
            return None

        limit, offset = normalize_pagination(limit, offset)
        query = """
            SELECT DISTINCT p.patient_id, p.birth_date, p.gender, p.state
            FROM patients p
            INNER JOIN clinical_events ce ON ce.patient_id = p.patient_id
            WHERE ce.event_type = 'CONDITION'
              AND ce.code = $1
            ORDER BY p.patient_id
            LIMIT $2 OFFSET $3
        """
        async with self._database.pool.acquire() as connection:
            rows = await connection.fetch(
                query,
                project["target_condition_code"],
                limit,
                offset,
            )
            return [dict(row) for row in rows]

    # Requisito: agregacoes de coorte.
    # Inclui quantidade total, distribuicao por sexo, distribuicao por faixa etaria,
    # media de hemoglobina glicada e frequencia de medicamentos.
    async def get_cohort_stats(
        self,
        context: UserContext,
        project_id: str,
    ) -> dict[str, Any] | None:
        project = await self._get_active_project(context, project_id)
        if project is None:
            return None

        condition_code = project["target_condition_code"]
        async with self._database.pool.acquire() as connection:
            total = await connection.fetchval(
                """
                SELECT COUNT(DISTINCT p.patient_id)
                FROM patients p
                INNER JOIN clinical_events ce ON ce.patient_id = p.patient_id
                WHERE ce.event_type = 'CONDITION'
                  AND ce.code = $1
                """,
                condition_code,
            )
            gender_rows = await connection.fetch(
                """
                SELECT p.gender AS label, COUNT(DISTINCT p.patient_id) AS count,
                       CASE WHEN $2::int = 0 THEN 0
                            ELSE COUNT(DISTINCT p.patient_id)::float * 100 / $2::float
                       END AS percentage
                FROM patients p
                INNER JOIN clinical_events ce ON ce.patient_id = p.patient_id
                WHERE ce.event_type = 'CONDITION'
                  AND ce.code = $1
                GROUP BY p.gender
                ORDER BY p.gender
                """,
                condition_code,
                total,
            )
            age_rows = await connection.fetch(
                """
                WITH cohort AS (
                    SELECT DISTINCT p.patient_id, p.birth_date
                    FROM patients p
                    INNER JOIN clinical_events ce ON ce.patient_id = p.patient_id
                    WHERE ce.event_type = 'CONDITION'
                      AND ce.code = $1
                ),
                buckets AS (
                    SELECT CASE
                        WHEN EXTRACT(YEAR FROM age(CURRENT_DATE, birth_date)) < 18 THEN '0-17'
                        WHEN EXTRACT(YEAR FROM age(CURRENT_DATE, birth_date)) <= 39 THEN '18-39'
                        WHEN EXTRACT(YEAR FROM age(CURRENT_DATE, birth_date)) <= 59 THEN '40-59'
                        WHEN EXTRACT(YEAR FROM age(CURRENT_DATE, birth_date)) <= 79 THEN '60-79'
                        ELSE '80+'
                    END AS label, patient_id
                    FROM cohort
                )
                SELECT label, COUNT(*) AS count,
                       CASE WHEN $2::int = 0 THEN 0
                            ELSE COUNT(*)::float * 100 / $2::float
                       END AS percentage
                FROM buckets
                GROUP BY label
                ORDER BY label
                """,
                condition_code,
                total,
            )
            department_rows = await connection.fetch(
                """
                SELECT e.department AS label, COUNT(DISTINCT p.patient_id) AS count,
                       CASE WHEN $2::int = 0 THEN 0
                            ELSE COUNT(DISTINCT p.patient_id)::float * 100 / $2::float
                       END AS percentage
                FROM patients p
                INNER JOIN clinical_events ce ON ce.patient_id = p.patient_id
                INNER JOIN encounters e ON e.patient_id = p.patient_id
                WHERE ce.event_type = 'CONDITION'
                  AND ce.code = $1
                GROUP BY e.department
                ORDER BY count DESC, e.department
                """,
                condition_code,
                total,
            )
            hba1c_average = await connection.fetchval(
                """
                WITH cohort AS (
                    SELECT DISTINCT p.patient_id
                    FROM patients p
                    INNER JOIN clinical_events condition
                      ON condition.patient_id = p.patient_id
                    WHERE condition.event_type = 'CONDITION'
                      AND condition.code = $1
                )
                SELECT AVG(NULLIF(regexp_replace(obs.value, '[^0-9.]', '', 'g'), '')::numeric)
                FROM cohort c
                INNER JOIN clinical_events obs
                  ON obs.patient_id = c.patient_id
                WHERE obs.event_type = 'OBSERVATION'
                  AND (
                    obs.code ILIKE '%HBA1C%'
                    OR obs.description ILIKE '%hemoglobina glicada%'
                    OR obs.description ILIKE '%glycated hemoglobin%'
                  )
                """,
                condition_code,
            )
            medication_rows = await connection.fetch(
                """
                WITH cohort AS (
                    SELECT DISTINCT p.patient_id
                    FROM patients p
                    INNER JOIN clinical_events condition
                      ON condition.patient_id = p.patient_id
                    WHERE condition.event_type = 'CONDITION'
                      AND condition.code = $1
                )
                SELECT medication.description AS label,
                       COUNT(*) AS count,
                       CASE WHEN $2::int = 0 THEN 0
                            ELSE COUNT(*)::float * 100 / $2::float
                       END AS percentage
                FROM cohort c
                INNER JOIN clinical_events medication
                  ON medication.patient_id = c.patient_id
                WHERE medication.event_type = 'MEDICATION'
                GROUP BY medication.description
                ORDER BY count DESC, medication.description
                LIMIT 20
                """,
                condition_code,
                total,
            )

        return {
            "project": project,
            "total_patients": int(total or 0),
            "gender_distribution": [dict(row) for row in gender_rows],
            "age_distribution": [dict(row) for row in age_rows],
            "department_distribution": [dict(row) for row in department_rows],
            "hba1c_average": float(hba1c_average) if hba1c_average is not None else None,
            "medication_frequency": [dict(row) for row in medication_rows],
        }

    # Requisito: exames laboratoriais por paciente com dados anonimizados.
    # Usa a coorte do projeto e retorna apenas exames/eventos OBSERVATION.
    async def list_anonymized_lab_results(
        self,
        context: UserContext,
        project_id: str,
        limit: int,
        offset: int,
    ) -> list[dict[str, Any]] | None:
        project = await self._get_active_project(context, project_id)
        if project is None:
            return None

        limit, offset = normalize_pagination(limit, offset)
        condition_code = project["target_condition_code"]
        query = """
            WITH cohort AS (
                SELECT DISTINCT p.patient_id, p.birth_date, p.gender, p.state
                FROM patients p
                INNER JOIN clinical_events ce ON ce.patient_id = p.patient_id
                WHERE ce.event_type = 'CONDITION'
                  AND ce.code = $1
                ORDER BY p.patient_id
                LIMIT $2 OFFSET $3
            )
            SELECT c.patient_id, c.birth_date, c.gender, c.state,
                   ce.code, ce.description, ce.value, ce.unit, ce.event_date
            FROM cohort c
            LEFT JOIN clinical_events ce
              ON ce.patient_id = c.patient_id
             AND ce.event_type = 'OBSERVATION'
            ORDER BY c.patient_id, ce.event_date DESC
        """
        async with self._database.pool.acquire() as connection:
            rows = await connection.fetch(query, condition_code, limit, offset)

        grouped: dict[str, dict[str, Any]] = {}
        exams_by_patient: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in rows:
            data = dict(row)
            patient_id = data["patient_id"]
            grouped[patient_id] = {
                "patient_id": patient_id,
                "birth_date": data["birth_date"],
                "gender": data["gender"],
                "state": data["state"],
            }
            if data.get("code"):
                exams_by_patient[patient_id].append(
                    {
                        "code": data["code"],
                        "description": data["description"],
                        "value": data["value"],
                        "unit": data["unit"],
                        "event_date": data["event_date"],
                    }
                )

        return [
            {"patient": patient, "exams": exams_by_patient[patient_id]}
            for patient_id, patient in grouped.items()
        ]
