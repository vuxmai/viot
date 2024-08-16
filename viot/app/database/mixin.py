import uuid
from datetime import datetime
from typing import Annotated
from uuid import UUID

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column
from sqlalchemy.types import UUID as UUIDType

PrimaryKey = Annotated[
    UUID,
    mapped_column(
        UUIDType(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        sort_order=-999,
    ),
]
"""

Usage:
    class User(Base):
        id: Mapped[PrimaryKey] = mapped_column(init=False)
        # other fields...
"""


class DateTimeMixin(MappedAsDataclass):
    """Mixin for DateTime"""

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default_factory=lambda: datetime.now().replace(tzinfo=None),
        sort_order=998,
        init=False,
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        onupdate=lambda: datetime.now().replace(tzinfo=None),
        nullable=True,
        sort_order=999,
        init=False,
    )
