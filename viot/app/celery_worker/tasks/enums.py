from enum import StrEnum


class EmailTaskType(StrEnum):
    VERIFY_ACCOUNT = "send_verify_account_email"
    RESET_PASSWORD = "send_reset_password_email"
    TEAM_INVITATION = "send_team_invitation_email"
