import unittest
from unittest.mock import patch, MagicMock
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from io import BytesIO
import json
from app.handlers.inmueble_handler import InmuebleHandler

class MockSocket:
    def __init__(self, request_data=b"GET /inmuebles HTTP/1.1\r\nHost: localhost\r\n\r\n"):
        self._buffer = BytesIO(request_data)

    def makefile(self, mode='rb', buffering=-1):
        return self._buffer

    def fileno(self):
        return -1

    def recv(self, maxlen):
        return self._buffer.read(maxlen)

    def sendall(self, data):
        pass

    def close(self):
        pass

class TestInmuebleHandler(unittest.TestCase):

    def setUp(self):
        """Se ejecuta antes de cada método de prueba para configurar el entorno."""
        self.mock_client_address = ('localhost', 8000)
        self.mock_server = MagicMock()

    def _create_handler(self, path, query=""):
        """Crea una instancia de InmuebleHandler con la ruta especificada."""
        request_line = f"GET {path}?{query} HTTP/1.1\r\nHost: localhost\r\n\r\n".encode('utf-8')
        mock_socket = MockSocket(request_line)
        handler = InmuebleHandler(mock_socket, self.mock_client_address, self.mock_server)
        handler.path = path + "?" + query if query else path
        handler.wfile = BytesIO()  # Simula el archivo de escritura
        return handler

    def _get_response_content(self, handler):
        """Obtiene el contenido de la respuesta del handler."""
        return handler.wfile.getvalue().decode('utf-8')

    def _assert_raw_response(self, handler, expected_status, expected_headers, expected_body):
        """Verifica la respuesta HTTP completa escrita en wfile."""
        response = self._get_response_content(handler).split('\r\n\r\n', 1)
        headers_part = response[0].split('\r\n')
        status_line = headers_part[0]
        received_headers = {}
        for header in headers_part[1:]:
            if ': ' in header:
                key, value = header.split(': ', 1)
                received_headers[key] = value.strip()
        body = response[1] if len(response) > 1 else ""

        self.assertIn(f"HTTP/1.0 {expected_status}", status_line)
        for key, value in expected_headers.items():
            self.assertIn(key, received_headers)
            self.assertEqual(received_headers[key], value)
        self.assertEqual(json.loads(body) if body else None, expected_body)

    def _assert_json_response(self, handler, expected_status, expected_content):
        """Verifica el código de estado y el contenido JSON de la respuesta."""
        response = self._get_response_content(handler).split('\r\n\r\n', 1)
        headers_part = response[0].split('\r\n')
        status_line = headers_part[0]
        received_headers = {}
        for header in headers_part[1:]:
            if ': ' in header:
                key, value = header.split(': ', 1)
                received_headers[key] = value.strip()
        body = response[1] if len(response) > 1 else ""

        self.assertIn(f"HTTP/1.0 {expected_status}", status_line)
        self.assertIn('Content-type', received_headers)
        self.assertEqual(received_headers['Content-type'], 'application/json')
        self.assertEqual(json.loads(body), expected_content)

    @patch('app.handlers.inmueble_handler.consultar_inmuebles')
    def test_do_GET_sin_filtros(self, mock_consultar_inmuebles):
        """Prueba la solicitud GET sin parámetros de consulta."""
        mock_consultar_inmuebles.return_value = [{"id": 1, "estado": "activo"}, {"id": 2, "estado": "inactivo"}]
        handler = self._create_handler('/inmuebles')
        handler.do_GET()
        self._assert_json_response(handler, 200, [{"id": 1, "estado": "activo"}, {"id": 2, "estado": "inactivo"}])
        self.assertEqual(mock_consultar_inmuebles.call_count, 2)

    @patch('app.handlers.inmueble_handler.consultar_inmuebles')
    def test_do_GET_con_filtro_estado(self, mock_consultar_inmuebles):
        """Prueba la solicitud GET con el parámetro de consulta 'estado'."""
        mock_consultar_inmuebles.return_value = [{"id": 3, "estado": "activo", "city": "Bogotá"}]
        handler = self._create_handler('/inmuebles', 'estado=activo')
        handler.do_GET()
        self._assert_json_response(handler, 200, [{"id": 3, "estado": "activo", "city": "Bogotá"}])
        self.assertEqual(mock_consultar_inmuebles.call_count, 2)

    @patch('app.handlers.inmueble_handler.consultar_inmuebles', side_effect=Exception("Error al consultar"))
    def test_do_GET_servicio_levanta_error(self, mock_consultar_inmuebles):
        """Prueba el caso en que el servicio consultar_inmuebles levanta una excepción."""
        handler = self._create_handler('/inmuebles')
        handler.do_GET()
        response = self._get_response_content(handler)
        self.assertIn("HTTP/1.0 500 Internal Server Error", response)
        self.assertIn("Content-type: application/json", response)
        self.assertIn(json.dumps({"error": "Error al consultar"}), response)
        self.assertEqual(mock_consultar_inmuebles.call_count, 2)