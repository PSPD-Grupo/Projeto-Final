from dataclasses import dataclass
from enum import StrEnum
from typing import Iterable


class UserRole(StrEnum):
    MEDICO = "MEDICO"
    ESTAGIARIO = "ESTAGIARIO"
    PESQUISADOR = "PESQUISADOR"


class AccessLevel(StrEnum):
    FULL = "FULL"
    PARTIAL = "PARTIAL"
    ANONYMIZED = "ANONYMIZED"
    AGGREGATED = "AGGREGATED"


@dataclass(frozen=True)
class UserContext:
    username: str
    roles: set[str]
    scopes: set[str]
    request_id: str | None = None

    @property
    def is_medico(self) -> bool:
        return UserRole.MEDICO in self.roles

    @property
    def is_estagiario(self) -> bool:
        return UserRole.ESTAGIARIO in self.roles

    @property
    def is_pesquisador(self) -> bool:
        return UserRole.PESQUISADOR in self.roles

    @property
    def can_read_identified_patients(self) -> bool:
        return self.is_medico or self.is_estagiario

    @property
    def can_read_research_data(self) -> bool:
        return self.is_pesquisador


def _split_header(value: str | None) -> set[str]:
    if not value:
        return set()
    return {item.strip().upper() for item in value.split(",") if item.strip()}


def user_context_from_metadata(metadata: Iterable[tuple[str, str]]) -> UserContext:
    values = {key.lower(): value for key, value in metadata}
    return UserContext(
        username=values.get("x-user-username", ""),
        roles=_split_header(values.get("x-user-roles")),
        scopes=_split_header(values.get("x-user-scopes")),
        request_id=values.get("x-request-id"),
    )
