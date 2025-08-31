from dataclasses import dataclass
from src.models.option import Option
from src.models.user import User

@dataclass
class Options:
  options: list[Option]

  def add_option(self, option: Option):
      self.options.append(option)

  def remove_option(self, option: Option):
      self.options.remove(option)

  def show_options(self, user: User):
      options_to_show = list(filter(lambda opt: not opt.admin_only or user.is_admin, self.options))
      for idx, option in enumerate(options_to_show):
          print(f"{idx + 1}. {option.text}")

  def execute_option(self, index: int) -> bool:
      option_selected = index - 1
      if 0 <= option_selected < len(self.options):
          self.options[option_selected].execute_action()
          return True
      print("Invalid option.")
      return False
