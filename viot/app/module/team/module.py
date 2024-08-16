from injector import Binder, Module, SingletonScope

from .controller import TeamController
from .repository import TeamRepository, UserTeamRepository
from .service import TeamService


class TeamModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(TeamRepository, TeamRepository, SingletonScope)
        binder.bind(UserTeamRepository, UserTeamRepository, SingletonScope)
        binder.bind(TeamService, TeamService, SingletonScope)
        binder.bind(TeamController, TeamController, SingletonScope)
