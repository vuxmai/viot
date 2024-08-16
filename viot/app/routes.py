from fastapi import APIRouter

from app.container import injector
from app.module.auth.controller import AuthController
from app.module.team.controller import TeamController
from app.module.team_invitation.controller import TeamInvitationController
from app.module.user.controller import UserController

router = APIRouter()


router.include_router(injector.get(AuthController).router)
router.include_router(injector.get(UserController).router)
router.include_router(injector.get(TeamController).router)
router.include_router(injector.get(TeamInvitationController).router)
