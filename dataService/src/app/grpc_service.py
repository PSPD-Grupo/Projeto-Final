import sys
from pathlib import Path

import grpc

from app.config import Settings
from app.mappers import (
    anonymized_lab_result_message,
    bucket_message,
    clinical_event_message,
    encounter_message,
    patient_record_message,
    research_project_message,
)
from app.repositories import PatientRepository


generated_dir = Path(__file__).resolve().parents[1] / "generated"
if str(generated_dir) not in sys.path:
    sys.path.insert(0, str(generated_dir))

import patient_data_pb2 as pb2
import patient_data_pb2_grpc as pb2_grpc


class PatientDataGrpcService(pb2_grpc.PatientDataServiceServicer):
    def __init__(self, repository: PatientRepository, settings: Settings) -> None:
        self._repository = repository
        self._settings = settings

    async def HealthCheck(self, request, context):
        return pb2.HealthCheckResponse(status="SERVING")

    async def GetPatient(self, request, context):
        user_context = context.user_context
        result = await self._repository.get_patient(user_context, request.patient_id)
        if result is None:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Patient not found or access denied")
        patient, access_level = result
        return pb2.GetPatientResponse(
            patient=patient_record_message(
                pb2,
                patient,
                access_level,
                self._settings.pseudonym_salt,
            )
        )

    async def SearchPatients(self, request, context):
        user_context = context.user_context
        patients = await self._repository.search_patients(
            user_context,
            request.query,
            request.limit,
            request.offset,
        )
        return pb2.SearchPatientsResponse(
            patients=[
                patient_record_message(pb2, patient, access_level, self._settings.pseudonym_salt)
                for patient, access_level in patients
            ]
        )

    async def ListEncounters(self, request, context):
        user_context = context.user_context
        result = await self._repository.list_encounters(
            user_context,
            request.patient_id,
            request.limit,
            request.offset,
        )
        if result is None:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Patient not found or access denied")
        encounters, _access_level = result
        return pb2.ListEncountersResponse(
            encounters=[
                encounter_message(pb2, encounter, _access_level, self._settings.pseudonym_salt)
                for encounter in encounters
            ]
        )

    async def ListClinicalEvents(self, request, context):
        user_context = context.user_context
        result = await self._repository.list_clinical_events(
            user_context,
            request.patient_id,
            request.encounter_id,
            request.event_type,
            request.limit,
            request.offset,
        )
        if result is None:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Patient not found or access denied")
        events, access_level = result
        return pb2.ListClinicalEventsResponse(
            events=[
                clinical_event_message(pb2, event, access_level, self._settings.pseudonym_salt)
                for event in events
            ]
        )

    async def ListResearchProjects(self, request, context):
        user_context = context.user_context
        projects = await self._repository.list_research_projects(user_context, request.status)
        if not user_context.can_read_research_data:
            await context.abort(grpc.StatusCode.PERMISSION_DENIED, "Research role required")
        return pb2.ListResearchProjectsResponse(
            projects=[research_project_message(pb2, project) for project in projects]
        )

    async def GetCohortStats(self, request, context):
        user_context = context.user_context
        result = await self._repository.get_cohort_stats(user_context, request.project_id)
        if result is None:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Project not found or access denied")

        project = result["project"]
        return pb2.GetCohortStatsResponse(
            access_level=pb2.AGGREGATED,
            project_id=project["project_id"],
            target_condition_code=project["target_condition_code"],
            total_patients=result["total_patients"],
            gender_distribution=[
                bucket_message(pb2, row) for row in result["gender_distribution"]
            ],
            age_distribution=[
                bucket_message(pb2, row) for row in result["age_distribution"]
            ],
            department_distribution=[
                bucket_message(pb2, row) for row in result["department_distribution"]
            ],
            hba1c_average=result["hba1c_average"] or 0,
            medication_frequency=[
                bucket_message(pb2, row) for row in result["medication_frequency"]
            ],
        )

    async def ListAnonymizedLabResults(self, request, context):
        user_context = context.user_context
        results = await self._repository.list_anonymized_lab_results(
            user_context,
            request.project_id,
            request.limit,
            request.offset,
        )
        if results is None:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Project not found or access denied")
        return pb2.ListAnonymizedLabResultsResponse(
            access_level=pb2.ANONYMIZED,
            results=[
                anonymized_lab_result_message(
                    pb2,
                    result["patient"],
                    result["exams"],
                    self._settings.pseudonym_salt,
                )
                for result in results
            ],
        )


def register_patient_data_service(
    server: grpc.aio.Server,
    repository: PatientRepository,
    settings: Settings,
) -> None:
    pb2_grpc.add_PatientDataServiceServicer_to_server(
        PatientDataGrpcService(repository, settings),
        server,
    )
