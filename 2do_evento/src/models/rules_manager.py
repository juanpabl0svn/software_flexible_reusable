from src.interfaces.price_rule_interface import PriceRuleInterface


class RulesManager:

  rules: list[PriceRuleInterface] = []

  @staticmethod
  def add_rule(rule: PriceRuleInterface):
    RulesManager.rules.append(rule)

  @staticmethod
  def get_rule(sku: str) -> PriceRuleInterface:
    if not RulesManager.rules:
      raise ValueError("No pricing rules available")
    for rule in RulesManager.rules:
      if rule.is_applicable(sku):
        return rule
    return None