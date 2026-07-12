def patient_to_fhir(patient) -> dict:
    return {
        "resourceType": "Patient",
        "id": patient.patient_id,
        "name": [{"text": patient.name}],
        "birthDate": patient.birth_date,
        "gender": patient.gender,
        "address": [{"city": patient.city, "state": patient.state}],
        "identifier": [
            {"system": "cpf", "value": patient.cpf},
            {"system": "cns", "value": patient.cns},
        ],
    }