import re
from typing import Optional, Dict, Any
from ..interface.request_handler import RequestHandler
from ..models.request import Request
from ..models.response import Response
from ..enum.status_code import StatusCode


class DataValidationHandler(RequestHandler):
    
    def __init__(self):
        super().__init__()
        self.dangerous_patterns = [
            r'<script.*?>.*?</script>',  # Scripts XSS
            r'javascript:',              # JavaScript URLs
            r'on\w+\s*=',               # Event handlers
            r'SELECT.*FROM',            # SQL injection básica
            r'DROP\s+TABLE',            # SQL injection
            r'INSERT\s+INTO',           # SQL injection
            r'DELETE\s+FROM',           # SQL injection
            r'\.\./.*',                 # Directory traversal
            r'exec\(',                  # Code execution
            r'eval\(',                  # Code evaluation
        ]
    
    def handle(self, request: Request) -> Optional[Response]:
        
        if not self._validate_headers(request.headers):
            return Response(
                status_code=StatusCode.BAD_REQUEST,
                headers={},
                body={"error": "Headers inválidos", "code": "INVALID_HEADERS"}
            )
        
        if not self._validate_and_sanitize_body(request):
            return Response(
                status_code=StatusCode.BAD_REQUEST,
                headers={},
                body={"error": "Datos de entrada inválidos", "code": "INVALID_DATA"}
            )
        
        return self._pass_to_next(request)
    
    def _validate_headers(self, headers: Dict[str, str]) -> bool:

        for _, header_value in headers.items():
            if self._contains_dangerous_content(header_value):
                return False
        return True
    
    def _validate_and_sanitize_body(self, request: Request) -> bool:

        if not request.body:
            return True
        
        sanitized_body = {}
        
        for key, value in request.body.items():
            if isinstance(value, str):
                if self._contains_dangerous_content(value):
                    return False
                
                sanitized_value = self._sanitize_string(value)
                sanitized_body[key] = sanitized_value
            else:
                sanitized_body[key] = value
        
        request.body = sanitized_body
        return True
    
    def _contains_dangerous_content(self, content: str) -> bool:
        content_lower = content.lower()
        
        for pattern in self.dangerous_patterns:
            if re.search(pattern, content_lower, re.IGNORECASE):
                return True
        
        return False
    
    def _sanitize_string(self, value: str) -> str:

        value = value.replace("<", "&lt;")
        value = value.replace(">", "&gt;")
        value = value.replace("&", "&amp;")
        value = value.replace('"', "&quot;")
        value = value.replace("'", "&#x27;")
        
        value = re.sub(r'[\x00-\x1F\x7F]', '', value)
        
        return value.strip()
