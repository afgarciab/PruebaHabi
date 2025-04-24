import mysql.connector

def get_connection():
    """
    Establece y devuelve una conexión a la base de datos MySQL.

    Esta función utiliza la librería `mysql.connector` para conectar a una base de datos MySQL.
    Los parámetros de conexión (como el host, puerto, usuario, contraseña y base de datos) están definidos
    explícitamente dentro de la función.

    Retorna:
    connection (MySQLConnection): Una conexión activa a la base de datos MySQL que se puede usar para realizar consultas.

    Excepciones:
    mysql.connector.Error: Si hay un problema con la conexión, se lanzará una excepción.
    """
    return mysql.connector.connect(
        host="18.221.137.98",          # Dirección IP o nombre de host del servidor MySQL
        port=3309,                     # Puerto en el que el servidor MySQL está escuchando
        user="pruebas",                # Nombre de usuario para autenticarse en la base de datos
        password="VGbt3Day5R",         # Contraseña para autenticarse en la base de datos
        database="habi_db"             # Nombre de la base de datos a la que se desea conectar
    )
