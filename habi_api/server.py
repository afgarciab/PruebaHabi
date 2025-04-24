# server.py
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from app.handlers.inmueble_handler import InmuebleHandler

# Levantar el servidor


class MyHandler(BaseHTTPRequestHandler):

    # Función para levantar el servidor
    def run():
        server_address = ('', 8000)  # Establecemos el puerto donde escuchará
        # Usamos la clase InmuebleHandler para manejar las solicitudes
        httpd = HTTPServer(server_address, InmuebleHandler)

        print("Servidor corriendo en http://localhost:8000")
        httpd.serve_forever()  # Levanta el servidor

    if __name__ == "__main__":
        run()
