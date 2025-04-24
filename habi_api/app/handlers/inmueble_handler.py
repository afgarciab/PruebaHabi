from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
from app.services.inmueble_service import consultar_inmuebles


class InmuebleHandler(BaseHTTPRequestHandler):
    """
    InmuebleHandler es una clase encargada de procesar solicitudes HTTP GET para consultar propiedades inmobiliarias
    en base a parámetros de consulta especificados.

    Métodos:
        do_GET(self):
            Procesa solicitudes GET extrayendo parámetros de la URL, aplica filtros
            y devuelve una respuesta JSON con las propiedades que coincidan.

            Parámetros de consulta:
                - estado (str): El estado actual de la propiedad (opcional).
                - year (str): El año de construcción o publicación de la propiedad (opcional).
                - city (str): La ciudad en la que se encuentra la propiedad (opcional).

            Respuesta:
                - HTTP 200: Retorna un objeto JSON con la lista de propiedades filtradas.
                - HTTP 500: En caso de error, retorna un objeto JSON con un mensaje de error.
    """

    def do_GET(self):
        """
        Maneja solicitudes HTTP GET para recuperar propiedades inmobiliarias según los parámetros de consulta.
        Este método parsea la URL para extraer parámetros como 'estado', 'year' y 'city',
        y los utiliza como filtros para consultar propiedades inmobiliarias. Los resultados se devuelven en formato JSON.

        Parámetros de consulta:
            estado (str, opcional): El estado de la propiedad.
            year (str, opcional): El año de la propiedad.
            city (str, opcional): La ciudad donde se encuentra la propiedad.

        Respuesta:
            HTTP 200: Devuelve una respuesta JSON con las propiedades inmobiliarias filtradas.
        Excepciones:
            ValueError: Si hay un problema con los parámetros de consulta o el procesamiento de los datos.
        """

        # Parsear la URL para obtener los parámetros de la consulta
        query_params = parse_qs(urlparse(self.path).query)

        # Extraer los parámetros de la consulta
        filtros = {}
        if 'estado' in query_params:
            filtros['estado'] = query_params['estado'][0]
        if 'year' in query_params:
            filtros['year'] = query_params['year'][0]
        if 'city' in query_params:
            filtros['city'] = query_params['city'][0]

        # Llamamos al servicio para obtener los inmuebles con los filtros
        try:
            inmuebles = consultar_inmuebles(filtros)

            # Respondemos con los resultados en formato JSON
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # Convertimos los inmuebles a JSON y los enviamos
            self.wfile.write(json.dumps(
                inmuebles, ensure_ascii=False).encode('utf-8'))
        except Exception as error:
            print(error)
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # Enviamos un mensaje de error en formato JSON
            self.wfile.write(json.dumps(
                {"error": "Error al consultar"}, ensure_ascii=False).encode('utf-8'))
