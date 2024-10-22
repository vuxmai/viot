from injector import Binder, Module, SingletonScope

from .controller.rule_controller import RuleController
from .repository.rule_repository import RuleRepository
from .service.emqx_rule_builder_service import EmqxRuleBuilderService
from .service.rule_service import RuleService


class RuleActionModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(RuleRepository, to=RuleRepository, scope=SingletonScope)

        binder.bind(RuleService, to=RuleService, scope=SingletonScope)
        binder.bind(EmqxRuleBuilderService, to=EmqxRuleBuilderService, scope=SingletonScope)

        binder.bind(RuleController, to=RuleController, scope=SingletonScope)
