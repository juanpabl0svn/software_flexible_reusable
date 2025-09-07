from typing import Optional, Dict
from ..models.request import Request
from ..models.response import Response
from ..services.auth_service import AuthService
from ..enum.status_code import StatusCode
from ..interface.request_handler import RequestHandler
from ..interface.extraction_method import ExtractionMethod


class AuthenticationHandler(RequestHandler):
    extraction_method: ExtractionMethod

    def __init__(self, extraction_method: ExtractionMethod):
        super().__init__()
        self.auth_service = AuthService()
        self.extraction_method = extraction_method

    def handle(self, request: Request) -> Optional[Response]:
        credentials = self.extraction_method.extract(request)
        
        if not credentials and hasattr(request, 'user_credentials') and request.user_credentials:
            credentials = request.user_credentials

        if not credentials:
            return Response(
                status_code=StatusCode.UNAUTHORIZED,
                headers={},
                body={"error": "Credenciales requeridas",
                      "code": StatusCode.UNAUTHORIZED}
            )

        user = self.auth_service.authenticate(
            credentials.get("username"),
            credentials.get("password")
        )

        if not user:
            return Response(
                status_code=StatusCode.UNAUTHORIZED,
                headers={},
                body={"error": "Credenciales inválidas",
                      "code": StatusCode.UNAUTHORIZED}
            )

        request.set_authenticated_user(user)

        return self._pass_to_next(request)       