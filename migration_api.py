from fastapi import FastAPI
from typing import List, Dict
from fastapi.exceptions import HTTPException
from fastavro import writer, parse_schema
import pyodbc
import json

app = FastAPI()

@app.get("/read/{table_name}")
async def read_table(table_name: str):
    # Leer tabla
    server = 'LAPTOP-DF01N7UN'
    database = 'departments_globant'

    # Cadenas de conexión con la autenticación de Windows
    conn_str = (
        r'DRIVER={SQL Server};'
        rf'SERVER={server};'
        rf'DATABASE={database};'
        'Trusted_Connection=yes;'
    )

    # Establecer la conexión
    conn = pyodbc.connect(conn_str)

    # Crear un cursor
    cursor = conn.cursor()
    print(table_name)
    print(f'SELECT * FROM {table_name}')

    # Ejecutar una consulta
    cursor.execute(f'SELECT * FROM {table_name}')

    # Obtener los resultados
    rows = []
    for row in cursor:
        rows.append(row)

    # Cerrar la conexión
    conn.close()
    
    print(rows)
    
    columns = [column[0] for column in cursor.description]
    rows = [dict(zip(columns, row)) for row in rows]
    
    rows= json.JSONEncoder().encode(rows)

    return {rows}


@app.post("/insert/{table_name}")
async def insert_data(table_name: str, data: List[Dict]):
    # Leer tabla
    server = 'LAPTOP-DF01N7UN'
    database = 'departments_globant'

    # Cadenas de conexión con la autenticación de Windows
    conn_str = (
        r'DRIVER={SQL Server};'
        rf'SERVER={server};'
        rf'DATABASE={database};'
        'Trusted_Connection=yes;'
    )

    # Establecer la conexión
    conn = pyodbc.connect(conn_str)

    # Crear un cursor
    cursor = conn.cursor()

    # Ejecutar una consulta para obtener las columnas de la tabla
    cursor.execute(f"SELECT TOP 0 * FROM {table_name}")
    columns = [column[0] for column in cursor.description]

    # Verificar que los datos tengan las mismas columnas que la tabla
    for row in data:
        if set(row.keys()) != set(columns):
            raise HTTPException(status_code=400, detail="Las columnas de los datos no coinciden con las de la tabla")

    # Ejecutar la inserción
    try:
        cursor.fast_executemany = True
        cursor.executemany(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join('?'*len(columns))})", 
                           [tuple(row.values()) for row in data])
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    # Cerrar la conexión
    conn.close()

    return {"message": "Los datos han sido insertados correctamente."}


@app.get("/save/{table_name}")
async def save_table(table_name: str):
    # Leer tabla
    server = 'LAPTOP-DF01N7UN'
    database = 'departments_globant'

    # Cadenas de conexión con la autenticación de Windows
    conn_str = (
        r'DRIVER={SQL Server};'
        rf'SERVER={server};'
        rf'DATABASE={database};'
        'Trusted_Connection=yes;'
    )

    # Establecer la conexión
    conn = pyodbc.connect(conn_str)

    # Crear un cursor
    cursor = conn.cursor()
    print(table_name)
    print(f'SELECT * FROM {table_name}')

    # Ejecutar una consulta
    cursor.execute(f'SELECT * FROM {table_name}')

    # Obtener los resultados
    rows = []
    for row in cursor:
        rows.append(row)

    # Cerrar la conexión
    conn.close()
    
    columns = [column[0] for column in cursor.description]
    rows = [dict(zip(columns, row)) for row in rows]
    
    from fastavro import writer, parse_schema

    # Definir el esquema
    schema = {
        'doc': 'Empleados',
        'name': 'Empleado',
        'namespace': 'test',
        'type': 'record',
        'fields': [
            {'name': 'id', 'type': 'int'},
            {'name': 'name', 'type': 'string'},
            {'name': 'datetime', 'type': 'string'},
            {'name': 'department_id', 'type': 'int'},
            {'name': 'job_id', 'type': 'int'},
        ],
    }
    parsed_schema = parse_schema(schema)


    # Guardar los registros en un archivo avro
    with open('./Backup/employees.avro', 'wb') as out:
        writer(out, parsed_schema, rows)

    
    return {f'message": "Backup exitoso de la tabla {table_name}'}


@app.get("/save/{table_name}")
async def save_table(table_name: str):
    # Leer tabla
    server = 'LAPTOP-DF01N7UN'
    database = 'departments_globant'

    # Cadenas de conexión con la autenticación de Windows
    conn_str = (
        r'DRIVER={SQL Server};'
        rf'SERVER={server};'
        rf'DATABASE={database};'
        'Trusted_Connection=yes;'
    )

    # Establecer la conexión
    conn = pyodbc.connect(conn_str)

    # Crear un cursor
    cursor = conn.cursor()
    print(table_name)
    print(f'SELECT * FROM {table_name}')

    # Ejecutar una consulta
    cursor.execute(f'SELECT * FROM {table_name}')

    # Obtener los resultados
    rows = []
    for row in cursor:
        rows.append(row)

    # Cerrar la conexión
    conn.close()
    
    columns = [column[0] for column in cursor.description]
    rows = [dict(zip(columns, row)) for row in rows]
    

    # Definir el esquema
    schema = {
        'doc': 'Empleados',
        'name': 'Empleado',
        'namespace': 'test',
        'type': 'record',
        'fields': [
            {'name': 'id', 'type': 'int'},
            {'name': 'name', 'type': 'string'},
            {'name': 'datetime', 'type': 'string'},
            {'name': 'department_id', 'type': 'int'},
            {'name': 'job_id', 'type': 'int'},
        ],
    }
    parsed_schema = parse_schema(schema)


    # Guardar los registros en un archivo avro
    with open('./Backup/employees.avro', 'wb') as out:
        writer(out, parsed_schema, rows)

    
    return {f'message": "Backup exitoso de la tabla {table_name}'}



@app.get("/read_avro")
async def read_avro():
    result=[]
    import fastavro
    with open('./Backup/employees.avro', 'rb') as fp:
        reader = fastavro.reader(fp)
        print()
        schema = reader.schema
        for record in reader:
            result.append(record)
    
    print(result)
    
    result=json.JSONEncoder().encode(result)
    
    return {result}




    