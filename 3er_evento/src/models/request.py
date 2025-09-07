from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime
from ..models.user import User


@dataclass
class Request:
    method: str
    path: str
    headers: Dict[str, str]
    body: Dict[str, Any]
    ip_address: str
    timestamp: datetime
    user_credentials: Optional[Dict[str, str]] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def set_authenticated_user(self, user: 'User'):
        self.authenticated_user = user