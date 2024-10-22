from fastapi import APIRouter

from app import injector
from app.common.exception.constant import RESPONSE_SCHEMAS
from app.config import app_settings
from app.module.auth.controller.auth_controller import AuthController
from app.module.auth.controller.permission_controller import PermissionController
from app.module.auth.controller.team_role_controller import TeamRoleController
from app.module.auth.controller.user_controller import UserController
from app.module.device.controller.device_controller import DeviceController
from app.module.device_data.controller.connect_log_controller import ConnectLogController
from app.module.device_data.controller.device_data_controller import DeviceDataController
from app.module.emqx.controller.emqx_device_controller import EmqxDeviceController
from app.module.rule_action.controller.rule_controller import RuleController
from app.module.team.controller.member_controller import MemberController
from app.module.team.controller.team_controller import TeamController
from app.module.team.controller.team_invitation_controller import TeamInvitationController

api_router = APIRouter(prefix=app_settings.API_PREFIX, responses=RESPONSE_SCHEMAS)
internal_api_router = APIRouter(prefix=app_settings.API_INTERNAL_PREFIX, responses=RESPONSE_SCHEMAS)
authenticate_router = APIRouter()

authenticate_router.include_router(injector.get(AuthController).router)

api_router.include_router(injector.get(UserController).router)
api_router.include_router(injector.get(TeamController).router)
api_router.include_router(injector.get(TeamRoleController).router)
api_router.include_router(injector.get(PermissionController).router)
api_router.include_router(injector.get(TeamInvitationController).router)
api_router.include_router(injector.get(MemberController).router)
api_router.include_router(injector.get(DeviceController).router)
api_router.include_router(injector.get(ConnectLogController).router)
api_router.include_router(injector.get(DeviceDataController).router)
api_router.include_router(injector.get(RuleController).router)

internal_api_router.include_router(injector.get(EmqxDeviceController).router)

router = APIRouter()
router.include_router(authenticate_router)
router.include_router(api_router)
router.include_router(internal_api_router)
