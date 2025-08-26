from interfaces.price_rule_interface import PriceRuleInterface


class RulesManager:

  rules: list[PriceRuleInterface] = []

  def rules_handler(self):
    pass

  @staticmethod
  def get_rule(sku: str) -> PriceRuleInterface:
    for rule in RulesManager.rules:
      if rule.is_applicable(sku):
        return rule
    return None