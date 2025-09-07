from dataclasses import dataclass


@dataclass
class User:
    username: str
    password: str
    is_admin: bool = False
    is_authenticated: bool = False