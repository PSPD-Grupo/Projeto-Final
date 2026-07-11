from datetime import date, datetime
from typing import Any


def _to_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, date | datetime):
        return value.isoformat()
    return str(value)


def patient_message(pb2: Any, row: dict[str, Any]) -> Any:
    return pb2.Patient(
        patient_id=_to_text(row.get("patient_id")),
        full_name=_to_text(row.get("full_name")),
        birth_date=_to_text(row.get("birth_date")),
        gender=_to_text(row.get("gender")),
        city=_to_text(row.get("city")),
        state=_to_text(row.get("state")),
        cpf=_to_text(row.get("cpf")),
        cns=_to_text(row.get("cns")),
    )


def encounter_message(pb2: Any, row: dict[str, Any]) -> Any:
    return pb2.Encounter(
        encounter_id=_to_text(row.get("encounter_id")),
        patient_id=_to_text(row.get("patient_id")),
        start_date=_to_text(row.get("start_date")),
        end_date=_to_text(row.get("end_date")),
        encounter_type=_to_text(row.get("encounter_type")),
        department=_to_text(row.get("department")),
    )


def clinical_event_message(pb2: Any, row: dict[str, Any]) -> Any:
    return pb2.ClinicalEvent(
        event_id=_to_text(row.get("event_id")),
        patient_id=_to_text(row.get("patient_id")),
        encounter_id=_to_text(row.get("encounter_id")),
        event_type=_to_text(row.get("event_type")),
        code=_to_text(row.get("code")),
        description=_to_text(row.get("description")),
        value=_to_text(row.get("value")),
        unit=_to_text(row.get("unit")),
        event_date=_to_text(row.get("event_date")),
    )
