from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Patient(_message.Message):
    __slots__ = ("patient_id", "name", "birth_date", "gender", "city", "state", "cpf", "cns")
    PATIENT_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    BIRTH_DATE_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    CITY_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    CPF_FIELD_NUMBER: _ClassVar[int]
    CNS_FIELD_NUMBER: _ClassVar[int]
    patient_id: str
    name: str
    birth_date: str
    gender: str
    city: str
    state: str
    cpf: str
    cns: str
    def __init__(self, patient_id: _Optional[str] = ..., name: _Optional[str] = ..., birth_date: _Optional[str] = ..., gender: _Optional[str] = ..., city: _Optional[str] = ..., state: _Optional[str] = ..., cpf: _Optional[str] = ..., cns: _Optional[str] = ...) -> None: ...

class Encounter(_message.Message):
    __slots__ = ("encounter_id", "patient_id", "start_date", "end_date", "encounter_type", "department")
    ENCOUNTER_ID_FIELD_NUMBER: _ClassVar[int]
    PATIENT_ID_FIELD_NUMBER: _ClassVar[int]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    ENCOUNTER_TYPE_FIELD_NUMBER: _ClassVar[int]
    DEPARTMENT_FIELD_NUMBER: _ClassVar[int]
    encounter_id: str
    patient_id: str
    start_date: str
    end_date: str
    encounter_type: str
    department: str
    def __init__(self, encounter_id: _Optional[str] = ..., patient_id: _Optional[str] = ..., start_date: _Optional[str] = ..., end_date: _Optional[str] = ..., encounter_type: _Optional[str] = ..., department: _Optional[str] = ...) -> None: ...

class ClinicalEvent(_message.Message):
    __slots__ = ("event_id", "patient_id", "encounter_id", "event_type", "event_code", "description", "event_date", "value", "unit")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    PATIENT_ID_FIELD_NUMBER: _ClassVar[int]
    ENCOUNTER_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    EVENT_CODE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    EVENT_DATE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    patient_id: str
    encounter_id: str
    event_type: str
    event_code: str
    description: str
    event_date: str
    value: str
    unit: str
    def __init__(self, event_id: _Optional[str] = ..., patient_id: _Optional[str] = ..., encounter_id: _Optional[str] = ..., event_type: _Optional[str] = ..., event_code: _Optional[str] = ..., description: _Optional[str] = ..., event_date: _Optional[str] = ..., value: _Optional[str] = ..., unit: _Optional[str] = ...) -> None: ...

class TransformRequest(_message.Message):
    __slots__ = ("patient", "encounters", "clinical_events")
    PATIENT_FIELD_NUMBER: _ClassVar[int]
    ENCOUNTERS_FIELD_NUMBER: _ClassVar[int]
    CLINICAL_EVENTS_FIELD_NUMBER: _ClassVar[int]
    patient: Patient
    encounters: _containers.RepeatedCompositeFieldContainer[Encounter]
    clinical_events: _containers.RepeatedCompositeFieldContainer[ClinicalEvent]
    def __init__(self, patient: _Optional[_Union[Patient, _Mapping]] = ..., encounters: _Optional[_Iterable[_Union[Encounter, _Mapping]]] = ..., clinical_events: _Optional[_Iterable[_Union[ClinicalEvent, _Mapping]]] = ...) -> None: ...

class TransformResponse(_message.Message):
    __slots__ = ("fhir_bundle_json",)
    FHIR_BUNDLE_JSON_FIELD_NUMBER: _ClassVar[int]
    fhir_bundle_json: str
    def __init__(self, fhir_bundle_json: _Optional[str] = ...) -> None: ...

class AggregateRequest(_message.Message):
    __slots__ = ("cohort_code", "patients", "clinical_events")
    COHORT_CODE_FIELD_NUMBER: _ClassVar[int]
    PATIENTS_FIELD_NUMBER: _ClassVar[int]
    CLINICAL_EVENTS_FIELD_NUMBER: _ClassVar[int]
    cohort_code: str
    patients: _containers.RepeatedCompositeFieldContainer[Patient]
    clinical_events: _containers.RepeatedCompositeFieldContainer[ClinicalEvent]
    def __init__(self, cohort_code: _Optional[str] = ..., patients: _Optional[_Iterable[_Union[Patient, _Mapping]]] = ..., clinical_events: _Optional[_Iterable[_Union[ClinicalEvent, _Mapping]]] = ...) -> None: ...

class AggregateResponse(_message.Message):
    __slots__ = ("fhir_bundle_json",)
    FHIR_BUNDLE_JSON_FIELD_NUMBER: _ClassVar[int]
    fhir_bundle_json: str
    def __init__(self, fhir_bundle_json: _Optional[str] = ...) -> None: ...
