from injector import Binder, Module, SingletonScope

from .controller.device_controller import DeviceController
from .repository.device_repository import DeviceRepository
from .service.device_service import DeviceService


class DeviceModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(DeviceRepository, to=DeviceRepository, scope=SingletonScope)
        binder.bind(DeviceService, to=DeviceService, scope=SingletonScope)
        binder.bind(DeviceController, to=DeviceController, scope=SingletonScope)
