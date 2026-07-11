def event_to_observation(event) -> dict:
    return {
        "resourceType": "Observation",
        "id": event.event_id,
        "subject": {"reference": f"Patient/{event.patient_id}"},
        "encounter": {"reference": f"Encounter/{event.encounter_id}"},
        "code": {"text": event.event_code},
        "valueQuantity": {"value": event.value, "unit": event.unit},
        "effectiveDateTime": event.event_date,
    }