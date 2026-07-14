from dataclasses import dataclass
from enum import StrEnum



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
    role: UserRole
    access_level: AccessLevel

    @property
    def is_medico(self) -> bool:
        return self.role == UserRole.MEDICO

    @property
    def is_estagiario(self) -> bool:
        return self.role == UserRole.ESTAGIARIO

    @property
    def is_pesquisador(self) -> bool:
        return self.role == UserRole.PESQUISADOR

    @property
    def can_read_identified_patients(self) -> bool:
        return self.is_medico or self.is_estagiario

    @property
    def can_read_research_data(self) -> bool:
        return self.is_pesquisador



