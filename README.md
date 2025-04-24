# 🏡 Habi API - Sistema de Gestión de Inmuebles

Este proyecto es una API modular en Python que permite consultar propiedades inmobiliarias aplicando diversos filtros como ciudad, estado o año. Utiliza una arquitectura por capas que separa la lógica de acceso a datos, lógica de negocio y pruebas, y se conecta a una base de datos MySQL.

---

## 🚀 Tecnologías Utilizadas

- **Python 3.12**
- **MySQL**
- **mysql-connector-python** (conector para Python y MySQL)
- **unittest** (framework de pruebas unitarias de Python)
- **unittest.mock** (simulación de objetos externos)
- Arquitectura basada en **repositorios** y **servicios**
- **pydoc** (Autodocumetación del codigo)

---

## 📂 Estructura del Proyecto

habi_api/
│
├── app/
│   ├── __init__.py
│   ├── models/                  # Modelos y estructuras 
│   │   └── inmueble.py
│   ├── services/                # Lógica del negocio
│   │   └── inmueble_service.py
│   ├── repositories/           # Conexión con la base de datos
│   │   └── inmueble_repository.py
│   ├── handlers/               # Request handlers (controladores)
│   │   └── inmueble_handler.py
│   └── utils/                  # Funciones auxiliares, helpers, etc.
│       └── db_connection.py
│
├── tests/                      # Pruebas unitarias
│   └── test_inmueble.py
│
├── filters_example.json        # Ejemplo de filtros enviados por el front
├── server.py                   # Donde se levanta el microservicio
└── README.md
## 🧪 Cómo Ejecutar las Pruebas

Para ejecutar las pruebas unitarias, utiliza el siguiente comando:

python -m unittest discover tests


---

## ✅ Funcionalidades

La API permite consultar inmuebles filtrados por los siguientes parámetros:

- **ciudad**: Ciudad donde se encuentra la propiedad.
- **estado**: Estado de la propiedad (por ejemplo, "pre_venta", "en_venta", "vendido").
- **año de construcción**: Año en que fue construida la propiedad.

---

## 🧭 Enfoque del Proyecto

El desarrollo se realiza bajo una filosofía modular, escalable y testeable, siguiendo estos pasos:

1. **Diseño de arquitectura por capas**: Separación clara entre acceso a datos, lógica de negocio y controladores.
   
2. **Implementación iterativa**:
   - Primero la conexión a la base de datos.
   - Luego el repositorio para consulta de datos.
   - Después los servicios con lógica de negocio.
   - Finalmente los controladores y handlers.
   
3. **Pruebas desde el inicio (Test-First)**: Uso de `unittest` y `mock` para simular conexiones y asegurar la calidad desde el comienzo.

4. **Documentación técnica clara**: Código y pruebas documentadas.

5. **Preparación para despliegue simple y controlado**:
   - Se utilizará un servidor HTTP propio o un script personalizado en `server.py`.
   - Total independencia de frameworks web.
   - Fácil integración con herramientas externas vía HTTP básico o línea de comandos.

Este enfoque garantiza un sistema mantenible, de bajo consumo de recursos y que funciona con dependencias mínimas.

---

## 🏗️ Cómo Ejecutar la API

1. **Instalar dependencias**:
   Asegúrate de tener `mysql-connector-python` instalado. Puedes instalarlo usando `pip`:
   
pip install mysql-connector-python


2. **Configurar la base de datos**:
La API está conectada a una base de datos MySQL. Asegúrate de tener una base de datos configurada con la estructura adecuada.

3. **Ejecutar el servidor**:
Para levantar el servidor HTTP, ejecuta el siguiente comando en la raíz del proyecto:

python server.py


---

## ⚙️ Servicio de "Me gusta"

Para añadir la funcionalidad de "Me gusta" en las propiedades, se modificó el esquema de la base de datos agregando dos nuevas tablas:

1. **Tabla `like`**: Representa que un usuario ha marcado una propiedad como "me gusta".
2. **Tabla `user`**: Representa a los usuarios en la base de datos.

A través de la tabla `like`, se establece una relación entre los usuarios y las propiedades que les gustan. Además, se implementó una restricción para evitar que un usuario le dé "me gusta" a una propiedad más de una vez, mediante la especificación `"UNIQUE KEY 'like_user_property_unique' ('user_id', 'property_id')"`.

---

## 🔧 Mejora del Esquema

Para mejorar el esquema de la base de datos y optimizar el tiempo de respuesta de las consultas, se añadieron dos nuevas columnas a la tabla `property`:

1. **current_status**: El estado actual de la propiedad.
2. **last_update**: La fecha en la que se actualizó el estado de la propiedad.

Antes de esta mejora, era necesario realizar una consulta adicional a la tabla `status_history` para obtener el estado actual de la propiedad, lo cual aumentaba el tiempo de respuesta. Ahora, con la adición de estas dos columnas, el estado de la propiedad se encuentra directamente en la tabla `property`, lo que reduce significativamente el tiempo de consulta y mejora la eficiencia.

La columna `last_update` garantiza la integridad de la información al proporcionar una fecha clara de cuándo fue actualizado el estado de la propiedad.

---

## auto documentación
El proyecto incluye documentación automática generada a partir de los docstrings de cada módulo, clase y función.
Para visualizarla, simplemente ejecuta el siguiente comando desde la raíz del proyecto:

python -m pydoc -b

Este comando abrirá una interfaz web local, generalmente accesible desde http://localhost:7464, donde podrás explorar fácilmente toda la documentación del código.

Este `README.md` cubre todo lo necesario para entender el funcionamiento del proyecto, su estructura, cómo ejecutarlo y cómo implementar las funcionalidades clave, además de la documentación de las clases y métodos principales.





