from typing import Optional, Dict
from ..models.user import User


class AuthService:

    def __init__(self):
        self.users_db = [
            User(username="admin", password="admin123", is_admin=True),
            User(username="user1", password="password123", is_admin=False),
            User(username="user2", password="mypassword", is_admin=False),
            User(username="manager", password="manager456", is_admin=True),
        ]

    def authenticate(self, username: str, password: str) -> Optional[User]:
        if not username or not password:
            return None

        user : User = next((u for u in self.users_db if u.username == username), None)
        if not user or  user.password != password:
            return None
        authenticated_user = user
        return authenticated_user

    def create_user(self, username: str, password: str, is_admin: bool = False) -> bool:

        if username in self.users_db:
            return False
        
        user = User(username=username, password=password, is_admin=is_admin)
        self.users_db.append(user)
        return True

    def validate_credentials_format(self, username: str, password: str) -> bool:

        if not username or not password:
            return False

        if len(username) < 3 or len(password) < 6:
            return False

        if not username.isalnum():
            return False

        return True
