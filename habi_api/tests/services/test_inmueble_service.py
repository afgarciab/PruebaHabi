import unittest
from unittest.mock import patch
from app.services.inmueble_service import consultar_inmuebles

class TestConsultarInmuebles(unittest.TestCase):
    """
    Pruebas unitarias para la función `consultar_inmuebles` en el módulo `inmueble_service`.
    Esta clase contiene casos de prueba para verificar la funcionalidad de la función 
    `consultar_inmuebles`, incluyendo varios escenarios de filtros.
    """

    @patch('app.services.inmueble_service.get_filtered_properties')
    def test_consultar_inmuebles_con_filtros(self, mock_get_filtered_properties):
        """
        Verifica que `consultar_inmuebles` llame a `get_filtered_properties`
        con los filtros proporcionados y devuelva el resultado esperado.
        """
        # Definimos los filtros a utilizar.
        filtros = {}
        # Simulamos la respuesta esperada de la función `get_filtered_properties`.
        mock_response = [{"id": 1, "tipo": "apartamento", "precio": 450000},
                         {"id": 2, "tipo": "apartamento", "precio": 500000}]
        # Configuramos el mock para que devuelva la respuesta simulada.
        mock_get_filtered_properties.return_value = mock_response

        # Llamamos a la función que estamos probando.
        resultado = consultar_inmuebles(filtros)

        # Verificamos que el resultado coincida con la respuesta simulada.
        self.assertEqual(resultado, mock_response)

        # Verificamos que `get_filtered_properties` haya sido llamada una vez con los filtros.
        mock_get_filtered_properties.assert_called_once_with(filtros)

    @patch('app.services.inmueble_service.get_filtered_properties')
    def test_consultar_inmuebles_sin_filtros(self, mock_get_filtered_properties):
        """
        Verifica que `consultar_inmuebles` llame a `get_filtered_properties`
        con un diccionario vacío si no se proporcionan filtros.
        """
        # Definimos un diccionario vacío como filtro.
        filtros = {}
        # Simulamos la respuesta esperada de la función `get_filtered_properties`.
        mock_response = [{"id": 3, "tipo": "casa", "precio": 1000000}]
        # Configuramos el mock para que devuelva la respuesta simulada.
        mock_get_filtered_properties.return_value = mock_response

        # Llamamos a la función que estamos probando.
        resultado = consultar_inmuebles(filtros)

        # Verificamos que el resultado coincida con la respuesta simulada.
        self.assertEqual(resultado, mock_response)

        # Verificamos que `get_filtered_properties` haya sido llamada una vez con los filtros vacíos.
        mock_get_filtered_properties.assert_called_once_with(filtros)

    @patch('app.services.inmueble_service.get_filtered_properties')
    def test_consultar_inmuebles_con_filtros_complejos(self, mock_get_filtered_properties):
        """
        Verifica que `consultar_inmuebles` pase correctamente diccionarios de filtros complejos
        a la función `get_filtered_properties`.
        """
        # Definimos filtros complejos (con sub-diccionarios y listas).
        filtros = {"ubicacion": {"ciudad": "Bogotá", "barrio": "Chapinero"},
                   "caracteristicas": ["balcon", "parqueadero"],
                   "area_minima": 70}
        # Simulamos la respuesta esperada de la función `get_filtered_properties`.
        mock_response = [{"id": 4, "ubicacion": {"ciudad": "Bogotá", "barrio": "Chapinero"}, "area": 80, "caracteristicas": ["balcon", "parqueadero"]},
                         {"id": 5, "ubicacion": {"ciudad": "Bogotá", "barrio": "Chapinero"}, "area": 75, "caracteristicas": ["balcon", "parqueadero", "ascensor"]}]
        # Configuramos el mock para que devuelva la respuesta simulada.
        mock_get_filtered_properties.return_value = mock_response

        # Llamamos a la función que estamos probando.
        resultado = consultar_inmuebles(filtros)

        # Verificamos que el resultado coincida con la respuesta simulada.
        self.assertEqual(resultado, mock_response)

        # Verificamos que `get_filtered_properties` haya sido llamada una vez con los filtros complejos.
        mock_get_filtered_properties.assert_called_once_with(filtros)

    @patch('app.services.inmueble_service.get_filtered_properties')
    def test_consultar_inmuebles_retorna_lista_vacia(self, mock_get_filtered_properties):
        """
        Verifica que `consultar_inmuebles` retorne una lista vacía si
        `get_filtered_properties` retorna una lista vacía.
        """
        # Definimos un filtro que no debería devolver resultados.
        filtros = {"tipo": "finca"}
        # Simulamos la respuesta de `get_filtered_properties` que será una lista vacía.
        mock_response = []
        mock_get_filtered_properties.return_value = mock_response

        # Llamamos a la función que estamos probando.
        resultado = consultar_inmuebles(filtros)

        # Verificamos que el resultado sea una lista vacía.
        self.assertEqual(resultado, [])

        # Verificamos que `get_filtered_properties` haya sido llamada una vez con el filtro correspondiente.
        mock_get_filtered_properties.assert_called_once_with(filtros)
