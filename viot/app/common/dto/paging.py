from math import ceil
from typing import Generic, TypeVar

from pydantic import computed_field

from .base import BaseOutDto

T = TypeVar("T", bound=BaseOutDto)


class PagingDto(BaseOutDto, Generic[T]):
    """Paging DTO"""

    items: list[T]
    total_items: int
    page: int
    page_size: int

    @computed_field  # type: ignore
    @property
    def total_pages(self) -> int:
        return ceil(self.total_items / self.page_size)

    @computed_field  # type: ignore
    @property
    def has_next_page(self) -> bool:
        return self.page < self.total_pages

    @computed_field  # type: ignore
    @property
    def has_previous_page(self) -> bool:
        return self.page > 1
