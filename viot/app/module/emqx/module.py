from injector import Binder, Module, SingletonScope

from .controller.emqx_device_controller import EmqxDeviceController
from .service.emqx_auth_service import EmqxDeviceAuthService
from .service.emqx_event_service import EmqxEventService
from .service.emqx_rule_service import EmqxRuleService
from .service.mqtt_whitelist_service import MqttWhitelistService


class EmqxModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(EmqxDeviceAuthService, to=EmqxDeviceAuthService, scope=SingletonScope)
        binder.bind(EmqxEventService, to=EmqxEventService, scope=SingletonScope)
        binder.bind(MqttWhitelistService, to=MqttWhitelistService, scope=SingletonScope)
        binder.bind(EmqxRuleService, to=EmqxRuleService, scope=SingletonScope)

        binder.bind(EmqxDeviceController, to=EmqxDeviceController, scope=SingletonScope)
