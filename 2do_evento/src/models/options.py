from dataclasses import dataclass
from src.models.option import Option

@dataclass
class Options:
  options: list[Option]

  def add_option(self, option: Option):
      self.options.append(option)

  def remove_option(self, option: Option):
      self.options.remove(option)

  def show_options(self):
      for idx, option in enumerate(self.options):
          print(f"{idx + 1}. {option.text}")

  def execute_option(self, index: int) -> bool:
      option_selected = index - 1
      if 0 <= index < len(self.options):
          self.options[option_selected].execute_action()
          return True
      print("Invalid option.")
      return False
