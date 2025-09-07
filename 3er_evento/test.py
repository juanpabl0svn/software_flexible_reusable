import pytest
from datetime import datetime
from src.models.server import Server
from src.models.request import Request
from src.models.response import Response
from src.models.user import User
from src.handlers.authentication_handler import AuthenticationHandler
from src.handlers.authorization_handler import AuthorizationHandler
from src.handlers.data_validation_handler import DataValidationHandler
from src.handlers.brute_force_protection_handler import BruteForceProtectionHandler
from src.handlers.cache_handler import CacheHandler
from src.utils.extract_basic import ExtractBasic
from src.enum.status_code import StatusCode


class Test:
    @pytest.fixture
    def server(self):
        server = Server()
        
        server.add_middleware(BruteForceProtectionHandler(max_attempts=3))
        server.add_middleware(DataValidationHandler())
        server.add_middleware(AuthenticationHandler(extraction_method=ExtractBasic()))
        server.add_middleware(CacheHandler())
        server.add_middleware(AuthorizationHandler())
        
        return server

    @pytest.fixture
    def valid_user_request(self):
        return Request(
            method="POST",
            path="/orders",
            headers={"Authorization": "Basic user1:password123"},
            body={"items": ["Pizza", "Soda"], "total": 25.99},
            ip_address="192.168.1.100",
            timestamp=datetime.now(),
            user_credentials={"username": "user1", "password": "password123"}
        )

    @pytest.fixture
    def valid_admin_request(self):
        return Request(
            method="DELETE",
            path="/orders/1",
            headers={"Authorization": "Basic admin:admin123"},
            body={},
            ip_address="192.168.1.1",
            timestamp=datetime.now(),
            user_credentials={"username": "admin", "password": "admin123"}
        )

    def test_caso_uso_1_autenticacion_exitosa_usuario_normal(self, server, valid_user_request):

        response = server.process_request(valid_user_request)
        
        assert response.status_code == StatusCode.CREATED
        assert "order" in response.body
        assert response.body["order"]["user_id"] == "user1"

    def test_caso_uso_2_acceso_total_administrador(self, server, valid_admin_request):

        response = server.process_request(valid_admin_request)
        
        assert response.status_code == StatusCode.OK

    def test_caso_uso_3_verificaciones_secuenciales_fallo_autenticacion(self, server):

        invalid_auth_request = Request(
            method="POST",
            path="/orders",
            headers={},
            body={"items": ["Pizza"], "total": 15.99},
            ip_address="192.168.1.200",
            timestamp=datetime.now(),
            user_credentials={"username": "user1", "password": "wrong_password"}
        )
        
        response = server.process_request(invalid_auth_request)
        
        assert response.status_code == StatusCode.UNAUTHORIZED
        assert "credenciales" in response.body["error"].lower() or "authentication" in response.body["error"].lower()

    def test_caso_uso_4_sin_credenciales(self, server):

        no_credentials_request = Request(
            method="POST",
            path="/orders",
            headers={},
            body={"items": ["Pizza"], "total": 15.99},
            ip_address="192.168.1.300",
            timestamp=datetime.now()
        )
        
        response = server.process_request(no_credentials_request)
        
        assert response.status_code == StatusCode.UNAUTHORIZED

    def test_caso_uso_5_validacion_datos_maliciosos(self, server):

        malicious_request = Request(
            method="POST",
            path="/orders",
            headers={},
            body={
                "items": ["<script>alert('xss')</script>"],
                "description": "DROP TABLE orders; --",
                "total": 100
            },
            ip_address="192.168.1.400",
            timestamp=datetime.now(),
            user_credentials={"username": "user1", "password": "password123"}
        )
        
        response = server.process_request(malicious_request)
        
        assert response.status_code == StatusCode.BAD_REQUEST
        assert "invalid" in response.body["error"].lower() or "datos" in response.body["error"].lower()

    def test_caso_uso_6_proteccion_fuerza_bruta_bloqueo_ip(self, server):

        ip_address = "192.168.1.500"
        
        for i in range(4): 
            failed_request = Request(
                method="POST",
                path="/orders",
                headers={},
                body={"items": ["Test"], "total": 10.0},
                ip_address=ip_address,
                timestamp=datetime.now(),
                user_credentials={"username": "user1", "password": "wrong_password"}
            )
            
            response = server.process_request(failed_request)
            
            if i < 3:
                assert response.status_code == StatusCode.UNAUTHORIZED
            else:
                assert response.status_code == StatusCode.TOO_MANY_REQUESTS
                assert "bloqueada" in response.body["error"].lower() or "blocked" in response.body["error"].lower()

    def test_caso_uso_7_cache_respuestas_repetidas(self, server):

        get_request = Request(
            method="GET",
            path="/orders",
            headers={},
            body={},
            ip_address="192.168.1.600",
            timestamp=datetime.now(),
            user_credentials={"username": "user1", "password": "password123"}
        )
        
        response1 = server.process_request(get_request)
        assert response1.status_code == StatusCode.OK
        assert not response1.is_from_cache
        
        response2 = server.process_request(get_request)
        assert response2.status_code == StatusCode.OK
        assert response2.is_from_cache 

    def test_caso_uso_8_usuario_sin_permisos_admin(self, server):
        user_admin_attempt = Request(
            method="DELETE",
            path="/orders/test-id",
            headers={},
            body={},
            ip_address="192.168.1.700",
            timestamp=datetime.now(),
            user_credentials={"username": "user1", "password": "password123"}
        )
        
        response = server.process_request(user_admin_attempt)
        
        assert response.status_code == StatusCode.FORBIDDEN

    def test_caso_uso_9_extension_nuevas_verificaciones(self, server):
        class NewVerificationHandler:
            def __init__(self):
                self.next_handler = None
                
            def set_next(self, handler):
                self.next_handler = handler
                
            def handle(self, request):
                if "test_extension" not in request.body:
                    return Response(
                        status_code=StatusCode.BAD_REQUEST,
                        headers={},
                        body={"error": "New Verification fails"}
                    )
                return self.next_handler.handle(request) if self.next_handler else None
        
        new_middleware = NewVerificationHandler()
        server.add_middleware(new_middleware)
        
        test_request = Request(
            method="POST",
            path="/orders",
            headers={},
            body={"test_extension": True, "items": ["Test"], "total": 10.0},
            ip_address="192.168.1.800",
            timestamp=datetime.now(),
            user_credentials={"username": "user1", "password": "password123"}
        )
        
        response = server.process_request(test_request)
        
        assert response.status_code == StatusCode.CREATED

        test_request_fail = Request(
            method="POST",
            path="/orders",
            headers={},
            body={"items": ["Test"], "total": 10.0},
            ip_address="192.168.1.800",
            timestamp=datetime.now(),
            user_credentials={"username": "user1", "password": "password123"}
        )

        response_fail = server.process_request(test_request_fail)

        assert response_fail.status_code == StatusCode.BAD_REQUEST
        assert "New Verification fails" in response_fail.body["error"]

    def test_caso_uso_10_reutilizacion_verificaciones(self, server):
        server2 = Server()
        server2.add_middleware(AuthenticationHandler(extraction_method=ExtractBasic()))
        server2.add_middleware(DataValidationHandler())
        
        test_request = Request(
            method="POST",
            path="/orders",
            headers={},
            body={"items": ["Test"], "total": 10.0},
            ip_address="192.168.1.900",
            timestamp=datetime.now(),
            user_credentials={"username": "user1", "password": "password123"}
        )
        
        response = server2.process_request(test_request)
        
        assert response is not None
        assert hasattr(test_request, 'authenticated_user')


class TestMiddlewareIndividual:

    def test_authentication_handler_usuario_valido(self):
        handler = AuthenticationHandler(extraction_method=ExtractBasic())
        
        request = Request(
            method="POST",
            path="/orders",
            headers={},
            body={},
            ip_address="192.168.1.1",
            timestamp=datetime.now(),
            user_credentials={"username": "user1", "password": "password123"}
        )
        
        response = handler.handle(request)
        
        assert response is None
        assert hasattr(request, 'authenticated_user')
        assert request.authenticated_user.username == "user1"

    def test_authentication_handler_credenciales_invalidas(self):
        handler = AuthenticationHandler(extraction_method=ExtractBasic())
        
        request = Request(
            method="POST",
            path="/orders",
            headers={},
            body={},
            ip_address="192.168.1.1",
            timestamp=datetime.now(),
            user_credentials={"username": "user1", "password": "wrong"}
        )
        
        response = handler.handle(request)
        
        assert response is not None
        assert response.status_code == StatusCode.UNAUTHORIZED

    def test_authorization_handler_admin_acceso(self):
        handler = AuthorizationHandler()
        
        request = Request(
            method="DELETE",
            path="/admin/users",
            headers={},
            body={},
            ip_address="192.168.1.1",
            timestamp=datetime.now()
        )
        
        admin_user = User(username="admin", password="admin123", is_admin=True)
        request.set_authenticated_user(admin_user)
        
        response = handler.handle(request)
        
        assert response is None 

    def test_authorization_handler_user_sin_permisos(self):
        handler = AuthorizationHandler()
        
        request = Request(
            method="DELETE",
            path="/admin/users",
            headers={},
            body={},
            ip_address="192.168.1.1",
            timestamp=datetime.now()
        )
        
        normal_user = User(username="user1", password="password123", is_admin=False)
        request.set_authenticated_user(normal_user)
        
        response = handler.handle(request)
        
        assert response is not None
        assert response.status_code == StatusCode.FORBIDDEN

    def test_data_validation_handler_datos_limpios(self):
        handler = DataValidationHandler()
        
        request = Request(
            method="POST",
            path="/orders",
            headers={"Content-Type": "application/json"},
            body={"items": ["Pizza", "Soda"], "total": 25.99},
            ip_address="192.168.1.1",
            timestamp=datetime.now()
        )
        
        response = handler.handle(request)
        
        assert response is None

    def test_data_validation_handler_datos_maliciosos(self):
        handler = DataValidationHandler()
        
        request = Request(
            method="POST",
            path="/orders",
            headers={},
            body={"description": "<script>alert('xss')</script>"},
            ip_address="192.168.1.1",
            timestamp=datetime.now()
        )
        
        response = handler.handle(request)
        
        assert response is not None
        assert response.status_code == StatusCode.BAD_REQUEST


class TestScenarios:

    @pytest.fixture
    def configured_server(self):
        """Servidor completamente configurado"""
        server = Server()
        server.add_middleware(BruteForceProtectionHandler())
        server.add_middleware(DataValidationHandler())
        server.add_middleware(CacheHandler())
        server.add_middleware(AuthenticationHandler(extraction_method=ExtractBasic()))
        server.add_middleware(AuthorizationHandler())
        return server

    def test_escenario_flujo_completo_exitoso(self, configured_server):

        request = Request(
            method="POST",
            path="/orders",
            headers={"Content-Type": "application/json"},
            body={"items": ["Pizza Margherita", "Coca Cola"], "total": 25.99},
            ip_address="192.168.1.100",
            timestamp=datetime.now(),
            user_credentials={"username": "user1", "password": "password123"}
        )
        
        response = configured_server.process_request(request)
        
        assert response.status_code == StatusCode.CREATED
        assert "order" in response.body
        assert response.body["order"]["user_id"] == "user1"
        assert response.body["order"]["items"] == ["Pizza Margherita", "Coca Cola"]
        assert response.body["order"]["total"] == 25.99

    def test_escenario_administrador_completo(self, configured_server):
        create_request = Request(
            method="POST",
            path="/orders",
            headers={"Content-Type": "application/json"},
            body={"items": ["Laptop", "Mouse"], "total": 999.99},
            ip_address="192.168.1.1",
            timestamp=datetime.now(),
            user_credentials={"username": "admin", "password": "admin123"}
        )
        
        create_response = configured_server.process_request(create_request)
        assert create_response.status_code == StatusCode.CREATED
        
        get_request = Request(
            method="GET",
            path="/orders",
            headers={},
            body={},
            ip_address="192.168.1.1",
            timestamp=datetime.now(),
            user_credentials={"username": "admin", "password": "admin123"}
        )
        
        get_response = configured_server.process_request(get_request)
        assert get_response.status_code == StatusCode.OK
        assert "orders" in get_response.body

    def test_escenario_cadena_verificaciones_secuencial(self, configured_server):
        request = Request(
            method="GET",
            path="/orders",
            headers={"User-Agent": "TestClient/1.0"},
            body={},
            ip_address="192.168.1.200",
            timestamp=datetime.now(),
            user_credentials={"username": "user1", "password": "password123"}
        )
        
        response = configured_server.process_request(request)
        
        assert response.status_code == StatusCode.OK
        
        assert hasattr(request, 'authenticated_user')
        assert request.authenticated_user.username == "user1"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
