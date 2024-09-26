from injector import Binder, Module, SingletonScope

from .controller.team_controller import TeamController
from .controller.team_invitation_controller import TeamInvitationController
from .repository.team_invitation_repository import TeamInvitationRepository
from .repository.team_repository import TeamRepository
from .repository.user_team_repository import UserTeamRepository
from .service.member_service import MemberService
from .service.team_invitation_service import TeamInvitationService
from .service.team_service import TeamService


class TeamModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(TeamRepository, TeamRepository, SingletonScope)
        binder.bind(UserTeamRepository, UserTeamRepository, SingletonScope)
        binder.bind(TeamInvitationRepository, TeamInvitationRepository, SingletonScope)

        binder.bind(TeamService, TeamService, SingletonScope)
        binder.bind(MemberService, MemberService, SingletonScope)
        binder.bind(TeamInvitationService, TeamInvitationService, SingletonScope)

        binder.bind(TeamController, TeamController, SingletonScope)
        binder.bind(TeamInvitationController, TeamInvitationController, SingletonScope)
