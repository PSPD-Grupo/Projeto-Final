def encounter_to_fhir(encounter) -> dict:
    return {
        "resourceType": "Encounter",
        "id": encounter.encounter_id,
        "subject": {"reference": f"Patient/{encounter.patient_id}"},
        "class": encounter.encounter_type,
        "serviceProvider": {"display": encounter.department},
        "period": {"start": encounter.start_date, "end": encounter.end_date},
    }