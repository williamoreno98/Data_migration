import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# cargar datos
departments_data = pd.read_csv('./Input_data/departments.csv', header=None, names=['id', 'department'])
hired_employees_data = pd.read_csv('./Input_data/hired_employees.csv', header=None, names=['id', 'name', 'datetime', 'department_id', 'job_id'])
jobs_data = pd.read_csv('./Input_data/jobs.csv', header=None, names=['id', 'job'])

# convertir la columna datetime a datetime
hired_employees_data['datetime'] = pd.to_datetime(hired_employees_data['datetime'])

# agregar una columna de trimestre para el 2021
hired_employees_data['quarter'] = hired_employees_data[hired_employees_data['datetime'].dt.year == 2021]['datetime'].dt.quarter

# combinar las tablas de empleados contratados y departamentos por la columna 'department_id'
hired_employees_department = pd.merge(hired_employees_data, departments_data, left_on='department_id', right_on='id')

# combinar la tabla combinada anterior y la tabla de trabajos por la columna 'job_id'
hired_employees_department_job = pd.merge(hired_employees_department, jobs_data, left_on='job_id', right_on='id')

# agrupar los datos por trimestre, departamento y trabajo y contar el número de empleados contratados
result = hired_employees_department_job.groupby(['quarter', 'department', 'job']).agg({'id': 'count'}).rename(columns={'id': 'hired_employees'}).reset_index()

# ordenar el resultado por departamento y trabajo
result = result.sort_values(['department', 'job'])

print(result)


# crear columnas Q1, Q2, Q3, Q4 con valor 0
result['Q1'] = 0
result['Q2'] = 0
result['Q3'] = 0
result['Q4'] = 0

# actualizar las columnas Q1, Q2, Q3, Q4 con la sumatoria de empleados contratados por trimestre
result.loc[result['quarter'] == 1, 'Q1'] = result['hired_employees']
result.loc[result['quarter'] == 2, 'Q2'] = result['hired_employees']
result.loc[result['quarter'] == 3, 'Q3'] = result['hired_employees']
result.loc[result['quarter'] == 4, 'Q4'] = result['hired_employees']

# eliminar las columnas quarter y hired_employees
result.drop(['quarter', 'hired_employees'], axis=1, inplace=True)

# ordenar el resultado por departamento y trabajo
result = result.sort_values(['department', 'job'])


def create_plot(job):
    # Cargar los datos
    result = pd.read_csv("result_requirement1_final.csv")

    # Filtrar los datos por el trabajo especificado
    df_filtered = result[result['job'] == job]

    # Agrupar los datos por departamento y trabajo
    grouped = df_filtered.groupby(['department']).sum()

    # Crear un DataFrame con los valores de cada trimestre para cada departamento y trabajo
    quarters = ['Q1', 'Q2', 'Q3', 'Q4']
    data = pd.DataFrame(index=grouped.index, columns=quarters)
    for i, row in grouped.iterrows():
        for q in quarters:
            data.at[i, q] = row[q]

    # Crear la gráfica de barras apiladas
    fig, ax = plt.subplots(figsize=(12,8))
    data.plot(kind='bar', stacked=True, ax=ax)

    # Configurar el título y las etiquetas de los ejes
    ax.set_title(f'Empleados contratados por trimestre para el trabajo "{job}" en cada departamento')
    ax.set_xlabel('Departamento')
    ax.set_ylabel('Cantidad de empleados contratados')

    # Configurar la leyenda
    ax.legend(title='Trimestre', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Convertir la figura de matplotlib a imagen y mostrarla en Streamlit
    st.pyplot(fig)


# Definir la interfaz de usuario con Streamlit
st.title("Visualización de empleados contratados por trimestre")
job = st.text_input("Ingresa el nombre del trabajo:", "Web Designer I")
create_plot(job)
