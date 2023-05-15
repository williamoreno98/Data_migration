
# Solución de migración de datos y API REST para el proyecto de Big Data
Este proyecto tiene como objetivo realizar la migración de datos históricos desde archivos CSV a un nuevo sistema de base de datos. Además, se requiere crear una API REST que permita recibir nuevos datos y cumplir con ciertos requisitos. A continuación, se detalla la solución paso a paso:

# ¿Cómo probarlo?

1. Ir al diccionario root del proyecto y escribir el siguiente comando:

uvicorn migration_api:app --reload

Output: http://127.0.0.1:8000/

#  ¿Qué debo instalar?

fastapi==0.95.1
fastavro==1.7.4
pyodbc==4.0.39
uvicorn==0.22.0
pandas==2.0.1


## Paso 1: Migración de datos históricos desde archivos CSV
1. La solución implementada se encuentra en el archivo "migration_api.py".
2. Se utiliza la biblioteca pandas de Python para leer los datos de los archivos CSV.
3. Los archivos de entrada son: "departments.csv", "hired_employees.csv" y "jobs.csv".
4. Se lee cada archivo CSV y se almacena en un DataFrame de pandas.
5. Para cada tabla (departments, hired_employees, jobs), se crea una conexión con la base de datos SQL Server.
6. Se utiliza la biblioteca pyodbc para establecer la conexión y crear un cursor.
7. Se crea una nueva tabla en la base de datos para cada tabla de los archivos CSV.
8. Se recorre cada fila del DataFrame y se inserta en la tabla correspondiente utilizando consultas SQL.
9. Finalmente, se guardan los cambios y se cierra la conexión con la base de datos.

## Paso 2: Creación de una API REST para recibir nuevos datos
1. Se utiliza la biblioteca FastAPI de Python para crear la API REST.
2. Se definen varios endpoints para cumplir con los requisitos del proyecto.

### Endpoint: /create/{table_name}
1. Este endpoint permite crear una tabla en la base de datos para la tabla especificada.
2. Los datos de las tablas iniciales (departments, hired_employees, jobs) ya han sido migrados en el Paso 1.
3. Se lee el archivo CSV correspondiente a la tabla especificada.
4. Se establece una conexión con la base de datos SQL Server.
5. Se crea una nueva tabla en la base de datos con la estructura adecuada.
6. Se recorre cada fila del archivo CSV y se inserta en la tabla de la base de datos.
7. Se guardan los cambios y se cierra la conexión.

### Endpoint: /read/{table_name}
1. Este endpoint permite leer y obtener todos los registros de una tabla especificada.
2. Se establece una conexión con la base de datos SQL Server.
3. Se ejecuta una consulta SQL para obtener todos los registros de la tabla especificada.
4. Se obtienen los resultados y se almacenan en una lista de diccionarios.
5. Se cierra la conexión y se retorna la lista de registros en formato JSON.

### Endpoint: /insert/{table_name}
1. Este endpoint permite insertar nuevos datos en una tabla especificada.
2. Se establece una conexión con la base de datos SQL Server.
3. Se verifica que los datos enviados tengan las mismas columnas que la tabla especificada.
4. Se ejecuta una consulta SQL para insertar los nuevos datos en la tabla.
5. Se guardan los cambios y se cierra la conexión.

### Endpoint: /save/{table_name}
1. Este endpoint permite realizar un respaldo (backup) de una tabla especificada en formato AVRO.
2. Se establece una conexión con la base de datos SQL Server.
3. Se ejecuta una consulta SQL para obtener todos los registros de la tabla especificada.
4. Se obtienen los resultados y se almacenan en una lista de diccionarios.
5. Se define un esquema AVRO para la tabla especificada.
6. Se guarda la lista de registros en un archivo AVRO en el sistema de archivos.

### Endpoint: /read_table/{table_name}
1. Este endpoint permite leer los datos del archivo avro
y mostrarlos en la respuesta del API para un posterior uso.

## Apreciaciones adicionales

1. Se realizo un dockerfile que corre el API en un contenedor en la nube.
2. se agregó un archivo .env para incluir seguridad al repo y guardar las variables de entorno
de la conexión de SQL server.
3. Todo se realiza en la rama "/Data_migration" y al final se hace merge con el 
otro challenge conservando todas las versiones del proceso de desarrollo realizado.