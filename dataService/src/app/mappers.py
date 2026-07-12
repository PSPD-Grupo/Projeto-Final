import hashlib
from datetime import date, datetime
from typing import Any

from app.user_context import AccessLevel


def _to_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, date | datetime):
        return value.isoformat()
    return str(value)


def _initials(full_name: str) -> str:
    return "".join(part[0].upper() for part in full_name.split() if part)


def _age(birth_date: date | None) -> int | None:
    if birth_date is None:
        return None
    today = date.today()
    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age


def _age_range(birth_date: date | None) -> str:
    age = _age(birth_date)
    if age is None:
        return ""
    if age < 18:
        return "0-17"
    if age <= 39:
        return "18-39"
    if age <= 59:
        return "40-59"
    if age <= 79:
        return "60-79"
    return "80+"


def _patient_hash(patient_id: str, salt: str) -> str:
    digest = hashlib.sha256(f"{salt}:{patient_id}".encode("utf-8")).hexdigest()
    return f"hash{digest[:12]}"


def _proto_access_level(pb2: Any, access_level: AccessLevel) -> Any:
    return getattr(pb2, access_level.value)


def patient_record_message(
    pb2: Any,
    row: dict[str, Any],
    access_level: AccessLevel,
    pseudonym_salt: str,
) -> Any:
    birth_date = row.get("birth_date")
    patient_id = _to_text(row.get("patient_id"))

    if access_level == AccessLevel.FULL:
        return pb2.PatientRecord(
            access_level=_proto_access_level(pb2, access_level),
            patient_ref=patient_id,
            full_name=_to_text(row.get("full_name")),
            birth_date=_to_text(birth_date),
            gender=_to_text(row.get("gender")),
            city=_to_text(row.get("city")),
            state=_to_text(row.get("state")),
            cpf=_to_text(row.get("cpf")),
            cns=_to_text(row.get("cns")),
        )

    if access_level == AccessLevel.PARTIAL:
        return pb2.PatientRecord(
            access_level=_proto_access_level(pb2, access_level),
            patient_ref=patient_id,
            initials=_initials(_to_text(row.get("full_name"))),
            birth_year=_to_text(birth_date.year if isinstance(birth_date, date) else ""),
            age_range=_age_range(birth_date if isinstance(birth_date, date) else None),
            gender=_to_text(row.get("gender")),
            city=_to_text(row.get("city")),
            state=_to_text(row.get("state")),
        )

    return pb2.PatientRecord(
        access_level=_proto_access_level(pb2, AccessLevel.ANONYMIZED),
        patient_ref=_patient_hash(patient_id, pseudonym_salt),
        age_range=_age_range(birth_date if isinstance(birth_date, date) else None),
        gender=_to_text(row.get("gender")),
        state=_to_text(row.get("state")),
    )


def encounter_message(
    pb2: Any,
    row: dict[str, Any],
    access_level: AccessLevel,
    pseudonym_salt: str,
) -> Any:
    patient_id = _to_text(row.get("patient_id"))
    patient_ref = (
        patient_id
        if access_level == AccessLevel.FULL
        else _patient_hash(patient_id, pseudonym_salt)
    )
    return pb2.Encounter(
        encounter_id=_to_text(row.get("encounter_id")),
        patient_ref=patient_ref,
        start_date=_to_text(row.get("start_date")),
        end_date=_to_text(row.get("end_date")),
        encounter_type=_to_text(row.get("encounter_type")),
        department=_to_text(row.get("department")),
    )


def clinical_event_message(
    pb2: Any,
    row: dict[str, Any],
    access_level: AccessLevel,
    pseudonym_salt: str,
) -> Any:
    patient_id = _to_text(row.get("patient_id"))
    patient_ref = (
        patient_id
        if access_level == AccessLevel.FULL
        else _patient_hash(patient_id, pseudonym_salt)
    )
    return pb2.ClinicalEvent(
        event_id=_to_text(row.get("event_id")),
        patient_ref=patient_ref,
        encounter_id=_to_text(row.get("encounter_id")),
        event_type=_to_text(row.get("event_type")),
        code=_to_text(row.get("code")),
        description=_to_text(row.get("description")),
        value=_to_text(row.get("value")),
        unit=_to_text(row.get("unit")),
        event_date=_to_text(row.get("event_date")),
    )


def research_project_message(pb2: Any, row: dict[str, Any]) -> Any:
    return pb2.ResearchProject(
        project_id=_to_text(row.get("project_id")),
        title=_to_text(row.get("title")),
        researcher_username=_to_text(row.get("researcher_username")),
        target_condition_code=_to_text(row.get("target_condition_code")),
        status=_to_text(row.get("status")),
        valid_until=_to_text(row.get("valid_until")),
    )


def bucket_message(pb2: Any, row: dict[str, Any]) -> Any:
    return pb2.Bucket(
        label=_to_text(row.get("label")),
        count=int(row.get("count") or 0),
        percentage=float(row.get("percentage") or 0),
    )


def anonymized_lab_result_message(
    pb2: Any,
    patient_row: dict[str, Any],
    exams: list[dict[str, Any]],
    pseudonym_salt: str,
) -> Any:
    birth_date = patient_row.get("birth_date")
    return pb2.AnonymizedLabResult(
        patient_hash=_patient_hash(_to_text(patient_row.get("patient_id")), pseudonym_salt),
        gender=_to_text(patient_row.get("gender")),
        age_range=_age_range(birth_date if isinstance(birth_date, date) else None),
        state=_to_text(patient_row.get("state")),
        exams=[
            pb2.LabExam(
                code=_to_text(exam.get("code")),
                description=_to_text(exam.get("description")),
                value=_to_text(exam.get("value")),
                unit=_to_text(exam.get("unit")),
                event_date=_to_text(exam.get("event_date")),
            )
            for exam in exams
        ],
    )
