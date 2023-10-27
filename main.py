# -*- coding: utf-8 -*-
import pandas as pd
from datetime import datetime, timedelta

# Load the data
file_path = 'C:/Users/rootf/Downloads/Jul-27-2023_Oct-26-2023_1529436154481158.csv'
data = pd.read_csv(file_path)

# Convert the 'Hora de publicación' column to datetime
data['Hora de publicación'] = pd.to_datetime(data['Hora de publicación'], format='%m/%d/%Y %H:%M')

# Get the current date and time
now = datetime.now()

# Calculate the cutoff date (5 days ago)
cutoff = now - timedelta(days=5)

# Filter the DataFrame
data = data[data['Hora de publicación'] < cutoff]

# Group the data and sum the earnings
data_grouped = data.groupby(['Nombre de la página', 'Identificador del activo de video', 'Hora de publicación'])['Ingresos estimados (USD)'].sum().reset_index()

# Filter rows with zero earnings
data_grouped = data_grouped[data_grouped['Ingresos estimados (USD)'] == 0]

# Export the data to a new CSV file
data_grouped.to_csv('C:/Users/rootf/Downloads/videos_earnings.csv', index=False)