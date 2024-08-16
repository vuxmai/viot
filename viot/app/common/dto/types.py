from typing import Annotated

from fastapi import Query
from pydantic import StringConstraints

NameStr = Annotated[
    str,
    StringConstraints(pattern=r"^[a-zA-Z ]+$", strip_whitespace=True, min_length=2, max_length=20),
]
NameWithNumberStr = Annotated[
    str,
    StringConstraints(
        pattern=r"^[a-zA-Z0-9 ]+$", strip_whitespace=True, min_length=4, max_length=32
    ),
]
TeamSlug = Annotated[
    str,
    StringConstraints(
        pattern=r"^[a-z0-9]+(?:(?:-|_)+[a-z0-9]+)*$",
        strip_whitespace=True,
        min_length=1,
        max_length=50,
    ),
]
QueryStr = Annotated[str, StringConstraints(pattern=r"^[ -~]+$", min_length=1)]


# Paging
PageQuery = Annotated[int, Query(ge=1, alias="page")]
PageSizeQuery = Annotated[int, Query(ge=1, alias="pageSize")]
