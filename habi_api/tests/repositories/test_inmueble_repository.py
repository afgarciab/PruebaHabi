import unittest
from unittest.mock import patch, MagicMock
from app.repositories.inmueble_repository import get_filtered_properties

class TestInmuebleRepository(unittest.TestCase):
    """
    Clase de pruebas para verificar el funcionamiento de la función `get_filtered_properties` 
    en el repositorio de inmuebles. Se utiliza `unittest` para realizar las pruebas unitarias.
    """

    @patch('app.repositories.inmueble_repository.get_connection')
    def test_get_properties_with_city_and_estado_filter(self, mock_get_connection):
        """
        Prueba para verificar que la función `get_filtered_properties` retorna correctamente
        los inmuebles cuando se aplican los filtros de ciudad y estado.
        """
        # Simulamos una conexión a la base de datos y un cursor.
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Simulamos los resultados de la consulta a la base de datos.
        mock_cursor.fetchall.return_value = [
            {
                "address": "Calle Falsa 123",
                "city": "Bogotá",
                "price": 450000000,
                "description": "Bonito apartamento",
                "estado": "vendido"
            }
        ]

        # Filtros a aplicar en la consulta.
        filtros = {
            "city": "Bogotá",
            "estado": "vendido"
        }

        # Llamamos a la función con los filtros.
        result = get_filtered_properties(filtros)

        # Verificamos que el resultado sea el esperado.
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["city"], "Bogotá")
        self.assertEqual(result[0]["estado"], "vendido")

    @patch('app.repositories.inmueble_repository.get_connection')
    def test_get_properties_with_only_year_filter(self, mock_get_connection):
        """
        Prueba para verificar que la función `get_filtered_properties` retorna correctamente
        los inmuebles cuando se aplica solo el filtro de año.
        """
        # Simulamos una conexión a la base de datos y un cursor.
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Simulamos los resultados de la consulta a la base de datos.
        mock_cursor.fetchall.return_value = [
            {
                "address": "Avenida Siempre Viva",
                "city": "Medellín",
                "price": 550000000,
                "description": "Hermosa casa",
                "estado": "en_venta"
            }
        ]

        # Filtro a aplicar en la consulta (solo año).
        filtros = {
            "year": 2020
        }

        # Llamamos a la función con el filtro de año.
        result = get_filtered_properties(filtros)

        # Verificamos que el resultado sea el esperado.
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["estado"], "en_venta")

    @patch('app.repositories.inmueble_repository.get_connection')
    def test_get_properties_with_no_filters(self, mock_get_connection):
        """
        Prueba para verificar que la función `get_filtered_properties` retorna todos los inmuebles
        cuando no se aplican filtros.
        """
        # Simulamos una conexión a la base de datos y un cursor.
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Simulamos los resultados de la consulta a la base de datos (sin filtros).
        mock_cursor.fetchall.return_value = [
            {
                "address": "Carrera 45",
                "city": "Cali",
                "price": 300000000,
                "description": "Casa amplia",
                "estado": "pre_venta"
            },
            {
                "address": "Calle 10",
                "city": "Bogotá",
                "price": 700000000,
                "description": "Apartamento central",
                "estado": "vendido"
            }
        ]

        # No se aplican filtros.
        filtros = {}

        # Llamamos a la función sin filtros.
        result = get_filtered_properties(filtros)

        # Verificamos que se devuelvan las dos propiedades.
        self.assertEqual(len(result), 2)

    @patch('app.repositories.inmueble_repository.get_connection')
    def test_get_properties_with_filters_no_results(self, mock_get_connection):
        """
        Prueba para verificar que la función `get_filtered_properties` retorna una lista vacía
        cuando no se encuentran resultados con los filtros aplicados.
        """
        # Simulamos una conexión a la base de datos y un cursor.
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Simulamos que no se encuentran resultados para los filtros dados.
        mock_cursor.fetchall.return_value = []

        # Filtros que no producen resultados.
        filtros = {
            "city": "CiudadFantasma",
            "estado": "en_venta"
        }

        # Llamamos a la función con los filtros.
        result = get_filtered_properties(filtros)

        # Verificamos que no se devuelvan resultados.
        self.assertEqual(result, [])

if __name__ == '__main__':
    # Ejecuta las pruebas.
    unittest.main()
