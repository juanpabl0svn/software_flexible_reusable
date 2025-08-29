from dataclasses import dataclass
from typing import Callable, Optional

@dataclass
class Option:
  text: str
  action: Optional[Callable] = None

  def set_action(self, action: Callable):
    self.action = action

  def execute_action(self):
      if not self.action:
         raise ValueError("No action defined for this option.")
      
      self.action()
      
