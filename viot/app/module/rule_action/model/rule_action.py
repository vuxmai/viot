from uuid import UUID

from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class RuleAction(Base):
    __tablename__ = "rule_actions"

    rule_id: Mapped[UUID] = mapped_column(
        ForeignKey("rules.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    action_id: Mapped[UUID] = mapped_column(
        ForeignKey("actions.id", onupdate="CASCADE", ondelete="CASCADE")
    )

    __table_args__ = (PrimaryKeyConstraint("rule_id", "action_id"),)
