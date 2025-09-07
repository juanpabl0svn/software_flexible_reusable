"""
Handler para manejo de caché de respuestas
"""
import hashlib
import json
from typing import Optional, Dict
from datetime import datetime, timedelta
from ..interface.request_handler import RequestHandler
from ..models.request import Request
from ..models.response import Response


class CacheHandler(RequestHandler):

    
    def __init__(self, cache_duration: int = 300):
        super().__init__()
        self.cache_duration = cache_duration
        self.cache: Dict[str, Dict] = {}
    
    def handle(self, request: Request) -> Optional[Response]:
        if request.method.upper() != "GET":
            return self._pass_to_next(request)
        
        cache_key = self._generate_cache_key(request)
        
        cached_response = self._get_from_cache(cache_key)
        if cached_response:
            cached_response.is_from_cache = True
            return cached_response
        
        response = self._pass_to_next(request)
        
        if response and response.status_code.value >= 200 and response.status_code.value < 300:
            self._store_in_cache(cache_key, response)
        
        return response
    
    def _generate_cache_key(self, request: Request) -> str:
        cache_data = {
            "method": request.method,
            "path": request.path,
            "body": request.body,
            "user": request.authenticated_user.username if hasattr(request, 'authenticated_user') and request.authenticated_user else None
        }
        
        cache_string = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def _get_from_cache(self, cache_key: str) -> Optional[Response]:
        if cache_key not in self.cache:
            return None
        
        cached_item = self.cache[cache_key]
        cached_time = cached_item["timestamp"]
        current_time = datetime.now()
        
        if current_time - cached_time > timedelta(seconds=self.cache_duration):
            del self.cache[cache_key]
            return None
        
        cached_response = cached_item["response"]
        return Response(
            status_code=cached_response.status_code,
            headers=cached_response.headers.copy(),
            body=cached_response.body.copy() if isinstance(cached_response.body, dict) else cached_response.body,
            is_from_cache=True
        )
    
    def _store_in_cache(self, cache_key: str, response: Response):
        cached_response = Response(
            status_code=response.status_code,
            headers=response.headers.copy(),
            body=response.body.copy() if isinstance(response.body, dict) else response.body
        )
        
        self.cache[cache_key] = {
            "response": cached_response,
            "timestamp": datetime.now()
        }
        
        if len(self.cache) > 100:
            self._cleanup_old_cache()
    
    def _cleanup_old_cache(self):

        current_time = datetime.now()
        keys_to_remove = []
        
        for key, cached_item in self.cache.items():
            cached_time = cached_item["timestamp"]
            if current_time - cached_time > timedelta(seconds=self.cache_duration):
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self.cache[key]