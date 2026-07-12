def event_to_medication_request(event) -> dict:
    return {
        "resourceType": "MedicationRequest",
        "id": event.event_id,
        "subject": {"reference": f"Patient/{event.patient_id}"},
        "encounter": {"reference": f"Encounter/{event.encounter_id}"},
        "medicationCodeableConcept": {"text": event.event_code},
        "dosageInstruction": [{"text": f"{event.value} {event.unit}".strip()}],
        "authoredOn": event.event_date,
    }