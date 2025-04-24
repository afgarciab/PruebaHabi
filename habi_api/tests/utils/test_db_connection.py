from unittest.mock import patch
import mysql.connector
from app.utils.db_connection import get_connection
import unittest

class TestGetConnection(unittest.TestCase):
    """
    Pruebas unitarias para la función `get_connection` en el módulo `app.utils.db_connection`.
    Esta clase contiene casos de prueba para verificar la funcionalidad de la función `get_connection`,
    incluyendo intentos de conexión exitosos y fallidos.
    """

    @patch('mysql.connector.connect')
    def test_get_connection_success(self, mock_connect):
        """
        Verifica que `get_connection` establezca correctamente una conexión
        y devuelva un objeto MySQLConnection.
        """
        # Simulamos que la conexión fue exitosa
        mock_connection = mock_connect.return_value
        # Llamamos a la función que estamos probando.
        connection = get_connection()
        # Verificamos que la conexión devuelta sea la simulada.
        self.assertEqual(connection, mock_connection)
        # Verificamos que los parámetros de conexión sean los correctos.
        mock_connect.assert_called_once_with(
            host="18.221.137.98",
            port=3309,
            user="pruebas",
            password="VGbt3Day5R",
            database="habi_db"
        )
        # Cerramos la conexión (limpieza del mock)
        connection.close()

    @patch('mysql.connector.connect', side_effect=mysql.connector.Error("Connection failed"))
    def test_get_connection_failure(self, mock_connect):
        """
        Verifica que `get_connection` lance un `mysql.connector.Error` si
        el intento de conexión falla.
        """
        # Verificamos que se lance el error esperado cuando se intenta conectar.
        with self.assertRaises(mysql.connector.Error) as context:
            get_connection()
        # Verificamos que el mensaje del error sea el esperado.
        self.assertEqual(str(context.exception), "Connection failed")
        # Verificamos que los parámetros de conexión sean los correctos.
        mock_connect.assert_called_once_with(
            host="18.221.137.98",
            port=3309,
            user="pruebas",
            password="VGbt3Day5R",
            database="habi_db"
        )
