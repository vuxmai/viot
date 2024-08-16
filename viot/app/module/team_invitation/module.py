from injector import Binder, Module, SingletonScope

from .repository import TeamInvitationRepository
from .service import TeamInvitationService


class TeamInvitationModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(TeamInvitationRepository, TeamInvitationRepository, SingletonScope)
        binder.bind(TeamInvitationService, TeamInvitationService, SingletonScope)
