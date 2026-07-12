from auth.access_level import AccessLevel
from fhir.patient import patient_to_fhir
from fhir.encounter import encounter_to_fhir
from fhir.condition import event_to_condition
from fhir.observation import event_to_observation
from fhir.medication_request import event_to_medication_request
from redaction.levels import redact_patient, redact_clinical_resource


def make_bundle(resources: list[dict]) -> dict:
    return {
        "resourceType": "Bundle",
        "type": "collection",
        "entry": [{"resource": r} for r in resources],
    }


def build_bundle(request, level: AccessLevel, salt: str) -> dict:
    resources = []

    if request.HasField("patient"):
        resources.append(redact_patient(patient_to_fhir(request.patient), level, salt))

    for encounter in request.encounters:
        resources.append(redact_clinical_resource(encounter_to_fhir(encounter), level, salt))

    for event in request.clinical_events:
        if event.event_type == "CONDITION":
            res = event_to_condition(event)
        elif event.event_type == "OBSERVATION":
            res = event_to_observation(event)
        elif event.event_type == "MEDICATION":
            res = event_to_medication_request(event)
        else:
            continue
        resources.append(redact_clinical_resource(res, level, salt))

    return make_bundle(resources)