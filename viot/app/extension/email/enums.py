from enum import Enum, auto


class TemplateType(Enum):
    VERIFY_ACCOUNT = auto()
    RESET_PASSWORD = auto()
    TEAM_INVITATION = auto()
