from typing import Optional

from ..models.request import Request
from ..interface.extraction_method import ExtractionMethod


class ExtractBasic(ExtractionMethod):
    def extract(self, request: Request) -> Optional[dict]:
        try:
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Basic "):
                encoded = auth_header.replace("Basic ", "")
                username, password = encoded.split(":")
                return {"username": username, "password": password}
            return None
        except Exception as e:
            print(f"Error extracting basic auth: {e}")
            return None
