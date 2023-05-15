from utils import *

st.markdown("# Page 1 🚀")
st.sidebar.markdown("# Empleados contratados por trimestre 2021 🚀")

st.title("Visualización de empleados contratados por trimestre 2021")
create_plot2()
jobs_data = pd.read_csv('./Input_data/jobs.csv', header=None, names=['id', 'job'])
job = st.selectbox("Selecciona el trabajo:", jobs_data["job"])
create_plot(job)

# Cargar los datos
result = pd.read_csv("result_requirement1_final.csv")

st.table(result)

