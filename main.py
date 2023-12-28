-- coding: utf-8 --
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

Establece la configuración de la página con un diseño más amplio
st.set_page_config(layout="wide")

def main():
st.title('Análisis de Video')
st.write('Por favor, sube un archivo CSV con información de video para la analítica')

data_upload = st.file_uploader("Seleccione un archivo CSV", type="csv")

if data_upload is not None:
    data = load_data(data_upload)
    # Agrega un filtro para seleccionar el nombre de la página
    unique_pages = data['Nombre de la página'].unique()
    selected_page = st.selectbox('Filtrar por nombre de la página:', ['Todos'] + list(unique_pages))
    
    if selected_page != 'Todos':
        data = data[data['Nombre de la página'] == selected_page]
    
    processed_data = process_data(data)
    st.success('Análisis completado!')
    # Utiliza todo el ancho de la página para el DataFrame
    st.dataframe(processed_data, width=1500)
def load_data(file):
# Carga el archivo CSV a un dataframe
data = pd.read_csv(file)

# Formatea 'Hora de publicación' como valor datetime
data['Hora de publicación'] = pd.to_datetime(data['Hora de publicación'], format='%m/%d/%Y %H:%M')

return data
def process_data(data):
# Obtiene la fecha/hora actual
now = datetime.now()

# Calcula la fecha de corte (5 días atrás)
cutoff = now - timedelta(days=5)

# Filtra el dataframe para incluir solo registros antes de la fecha de corte
data = data[data['Hora de publicación'] < cutoff]

# Agrupa y suma los valores de las tres columnas de interés
data_grouped = data.groupby(['Nombre de la página', 'Identificador del activo de video', 'Hora de publicación']).agg({
    'Ingresos estimados (USD)': 'sum',
    'Veces que se compartió': 'sum',
    'Reproducciones de video de 3 segundos': 'sum'
}).reset_index()

# Filtra para mostrar solo registros donde los ingresos estimados son igual a cero
data_grouped = data_grouped[data_grouped['Ingresos estimados (USD)'] == 0]

# Convert the 'Identificador del activo de video' column to String
data_grouped['Identificador del activo de video'] = data_grouped['Identificador del activo de video'].astype(str)

return data_grouped
if name == "main":
main()
