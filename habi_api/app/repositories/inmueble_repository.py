from app.utils.db_connection import get_connection

# Repository: obtener inmuebles de la BD
# 2.  conectamos con MySQL y ejecutamos el SQL.
# app/repositories/inmueble_repository.py

def get_filtered_properties(filtros):
    """
    Obtiene una lista de propiedades de la base de datos, aplicando filtros opcionales.
    
    Parámetros:
    filtros (dict): Diccionario con los filtros que se desean aplicar en la consulta. 
                    Puede contener las claves 'year', 'city', y 'estado'.

    Retorna:
    list: Una lista de diccionarios con los detalles de los inmuebles que cumplen con los filtros. 
          Cada diccionario representa una propiedad con las claves: 'address', 'city', 'price', 'description', 'estado'.
    
    La función realiza una consulta SQL a la base de datos y obtiene las propiedades que coinciden con los filtros proporcionados. 
    Los filtros son aplicados sobre el año de la propiedad, la ciudad y el estado del inmueble.
    """
    
    # Establece la conexión a la base de datos utilizando la función get_connection.
    conn = get_connection()
    
    # Crea un cursor para ejecutar las consultas SQL y obtener los resultados como diccionarios.
    cursor = conn.cursor(dictionary=True)
    
    # Consulta SQL base que obtiene las propiedades y su estado desde la base de datos.
    sql = """
    SELECT p.address, p.city, p.price, p.description,  s.name AS estado
        FROM property p
        JOIN (
            SELECT property_id, status_id
            FROM status_history
            WHERE (property_id, update_date) IN (
                SELECT property_id, MAX(update_date)
                FROM status_history
                GROUP BY property_id
            )
        ) sh ON p.id = sh.property_id
        JOIN status s ON sh.status_id = s.id
        WHERE s.name IN ('pre_venta', 'en_venta', 'vendido')
    """

    # Lista de parámetros que se utilizarán en la consulta SQL (filtros opcionales).
    params = []

    # Filtro por año, si se proporciona en los filtros.
    if filtros.get('year'):
        sql += " AND p.year = %s"
        params.append(filtros['year'])

    # Filtro por ciudad, si se proporciona en los filtros.
    if filtros.get('city'):
        sql += " AND p.city = %s"
        params.append(filtros['city'])

    # Filtro por estado, si se proporciona en los filtros.
    if filtros.get('estado'):
        sql += " AND s.name = %s"
        params.append(filtros['estado'])

    # Ejecuta la consulta SQL con los parámetros proporcionados.
    cursor.execute(sql, params)
    
    # Obtiene todos los resultados de la consulta en una lista de diccionarios.
    properties = cursor.fetchall()

    # Cierra el cursor y la conexión con la base de datos para liberar recursos.
    cursor.close()
    conn.close()
    
    # Retorna la lista de propiedades obtenidas.
    return properties
