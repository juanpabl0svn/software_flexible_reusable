from dataclasses import dataclass
from typing import Dict, Any
from ..enum.status_code import StatusCode


@dataclass
class Response:
    status_code: StatusCode
    headers: Dict[str, str]
    body: Dict[str, Any]
    is_from_cache: bool = False
    
    def __post_init__(self):
        if not self.headers:
            self.headers = {"Content-Type": "application/json"}