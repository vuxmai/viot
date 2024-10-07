from injector import Binder, Module, SingletonScope

from .controller.device_data_controller import DeviceDataController
from .repository.device_attribute_repository import DeviceAttributeRepository
from .repository.device_data_aggregation_repository import DeviceDataAggregationRepository
from .repository.device_data_latest_repository import DeviceDataLatestRepository
from .repository.device_data_repository import DeviceDataRepository
from .service.device_attribute_service import DeviceAttributeService
from .service.device_data_service import DeviceDataService


class DeviceDataModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(DeviceDataRepository, to=DeviceDataRepository, scope=SingletonScope)
        binder.bind(DeviceDataLatestRepository, to=DeviceDataLatestRepository, scope=SingletonScope)
        binder.bind(DeviceAttributeRepository, to=DeviceAttributeRepository, scope=SingletonScope)
        binder.bind(
            DeviceDataAggregationRepository,
            to=DeviceDataAggregationRepository,
            scope=SingletonScope,
        )

        binder.bind(DeviceDataService, to=DeviceDataService, scope=SingletonScope)
        binder.bind(DeviceAttributeService, to=DeviceAttributeService, scope=SingletonScope)

        binder.bind(DeviceDataController, to=DeviceDataController, scope=SingletonScope)
