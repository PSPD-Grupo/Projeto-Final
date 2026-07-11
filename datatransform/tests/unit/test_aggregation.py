from aggregation.stats import aggregate_cohort

class FakePatient:
    def __init__(self, gender):
        self.gender = gender


class FakeEvent:
    def __init__(self, event_type, event_code, value):
        self.event_type = event_type
        self.event_code = event_code
        self.value = value


def test_aggregate_com_lista_vazia_nao_quebra():
    result = aggregate_cohort([], [], "Diabetes")
    assert result["parameter"][0]["name"] == "totalPatients"
    assert result["parameter"][0]["valueInteger"] == 0


def test_aggregate_calcula_distribuicao_de_genero():
    patients = [FakePatient("F"), FakePatient("F"), FakePatient("M")]
    result = aggregate_cohort(patients, [], "Diabetes")
    total_param = next(p for p in result["parameter"] if p["name"] == "totalPatients")
    assert total_param["valueInteger"] == 3


def test_aggregate_calcula_media_de_observacao():
    patients = [FakePatient("F")]
    events = [
        FakeEvent("OBSERVATION", "HbA1c", "8.0"),
        FakeEvent("OBSERVATION", "HbA1c", "6.0"),
    ]
    result = aggregate_cohort(patients, events, "HbA1c")
    avg_param = next(p for p in result["parameter"] if p["name"] == "averageObservationValue")
    assert avg_param["valueDecimal"] == 7.0