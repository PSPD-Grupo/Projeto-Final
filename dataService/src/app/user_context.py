from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class UserContext:
    username: str
    roles: set[str]
    scopes: set[str]
    request_id: str | None = None

    @property
    def has_global_patient_read(self) -> bool:
        return "ADMIN" in self.roles or "patient:read:all" in self.scopes


def _split_header(value: str | None) -> set[str]:
    if not value:
        return set()
    return {item.strip() for item in value.split(",") if item.strip()}


def user_context_from_metadata(metadata: Iterable[tuple[str, str]]) -> UserContext:
    values = {key.lower(): value for key, value in metadata}
    return UserContext(
        username=values.get("x-user-username", ""),
        roles=_split_header(values.get("x-user-roles")),
        scopes=_split_header(values.get("x-user-scopes")),
        request_id=values.get("x-request-id"),
    )
