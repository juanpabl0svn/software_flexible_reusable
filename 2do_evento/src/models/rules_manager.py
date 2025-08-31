from src.interfaces.product_rule_interface import IProductRule


class RulesManager:

  rules: list[IProductRule] = []

  @staticmethod
  def add_rule(rule: IProductRule):
    RulesManager.rules.append(rule)

  @staticmethod
  def get_rule(sku: str) -> IProductRule:
    if not RulesManager.rules:
      raise ValueError("No pricing rules available")
    for rule in RulesManager.rules:
      if rule.is_applicable(sku):
        return rule
    return None