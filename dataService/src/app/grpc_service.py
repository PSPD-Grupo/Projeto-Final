import sys
from pathlib import Path

import grpc

from app.mappers import clinical_event_message, encounter_message, patient_message
from app.repositories import PatientRepository
from app.user_context import user_context_from_metadata

generated_dir = Path(__file__).resolve().parents[1] / "generated"
if str(generated_dir) not in sys.path:
    sys.path.insert(0, str(generated_dir))

import patient_data_pb2 as pb2
import patient_data_pb2_grpc as pb2_grpc


class PatientDataGrpcService(pb2_grpc.PatientDataServiceServicer):
    def __init__(self, repository: PatientRepository) -> None:
        self._repository = repository

    async def HealthCheck(self, request, context):
        return pb2.HealthCheckResponse(status="SERVING")

    async def GetPatient(self, request, context):
        user_context = user_context_from_metadata(context.invocation_metadata())
        patient = await self._repository.get_patient(user_context, request.patient_id)
        if patient is None:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Patient not found or access denied")
        return pb2.GetPatientResponse(patient=patient_message(pb2, patient))

    async def SearchPatients(self, request, context):
        user_context = user_context_from_metadata(context.invocation_metadata())
        patients = await self._repository.search_patients(
            user_context,
            request.query,
            request.limit,
            request.offset,
        )
        return pb2.SearchPatientsResponse(
            patients=[patient_message(pb2, patient) for patient in patients]
        )

    async def ListEncounters(self, request, context):
        user_context = user_context_from_metadata(context.invocation_metadata())
        encounters = await self._repository.list_encounters(
            user_context,
            request.patient_id,
            request.limit,
            request.offset,
        )
        if encounters is None:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Patient not found or access denied")
        return pb2.ListEncountersResponse(
            encounters=[encounter_message(pb2, encounter) for encounter in encounters]
        )

    async def ListClinicalEvents(self, request, context):
        user_context = user_context_from_metadata(context.invocation_metadata())
        events = await self._repository.list_clinical_events(
            user_context,
            request.patient_id,
            request.encounter_id,
            request.event_type,
            request.limit,
            request.offset,
        )
        if events is None:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Patient not found or access denied")
        return pb2.ListClinicalEventsResponse(
            events=[clinical_event_message(pb2, event) for event in events]
        )


def register_patient_data_service(server: grpc.aio.Server, repository: PatientRepository) -> None:
    pb2_grpc.add_PatientDataServiceServicer_to_server(
        PatientDataGrpcService(repository),
        server,
    )
