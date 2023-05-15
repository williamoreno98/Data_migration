from utils import *

st.markdown("# Page 2 🏙")
st.sidebar.markdown("# Mayores contrataciones por departmento 🏙")
year=st.selectbox("Year to analyze", [2021,2022])
# Convertir la figura de matplotlib a imagen y mostrarla en Streamlit

create_plot3(year)
lista_top=top(year)

st.table(lista_top)
