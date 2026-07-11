from auth.access_level import AccessLevel
from redaction.pseudonymize import pseudonymize

_DROP_FIELDS = {
    AccessLevel.FULL: [],
    AccessLevel.PARTIAL: ["identifier"],
    AccessLevel.ANONYMIZED: ["identifier", "name", "birthDate"],
}


def redact_patient(resource: dict, level: AccessLevel, salt: str) -> dict:
    resource = dict(resource)

    for field in _DROP_FIELDS.get(level, []):
        resource.pop(field, None)

    if level == AccessLevel.PARTIAL:
        full_name = resource.get("name", [{}])[0].get("text", "")
        initials = "".join(w[0] for w in full_name.split() if w)
        resource["name"] = [{"text": initials}]
        resource["birthDate"] = resource["birthDate"][:4] if resource.get("birthDate") else None

    if level == AccessLevel.ANONYMIZED:
        resource["id"] = pseudonymize(resource["id"], salt)

    return resource


def redact_clinical_resource(resource: dict, level: AccessLevel, salt: str) -> dict:
    """Aplica-se a Encounter/Condition/Observation/MedicationRequest."""
    resource = dict(resource)
    if level == AccessLevel.ANONYMIZED:
        ref = resource.get("subject", {}).get("reference", "")
        patient_id = ref.split("/")[-1] if "/" in ref else ref
        resource["subject"] = {"reference": f"Patient/{pseudonymize(patient_id, salt)}"}
    return resource