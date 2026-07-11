def event_to_condition(event) -> dict:
    return {
        "resourceType": "Condition",
        "id": event.event_id,
        "subject": {"reference": f"Patient/{event.patient_id}"},
        "encounter": {"reference": f"Encounter/{event.encounter_id}"},
        "code": {"text": event.event_code, "coding": [{"display": event.description}]},
        "onsetDateTime": event.event_date,
    }