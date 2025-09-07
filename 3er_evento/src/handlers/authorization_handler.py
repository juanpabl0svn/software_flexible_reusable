from typing import Optional
from ..interface.request_handler import RequestHandler
from ..models.request import Request
from ..models.response import Response
from ..enum.status_code import StatusCode


class AuthorizationHandler(RequestHandler):
    def __init__(self, routes_requiring_admin = None):
        super().__init__()
        if routes_requiring_admin is None:
            self.admin_required_paths = [
                "/admin",
                "/users/delete", 
                "/orders/admin",
                "/system/config"
            ]
        else:
            self.admin_required_paths = routes_requiring_admin
    
    def handle(self, request: Request) -> Optional[Response]:
        if not hasattr(request, 'authenticated_user') or not request.authenticated_user:
            return Response(
                status_code=StatusCode.UNAUTHORIZED,
                headers={},
                body={"error": "Usuario no autenticado", "code": StatusCode.UNAUTHORIZED}
            )
        
        user = request.authenticated_user
        
        if self._requires_admin_permission(request.path, request.method):
            if not user.is_admin:
                return Response(
                    status_code=StatusCode.FORBIDDEN,
                    headers={},
                    body={"error": "Permisos insuficientes", "code": StatusCode.FORBIDDEN}
                )
        
        
        return self._pass_to_next(request)
    
    def _requires_admin_permission(self, path: str, method: str) -> bool:
        if method.upper() == "DELETE":
            return True
            
        return any(admin_path in path for admin_path in self.admin_required_paths)
