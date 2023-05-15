from fastapi import FastAPI
from typing import List, Dict
from fastapi.exceptions import HTTPException
from fastavro import writer, parse_schema
import pandas as pd
import pyodbc
import json

app = FastAPI()


@app.get("/create/{table_name}")
async def create_table(table_name: str):
    
    departments_data = pd.read_csv('./Input_data/departments.csv',header=None, names=['id', 'department'])
    hired_employees_data = pd.read_csv('./Input_data/hired_employees.csv',header=None, names=['id', 'name', 'datetime', 'department_id', 'job_id'])
    # Convertir la columna a tipo entero
    hired_employees_data['department_id'] = hired_employees_data['department_id'].astype(int)
    hired_employees_data['job_id'] = hired_employees_data['job_id'].astype(int)

    jobs_data= pd.read_csv('./Input_data/jobs.csv',header=None, names=['id','job'])
    
    if table_name=='departments1':
            # Establecer la conexión
        server = 'LAPTOP-DF01N7UN'
        database = 'departments_globant'

        conn_str = (
            r'DRIVER={SQL Server};'
            rf'SERVER={server};'
            rf'DATABASE={database};'
            'Trusted_Connection=yes;'
        )
        conn = pyodbc.connect(conn_str)

        # Crear un cursor
        cursor = conn.cursor()

        # Crear una tabla nueva
        cursor.execute('''
            CREATE TABLE departments1 (
                id INT,
                department VARCHAR(50),
            );
        ''')

        # Insertar datos en la tabla

        for index, row in departments_data.iterrows():
            cursor.execute(f"INSERT INTO departments1 (id, department) values (?,?)", row['id'], row['department'])

        # Guardar cambios y cerrar la conexión
        conn.commit()
        conn.close()
        
        return {f'message: Los datos de la tabla local {table_name} han sido guardados en el servidor SQL exitosamente'}
    
    elif table_name=='employees1':
                # Establecer la conexión
        server = 'LAPTOP-DF01N7UN'
        database = 'departments_globant'

        conn_str = (
            r'DRIVER={SQL Server};'
            rf'SERVER={server};'
            rf'DATABASE={database};'
            'Trusted_Connection=yes;'
        )
        conn = pyodbc.connect(conn_str)

        # Crear un cursor
        cursor = conn.cursor()

        # Crear una tabla nueva
        cursor.execute('''
            CREATE TABLE employees1 (
                id INT,
                name VARCHAR(255),
                datetime VARCHAR(255),
                department_id INT,
                job_id INT
            );
        ''')

        # Insertar datos en la tabla

        for index, row in hired_employees_data.iterrows():
            cursor.execute(f"INSERT INTO employees1 (id,name,datetime,department_id,job_id) values (?,?,?,?,?)", row['id'], row['name'],row['datetime'], row['department_id'],row['job_id'])

        # Guardar cambios y cerrar la conexión
        conn.commit()
        conn.close()
        
        return {f'message: Los datos de la tabla local {table_name} han sido guardados en el servidor SQL exitosamente'}
        
    elif table_name=='jobs1':
        
        # Establecer la conexión
        server = 'LAPTOP-DF01N7UN'
        database = 'departments_globant'

        conn_str = (
            r'DRIVER={SQL Server};'
            rf'SERVER={server};'
            rf'DATABASE={database};'
            'Trusted_Connection=yes;'
        )
        conn = pyodbc.connect(conn_str)

        # Crear un cursor
        cursor = conn.cursor()

        # Crear una tabla nueva
        cursor.execute('''
            CREATE TABLE jobs1 (
                id INT,
                job VARCHAR(255),
            );
        ''')

        # Insertar datos en la tabla

        for index, row in jobs_data.iterrows():
            cursor.execute(f"INSERT INTO jobs1 (id, job) values (?,?)", row['id'], row['job'])

        # Guardar cambios y cerrar la conexión
        conn.commit()
        conn.close()
        
        return {f'message: Los datos de la tabla local {table_name} han sido guardados en el servidor SQL exitosamente'}
    
    else:
        return {f'message: {table_name} No existe localmente'}
        


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

    
    if table_name== 'descriptions1':
        # Definir el esquema
        schema = {
            'doc': 'Descripciones',
            'name': 'Descripcion',
            'namespace': 'test',
            'type': 'record',
            'fields': [
                {'name': 'id', 'type': 'int'},
                {'name': 'department_id', 'type': 'string'},
            ],
        }
        parsed_schema = parse_schema(schema)
 
        # Guardar los registros en un archivo avro
        with open('./Backup/departments.avro', 'wb') as out:
            writer(out, parsed_schema, rows)
        
        return {f'message": "Backup exitoso de la tabla {table_name}'}
        
    elif table_name=='employees1':
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

    elif table_name=='jobs1':
        # Definir el esquema
        schema = {
            'doc': 'Trabajos',
            'name': 'Trabajo',
            'namespace': 'test',
            'type': 'record',
            'fields': [
                {'name': 'id', 'type': 'int'},
                {'name': 'job', 'type': 'int'},
            ],
        }
        parsed_schema = parse_schema(schema)
 
        # Guardar los registros en un archivo avro
        with open('./Backup/jobs.avro', 'wb') as out:
            writer(out, parsed_schema, rows)
            
        return {f'message": "Backup exitoso de la tabla {table_name}'}
    
    else: 
        return {f'message": "Ha ingresado el nombre de una tabla que no se ha creado aun'}

@app.get("/read_avro/{table_name}")
async def read_avro(table_name: str):
    
    import fastavro
    
    if table_name=='descriptions1':
        result=[]
        with open('./Backup/descriptions.avro', 'rb') as fp:
            reader = fastavro.reader(fp)
            print()
            schema = reader.schema
            for record in reader:
                result.append(record)
        
        print(result)
        
        result=json.JSONEncoder().encode(result)
        
        return {result}
    

    elif table_name=='employees1':
        result=[]

        with open('./Backup/employees.avro', 'rb') as fp:
            reader = fastavro.reader(fp)
            print()
            schema = reader.schema
            for record in reader:
                result.append(record)
        
        print(result)
        
        result=json.JSONEncoder().encode(result)
        
        return {result}

    elif table_name=='jobs1':
        result=[]

        with open('./Backup/jobs.avro', 'rb') as fp:
            reader = fastavro.reader(fp)
            print()
            schema = reader.schema
            for record in reader:
                result.append(record)
        
        print(result)
        
        result=json.JSONEncoder().encode(result)
        
        return {result}




    