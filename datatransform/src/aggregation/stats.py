from collections import Counter

def aggregate_cohort(patients, clinical_events, cohort_code: str) -> dict:
    total = len(patients)
    if total == 0:
        return {
            "resourceType": "Parameters",
            "parameter": [{"name": "totalPatients", "valueInteger": 0}],
        }

    gender_counts = Counter(p.gender for p in patients)
    gender_pct = {g: round(100 * c / total, 1) for g, c in gender_counts.items()}

    observations = [
        float(e.value) for e in clinical_events
        if e.event_type == "OBSERVATION" and e.event_code == cohort_code and e.value
    ]
    avg_value = round(sum(observations) / len(observations), 2) if observations else None

    return {
        "resourceType": "Parameters",
        "parameter": [
            {"name": "totalPatients", "valueInteger": total},
            {"name": "genderDistribution", "valueString": str(gender_pct)},
            {"name": "averageObservationValue", "valueDecimal": avg_value},
        ],
    }