# -*- coding: utf-8 -*-
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

def main():
    st.title('Análisis de Video')
    st.write('Por favor, sube un archivo CSV con información de video para la analítica')

    data_upload = st.file_uploader("Seleccione un archivo CSV", type="csv")

    if data_upload is not None:
        data = load_data(data_upload)
        process_data(data)
        st.success('Análisis completado!')

def load_data(file):
    # Carga el archivo CSV a un dataframe
    data = pd.read_csv(file)

    # Formatea 'Hora de publicación' como valor datetime
    data['Hora de publicación'] = pd.to_datetime(data['Hora de publicación'], format='%m/%d/%Y %H:%M')

    return data

def process_data(data):
    # Obtiene la fecha/hora actual
    now = datetime.now()

    # Calcula la fecha de inicio (10 días atrás)
    start_date = now - timedelta(days=10)

    # Calcula la fecha de corte (5 días atrás)
    cutoff_date = now - timedelta(days=5)

    # Filtra el dataframe para incluir solo los datos dentro del rango de tiempo deseado
    data_filtered = data[(data['Hora de publicación'] >= start_date) & (data['Hora de publicación'] < cutoff_date)]

    # Agrupa y suma los ingresos
    data_grouped = data_filtered.groupby(['Nombre de la página', 'Identificador del activo de video', 'Hora de publicación'])['Ingresos estimados (USD)'].sum().reset_index()

    # Convierte la columna 'Identificador del activo de video' a String
    data_grouped['Identificador del activo de video'] = data_grouped['Identificador del activo de video'].astype(str)

    # Filtra registros con cero ingresos
    data_no_income = data_grouped[data_grouped['Ingresos estimados (USD)'] == 0]

    # Muestra los datos
    st.dataframe(data_no_income)

if __name__ == "__main__":
    main()
