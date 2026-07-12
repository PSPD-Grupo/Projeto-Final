from auth.access_level import AccessLevel
from redaction.levels import redact_patient
from fhir.patient import patient_to_fhir


class FakePatient:
    patient_id = "P000001"
    name = "João da Silva"
    birth_date = "1970-05-10"
    gender = "male"
    city = "Brasília"
    state = "DF"
    cpf = "12345678900"
    cns = "987654321"


def test_full_mantem_todos_os_campos():
    resource = redact_patient(patient_to_fhir(FakePatient()), AccessLevel.FULL, "salt")
    assert "identifier" in resource
    assert resource["name"][0]["text"] == "João da Silva"


def test_partial_remove_identificadores_e_usa_iniciais():
    resource = redact_patient(patient_to_fhir(FakePatient()), AccessLevel.PARTIAL, "salt")
    assert "identifier" not in resource
    assert resource["name"][0]["text"] == "JS"
    assert resource["birthDate"] == "1970"


def test_anonymized_pseudonimiza_id_e_remove_nome():
    resource = redact_patient(patient_to_fhir(FakePatient()), AccessLevel.ANONYMIZED, "salt")
    assert resource["id"].startswith("hash")
    assert "name" not in resource