from app.repositories.inmueble_repository import get_filtered_properties

def consultar_inmuebles(filtros):
    """
    Consulta los inmuebles en la base de datos aplicando los filtros proporcionados.

    Esta función actúa como una capa intermedia entre el controlador y el repositorio. Recibe un diccionario de filtros,
    los pasa a la función `get_filtered_properties` del repositorio y devuelve los resultados obtenidos.

    Parámetros:
    filtros (dict): Un diccionario de filtros para limitar los resultados de la consulta de inmuebles.
                    Las claves posibles son:
                    - 'year': Año de la propiedad.
                    - 'city': Ciudad de la propiedad.
                    - 'estado': Estado de la propiedad (por ejemplo, 'en_venta', 'vendido').

    Retorna:
    list: Una lista de diccionarios donde cada diccionario representa una propiedad que cumple con los filtros.
          Cada diccionario contiene las siguientes claves: 'address', 'city', 'price', 'description', 'estado'.
    """
    # Llama al repositorio para obtener las propiedades filtradas
    return get_filtered_properties(filtros)
