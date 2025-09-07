from typing import Optional, Dict
from datetime import datetime, timedelta
from ..interface.request_handler import RequestHandler
from ..models.request import Request
from ..models.response import Response
from ..enum.status_code import StatusCode


class BruteForceProtectionHandler(RequestHandler):
    
    def __init__(self, max_attempts: int = 5, block_duration: int = 300):
        super().__init__()
        self.max_attempts = max_attempts
        self.block_duration = block_duration
        self.failed_attempts: Dict[str, list] = {} 
        self.blocked_ips: Dict[str, datetime] = {} 
    
    def handle(self, request: Request) -> Optional[Response]:
        ip_address = request.ip_address
        current_time = datetime.now()
        
        if self._is_ip_blocked(ip_address, current_time):
            remaining_time = self._get_remaining_block_time(ip_address, current_time)
            return Response(
                status_code=StatusCode.TOO_MANY_REQUESTS,
                headers={"Retry-After": str(remaining_time)},
                body={
                    "error": "Demasiados intentos fallidos. IP bloqueada temporalmente",
                    "code": "IP_BLOCKED",
                    "retry_after": remaining_time
                }
            )
        
        self._cleanup_old_attempts(ip_address, current_time)
        
        response: Response = self._pass_to_next(request)
        
        if response and response.status_code == StatusCode.UNAUTHORIZED:
            self._record_failed_attempt(ip_address, current_time)
        
        return response
    
    def _is_ip_blocked(self, ip_address: str, current_time: datetime) -> bool:
        if ip_address in self.blocked_ips:
            block_until = self.blocked_ips[ip_address]
            if current_time < block_until:
                return True
            else:
                del self.blocked_ips[ip_address]
        
        return False
    
    def _get_remaining_block_time(self, ip_address: str, current_time: datetime) -> int:
        if ip_address in self.blocked_ips:
            block_until = self.blocked_ips[ip_address]
            remaining = (block_until - current_time).total_seconds()
            return max(0, int(remaining))
        return 0
    
    def _cleanup_old_attempts(self, ip_address: str, current_time: datetime):
        if ip_address not in self.failed_attempts:
            return
        
        cutoff_time = current_time - timedelta(hours=1)
        self.failed_attempts[ip_address] = [
            attempt_time for attempt_time in self.failed_attempts[ip_address]
            if attempt_time > cutoff_time
        ]
        
        if not self.failed_attempts[ip_address]:
            del self.failed_attempts[ip_address]
    
    def _record_failed_attempt(self, ip_address: str, current_time: datetime):
        if ip_address not in self.failed_attempts:
            self.failed_attempts[ip_address] = []
        
        self.failed_attempts[ip_address].append(current_time)
        
        recent_attempts = self._count_recent_attempts(ip_address, current_time)
        
        if recent_attempts >= self.max_attempts:
            block_until = current_time + timedelta(seconds=self.block_duration)
            self.blocked_ips[ip_address] = block_until
    
    def _count_recent_attempts(self, ip_address: str, current_time: datetime) -> int:
        if ip_address not in self.failed_attempts:
            return 0
        
        cutoff_time = current_time - timedelta(minutes=15)
        recent_attempts = [
            attempt_time for attempt_time in self.failed_attempts[ip_address]
            if attempt_time > cutoff_time
        ]
        
        return len(recent_attempts)
