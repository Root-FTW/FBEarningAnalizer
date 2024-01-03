# -*- coding: utf-8 -*-
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

# Establece la configuración de la página con un diseño más amplio
st.set_page_config(layout="wide")

def main():
    st.title('Análisis de Video')
    st.write('Por favor, sube un archivo CSV con información de video para la analítica')

    data_upload = st.file_uploader("Seleccione un archivo CSV", type="csv")

    if data_upload is not None:
        data = load_data(data_upload)
        # Filtro para seleccionar el nombre de la página
        unique_pages = data['Nombre de la página'].unique()
        selected_page = st.selectbox('Filtrar por nombre de la página:', ['Todos'] + list(unique_pages))
        
        # Filtros adicionales con valores mínimos y máximos
        min_shares, max_shares = st.slider('Filtrar por el número de veces que se compartió:', 0, int(data['Veces que se compartió'].max()), (0, int(data['Veces que se compartió'].max())))
        ingresos_minimos_para_considerar = 0.0001
        min_earnings, max_earnings = st.slider('Filtrar por el rango de ingresos estimados (USD):', 0.0, float(data['Ingresos estimados (USD)'].max()), (0.0, float(data['Ingresos estimados (USD)'].max())))
        min_views, max_views = st.slider('Filtrar por el rango de reproducciones de video de 3 segundos:', 0, int(data['Reproducciones de video de 3 segundos'].max()), (0, int(data['Reproducciones de video de 3 segundos'].max())))

        # Aplicar filtros
        if selected_page != 'Todos':
            data = data[data['Nombre de la página'] == selected_page]

        data = data[(data['Veces que se compartió'] >= min_shares) & (data['Veces que se compartió'] <= max_shares)]
        data = data[((data['Ingresos estimados (USD)'] >= min_earnings) & (data['Ingresos estimados (USD)'] <= max_earnings)) | (data['Ingresos estimados (USD)'] < ingresos_minimos_para_considerar)]
        data = data[(data['Reproducciones de video de 3 segundos'] >= min_views) & (data['Reproducciones de video de 3 segundos'] <= max_views)]

        processed_data = process_data(data)
        st.success('Análisis completado!')
        st.dataframe(processed_data.style.format({'Ingresos estimados (USD)': '{:.4f}'}))

def load_data(file):
    # Carga el archivo CSV a un dataframe y especificamos los tipos de datos
    data = pd.read_csv(file, dtype={'Ingresos estimados (USD)': 'float64'})

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

    # Agrupa y suma los valores de las tres columnas de interés por 'Nombre de la página', 'Identificador del activo de video', y 'Hora de publicación'
    data_grouped = data.groupby(['Nombre de la página', 'Identificador del activo de video', 'Hora de publicación']).agg({
        'Ingresos estimados (USD)': 'sum',
        'Veces que se compartió': 'sum',
        'Reproducciones de video de 3 segundos': 'sum'
    }).reset_index()

    # Convierte la columna 'Identificador del activo de video' a String
    data_grouped['Identificador del activo de video'] = data_grouped['Identificador del activo de video'].astype(str)

    return data_grouped

if __name__ == "__main__":
    main()
