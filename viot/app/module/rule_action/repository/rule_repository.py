from uuid import UUID

from sqlalchemy import delete, select

from app.database.repository import PageableRepository

from ..model.rule import Rule


class RuleRepository(PageableRepository[Rule, UUID]):
    async def find_by_team_id_and_rule_id(self, *, team_id: UUID, rule_id: UUID) -> Rule | None:
        stmt = select(Rule).where(Rule.team_id == team_id, Rule.id == rule_id)
        return (await self.session.execute(stmt)).scalar()

    async def delete_by_team_id_and_rule_id(self, *, team_id: UUID, rule_id: UUID) -> None:
        stmt = delete(Rule).where(Rule.team_id == team_id, Rule.id == rule_id)
        await self.session.execute(stmt)
