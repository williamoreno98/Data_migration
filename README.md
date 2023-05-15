# Challenge 2: Solución reporte de metricas empleados

Este proyecto tiene como objetivo realizar un reporte de dos vistas solicitadas por los 
stakeholders para toma de decisiones.

## ¿Cómo probarlo?
Ir al diccionario root del proyecto y escribir el siguiente comando:
streamlit run main_page.py 

Lo anterior despliega el front del reporte final con los
dos requerimientos.

Output: http://localhost:8501

## ¿Qué debo instalar?
pandas==2.0.1
matplotlib==3.7.1
streamlit==1.22.0

# Desarrollo de la solución

1. El front se despliega con streamlit en el archivo "main_page.py" dependiendo de 2 endpoints para
cada uno de los dos requirements que se encuentran en la carpetas "pages".
2. Las funciones de la logica para filtrar la data como se deseaba en el requerimiento 1 y 2 se encuentran 
en el archivo "utils.py" que es llamado en el front en "pages".
3. Todas las pruebas se realizaron en el notebook "Notebook_graphs.ipynb"
4. Se despliega la solución en un contenedor de docker funcional.
5. El front cuenta con un reporte completo con los requerimientos para que los stakeholders
puedan filtrar facilmente por tipo de trabajo y puedan ver un historico de los datos
de contratacion para tomar decisiones.
de la conexión de SQL server.
3. Todo se realiza en la rama "/Data_migration" y al final se hace merge con el 
otro challenge conservando todas las versiones del proceso de desarrollo realizado.
