import msgspec

from .model import Team


class TeamWithRole(msgspec.Struct, frozen=True):
    team: Team
    role: str
