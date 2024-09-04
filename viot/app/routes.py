from fastapi import APIRouter

from app import injector
from app.module.auth.controller.auth_controller import AuthController
from app.module.auth.controller.user_controller import UserController
from app.module.team.controller.team_controller import TeamController
from app.module.team.controller.team_invitation_controller import TeamInvitationController

router = APIRouter()


router.include_router(injector.get(AuthController).router)
router.include_router(injector.get(UserController).router)
router.include_router(injector.get(TeamController).router)
router.include_router(injector.get(TeamInvitationController).router)
