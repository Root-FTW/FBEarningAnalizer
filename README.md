# README.md

Este documento describe una secuencia de operaciones de limpieza y manipulación de datos implementadas en un script de Python. El código en cuestión se dirige específicamente a la manipulación de un conjunto de datos de videos y su información relacionada.

## Datos

El script se alimenta de un archivo .csv con un conjunto particular de columnas y atributos. Una descripción del formato requerido de los datos se presenta a continuación:

Columnas:
- 'Nombre de la página'
- 'Identificador del activo de video'
- 'Hora de publicación'
- 'Ingresos estimados (USD)'

Formatos:
- 'Hora de publicación' debería estar en el formato '%m/%d/%Y %H:%M'
- 'Ingresos estimados (USD)' debe ser numérico

## Dependencias

El script requiere las siguientes bibliotecas de Python:

- `pandas`
- `datetime`

Asegúrese de instalar estas dependencias utilizando pip:

```
pip install pandas datetime
```

## Ejecución

Para ejecutar el script, modifique la línea en la parte superior del código para apuntar hacia el archivo .csv que pretenden analizar:

```
file_path = 'TÚ_RUTA_AL_CSV'
```

Y en la línea en la parte inferior para apuntar hacia el lugar donde desea que se guarde el archivo de salida:

```
data_grouped.to_csv('TÚ_RUTA_AL_ARCHIVO_DE_SALIDA', index=False)
```

Luego, ejecute el script de Python desde la línea de comandos.

## Salida

El script realizará diversas operaciones de limpieza y transformación en el conjunto de datos y producirá como salida un archivo .csv que contiene filas del conjunto de datos original agrupadas por 'Nombre de la página', 'Identificador del activo de video', y 'Hora de publicación', con la suma de los 'Ingresos estimados (USD)' por cada grupo. 

Las filas con cero 'Ingresos estimados (USD)' serán filtradas en la salida.
