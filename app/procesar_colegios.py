import pandas as pd

# Leer el archivo Excel (ajusta la ruta si es necesario)
df = pd.read_excel('colegios.xlsx')

# Verificar si la columna 'GEOPOSICION' existe en el archivo
if 'GEOPOSICION' in df.columns:
    # Crear nuevas columnas para latitud y longitud separadas
    df[['LATITUD', 'LONGITUD']] = df['GEOPOSICION'].str.split(',', expand=True)

    # Eliminar espacios en blanco extra en los datos de latitud y longitud
    df['LATITUD'] = df['LATITUD'].str.strip()
    df['LONGITUD'] = df['LONGITUD'].str.strip()

    # Verificar si los valores son numéricos y convertirlos
    df['LATITUD'] = pd.to_numeric(df['LATITUD'], errors='coerce')
    df['LONGITUD'] = pd.to_numeric(df['LONGITUD'], errors='coerce')

    # Guardar el DataFrame actualizado en un nuevo archivo Excel
    df.to_excel('colegios_procesados.xlsx', index=False)
    print("Archivo procesado y guardado como 'colegios_procesados.xlsx'.")
else:
    print("La columna 'GEOPOSICION' no se encontró en el archivo.")
