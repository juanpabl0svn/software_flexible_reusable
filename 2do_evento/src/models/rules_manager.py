from src.interfaces.price_rule_interface import IPriceRule


class RulesManager:

  rules: list[IPriceRule] = []

  @staticmethod
  def add_rule(rule: IPriceRule):
    RulesManager.rules.append(rule)

  @staticmethod
  def get_rule(sku: str) -> IPriceRule:
    if not RulesManager.rules:
      raise ValueError("No pricing rules available")
    for rule in RulesManager.rules:
      if rule.is_applicable(sku):
        return rule
    return None