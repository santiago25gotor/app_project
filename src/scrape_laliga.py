import pandas as pd
import requests
import os

def extraer_clasificacion_laliga():

    url = "https://es.wikipedia.org/wiki/Primera_Divisi%C3%B3n_de_Espa%C3%B1a_2024-25"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

    try:
        print(f"Extrayendo datos de: {url}...")
        
        # Obtenemo el contenido con requests por los headers
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'

        # TODAS las tablas de la página de golpe
       
        tablas = pd.read_html(response.text)
        
        df_clasificacion = None

        # identificamos porque debe tener columnas como 'Equipo', 'Pt' y 'PJ'
        for tabla in tablas:
            columnas = " ".join(tabla.columns.astype(str)).lower()
            if 'equipo' in columnas and 'pts' in columnas and 'pj' in columnas:
                df_clasificacion = tabla
                break

        if df_clasificacion is not None:
           
            if df_clasificacion.columns[0] == 'Unnamed: 0' or 'Pos' not in df_clasificacion.columns[0]:
                df_clasificacion.rename(columns={df_clasificacion.columns[0]: 'Pos'}, inplace=True)

            # Eliminamos filas que puedan ser notas al pie de la tabla
            df_clasificacion = df_clasificacion.dropna(subset=['Equipo'])
            
            # Limpiamos los nombres de los equipos (a veces traen notas tipo [n 1] o (C))
            df_clasificacion['Equipo'] = df_clasificacion['Equipo'].str.replace(r'\(.*\)', '', regex=True).str.strip()
            df_clasificacion['Equipo'] = df_clasificacion['Equipo'].str.replace(r'\[.*\]', '', regex=True).str.strip()

            carpeta = "csv's"
            if not os.path.exists(carpeta):
                os.makedirs(carpeta)
                print(f"Carpeta '{carpeta}' creada.")
        
            nombre_archivo = os.path.join(carpeta, 'clasificacion_laliga_24_25.csv')
            df_clasificacion.to_csv(nombre_archivo, index=False, encoding='utf-8-sig')
            
            print(f"¡Éxito! Tabla encontrada y guardada en '{nombre_archivo}'")
            print(df_clasificacion.head()) # Mostrar las primeras filas por consola
        else:
            print("No se encontró la tabla de clasificación en esta página.")

    except Exception as e:
        print(f"Hubo un error: {e}")

if __name__ == "__main__":
    extraer_clasificacion_laliga()