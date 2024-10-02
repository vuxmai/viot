from fastapi import APIRouter

from app import injector
from app.common.exception.constant import RESPONSE_SCHEMAS
from app.module.auth.controller.auth_controller import AuthController
from app.module.auth.controller.permission_controller import PermissionController
from app.module.auth.controller.team_role_controller import TeamRoleController
from app.module.auth.controller.user_controller import UserController
from app.module.device.controller.device_controller import DeviceController
from app.module.team.controller.member_controller import MemberController
from app.module.team.controller.team_controller import TeamController
from app.module.team.controller.team_invitation_controller import TeamInvitationController

api_router = APIRouter(responses=RESPONSE_SCHEMAS)
authenticate_router = APIRouter()

authenticate_router.include_router(injector.get(AuthController).router)
api_router.include_router(injector.get(UserController).router)
api_router.include_router(injector.get(TeamController).router)
api_router.include_router(injector.get(TeamRoleController).router)
api_router.include_router(injector.get(PermissionController).router)
api_router.include_router(injector.get(TeamInvitationController).router)
api_router.include_router(injector.get(MemberController).router)
api_router.include_router(injector.get(DeviceController).router)

router = APIRouter()
router.include_router(authenticate_router)
router.include_router(api_router)
