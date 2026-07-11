from fhir.patient import patient_to_fhir

class FakePatient:
    patient_id = "P000001"
    full_name = "João da Silva"
    birth_date = "1970-05-10"
    gender = "male"
    city = "Brasília"
    state = "DF"
    cpf = "12345678900"
    cns = "987654321"


def test_patient_to_fhir_mapeia_campos_corretamente():
    resource = patient_to_fhir(FakePatient())
    assert resource["resourceType"] == "Patient"
    assert resource["id"] == "P000001"
    assert resource["name"][0]["text"] == "João da Silva"
    assert resource["gender"] == "male"