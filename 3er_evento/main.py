from src.models.server import Server
from src.handlers.authentication_handler import AuthenticationHandler
from src.handlers.authorization_handler import AuthorizationHandler
from src.handlers.data_validation_handler import DataValidationHandler
from src.handlers.brute_force_protection_handler import BruteForceProtectionHandler
from src.handlers.cache_handler import CacheHandler
from src.utils.extract_basic import ExtractBasic
from src.models.request import Request
from src.models.response import Response
from src.enum.status_code import StatusCode
from datetime import datetime


if __name__ == "__main__":
    server = Server()
    server.add_middleware(BruteForceProtectionHandler(max_attempts=3, block_duration=120))      
    server.add_middleware(AuthenticationHandler(ExtractBasic()))
    server.add_middleware(AuthorizationHandler())
    server.add_middleware(DataValidationHandler())
    server.add_middleware(CacheHandler())