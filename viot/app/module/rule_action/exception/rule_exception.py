from app.common.exception import NotFoundException


class RuleNotFoundException(NotFoundException):
    def __init__(self, *, rule_id: str) -> None:
        super().__init__(code="RULE_NOT_FOUND", message=f"Rule with id {rule_id} not found")
