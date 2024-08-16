from math import ceil
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, computed_field
from pydantic.alias_generators import to_camel

TPagingModel = TypeVar("TPagingModel", bound="BaseOutDto")


class ViotDto(BaseModel):
    """Base model"""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class BaseInDto(ViotDto):
    """Base input model"""

    model_config = ConfigDict(use_enum_values=True)


class BaseOutDto(ViotDto):
    """Base output model"""

    model_config = ConfigDict(from_attributes=True)


class ErrorDto(BaseOutDto):
    """Error response model"""

    status: int
    error_code: str
    message: Any


class BasePagingDto(BaseOutDto, Generic[TPagingModel]):
    """Base paging model"""

    items: list[TPagingModel]
    total_items: int
    page: int
    items_per_page: int

    @computed_field
    @property
    def total_pages(self) -> int:
        return ceil(self.total_items / self.items_per_page)

    @property
    def has_next_page(self) -> bool:
        return self.page < self.total_pages

    @property
    def has_previous_page(self) -> bool:
        return self.page > 1
