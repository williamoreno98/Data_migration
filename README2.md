# Solución reporte de metricas empleados

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
2. Todas las pruebas se realizaron en el notebook "Notebook_graphs.ipynb"
3. Se despliega la solución en un contenedor de docker funcional.
4. El front cuenta con un reporte completo con los requerimientos para que los stakeholders
puedan filtrar facilmente por tipo de trabajo y puedan ver un historico de los datos
de contratacion para tomar decisiones.
