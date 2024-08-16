from collections.abc import Sequence
from typing import Any, Generic, Literal, TypeVar

import msgspec
from sqlalchemy import Column, ColumnElement, and_, func, select
from sqlalchemy.sql import Select, asc, desc

from app.database.repository.crud import CrudRepository

from .crud import TBaseModel, TModel, TPrimaryKey

SortDirection = Literal["asc", "desc"]
FilterOperator = Literal[
    "eq",
    "ne",
    "gt",
    "lt",
    "gte",
    "lte",
    "in",
    "nin",
    "like",
    "nlike",
    "ilike",
    "nilike",
    "is",
    "isnot",
    "isnull",
    "isnotnull",
]

TSelect = TypeVar("TSelect", bound=tuple[Any, ...])


class Sort:
    def __init__(self, field: str, direction: SortDirection = "asc") -> None:
        self.field = field
        self.direction = direction.lower()

    def apply(self, query: Select[TSelect]) -> Select[TSelect]:
        order_func = asc if self.direction == "asc" else desc
        return query.order_by(order_func(self.field))


class Filter:
    def __init__(self, field: str, operator: FilterOperator, value: Any) -> None:
        self.field = field
        self.operator = operator
        self.value = value

    def apply(self, model: type[TModel]) -> ColumnElement[Any]:
        column: Column[Any] = getattr(model, self.field)
        match self.operator:
            case "eq":
                return column == self.value
            case "ne":
                return column != self.value
            case "gt":
                return column > self.value
            case "lt":
                return column < self.value
            case "gte":
                return column >= self.value
            case "lte":
                return column <= self.value
            case "in":
                return column.in_(self.value)
            case "nin":
                return column.not_in(self.value)
            case "like":
                return column.like(self.value)
            case "nlike":
                return column.not_like(self.value)
            case "ilike":
                return column.ilike(self.value)
            case "nilike":
                return column.not_ilike(self.value)
            case "is":
                return column.is_(self.value)
            case "isnot":
                return column.isnot(self.value)
            case "isnull":
                return column.is_(None)
            case "isnotnull":
                return column.isnot(None)
            case _:
                raise ValueError(f"Unsupported operator: {self.operator}")


class Pageable:
    def __init__(
        self,
        page: int = 1,
        page_size: int = 20,
        sorts: list[Sort] | None = None,
        filters: list[Filter] | None = None,
    ) -> None:
        self.page = max(1, page)
        self.page_size = max(1, min(10, page_size))
        self.sorts = sorts or []
        self.filters = filters or []

    def apply(self, query: Select[TSelect], model: type[TModel]) -> Select[TSelect]:
        # Apply filters
        if self.filters:
            filter_conditions = [filter.apply(model) for filter in self.filters]
            query = query.where(and_(*filter_conditions))

        # Apply sorting
        for sort in self.sorts:
            query = sort.apply(query)

        # Apply pagination
        return query.offset((self.page - 1) * self.page_size).limit(self.page_size)


class Page(msgspec.Struct, Generic[TModel]):
    items: Sequence[TModel]
    total_items: int
    page: int
    page_size: int


class PageableRepository(CrudRepository[TBaseModel, TPrimaryKey]):
    async def find_all_with_paging(self, pageable: Pageable) -> Page[TBaseModel]:
        # Base query for selecting items
        base_query = select(self._model)

        # Apply filters, sorting, and pagination
        query = pageable.apply(base_query, self._model)

        # Count query (apply only filters)
        count_query = select(func.count()).select_from(
            pageable.apply(base_query, self._model).order_by(None).limit(None).subquery()
        )

        # Execute queries
        items = (await self.session.execute(query)).scalars().all()
        total_items = (await self.session.execute(count_query)).scalar_one()

        return Page(
            items=items, total_items=total_items, page=pageable.page, page_size=pageable.page_size
        )
