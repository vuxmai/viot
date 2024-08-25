from typing import Any
from unittest.mock import Mock

import pytest
from sqlalchemy import Select
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.repository.pagination import Filter, FilterOperator, Pageable, Sort


class ProductTest(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]


def test_sort() -> None:
    sort = Sort(field="created_at", direction="asc")
    assert sort.field == "created_at"
    assert sort.direction == "asc"

    mock_query = Mock()
    sort.apply(mock_query)
    mock_query.order_by.assert_called_once()


def test_filter() -> None:
    filter = Filter("name", "eq", "test")
    assert filter.field == "name"
    assert filter.operator == "eq"
    assert filter.value == "test"

    result = filter.apply(ProductTest)
    assert result is not None


@pytest.mark.parametrize(
    "operator, value, expected",
    [
        ("eq", 5, "products.id = :id_1"),
        ("ne", 5, "products.id != :id_1"),
        ("gt", 5, "products.id > :id_1"),
        ("lt", 5, "products.id < :id_1"),
        ("gte", 5, "products.id >= :id_1"),
        ("lte", 5, "products.id <= :id_1"),
        ("in", [1, 2, 3], "products.id IN (__[POSTCOMPILE_id_1])"),
        ("nin", [1, 2, 3], "(products.id NOT IN (__[POSTCOMPILE_id_1]))"),
        ("like", "%test%", "products.name LIKE :name_1"),
        ("nlike", "%test%", "products.name NOT LIKE :name_1"),
        ("ilike", "%test%", "lower(products.name) LIKE lower(:name_1)"),
        ("nilike", "%test%", "lower(products.name) NOT LIKE lower(:name_1)"),
        ("is", None, "products.id IS NULL"),
        ("isnot", None, "products.id IS NOT NULL"),
        ("isnull", None, "products.id IS NULL"),
        ("isnotnull", None, "products.id IS NOT NULL"),
    ],
)
def test_filter_apply(operator: FilterOperator, value: Any, expected: str) -> None:
    field = "id" if operator not in ["like", "nlike", "ilike", "nilike"] else "name"
    filter = Filter(field, operator, value)
    result = filter.apply(ProductTest)
    assert str(result) == expected


def test_filter_apply_unsupported_operator() -> None:
    with pytest.raises(ValueError, match="Unsupported operator: invalid_op"):
        Filter("id", "invalid_op", 5).apply(ProductTest)  # type: ignore


def test_pageable() -> None:
    pageable = Pageable(page=2, page_size=5, sorts=[Sort("name")], filters=[Filter("id", "gt", 10)])
    assert pageable.page == 2
    assert pageable.page_size == 5
    assert len(pageable.sorts) == 1
    assert len(pageable.filters) == 1

    mock_query = Mock(spec=Select)

    result = pageable.apply(mock_query, ProductTest)  # type: ignore

    mock_query.where.assert_called_once()
    assert result is not None
