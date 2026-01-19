
import requests
from datetime import datetime
import os
import pandas as pd
from .ver_laliga import cargar_clasificacion
from .scrape_laliga import extraer_clasificacion_laliga

def search_player_api(nombre):
    
    if not nombre:
        return {"error": "Nombre vacío"}
        
    url = f"https://www.thesportsdb.com/api/v1/json/3/searchplayers.php?p={nombre}"
    
    try:
        response = requests.get(url)
        data = response.json()

        if not data.get('player'):
            return {"error": "Jugador no encontrado"}

        jugador = data['player'][0]

        nombre_oficial = jugador.get('strPlayer', 'Desconocido')
        equipo = jugador.get('strTeam', 'Sin equipo')
        nacionalidad = jugador.get('strNationality', 'N/A')
        posicion = jugador.get('strPosition', 'N/A')
        estado = jugador.get('strStatus') 
        deporte = jugador.get('strSport') 
        genero = jugador.get('strGender') 

        nacimiento = jugador.get('dateBorn')
        edad = "??"
        if nacimiento:
            try:
                f_nac = datetime.strptime(nacimiento, '%Y-%m-%d')
                hoy = datetime.now()
                edad = hoy.year - f_nac.year - ((hoy.month, hoy.day) < (f_nac.month, f_nac.day))
            except: pass

        foto_url = jugador.get('strCutout') or jugador.get('strThumb')
        
        return {
            "nombre": nombre_oficial,
            "equipo": equipo,
            "nacionalidad": nacionalidad,
            "posicion": posicion,
            "estado": estado,
            "deporte": deporte,
            "genero": genero,
            "nacimiento": nacimiento,
            "edad": edad,
            "foto_url": foto_url,
            "description": jugador.get('strDescriptionEN', '') 
        }

    except Exception as e:
        return {"error": f"Error crítico: {str(e)}"}

def update_laliga_data_api():
    try:
        extraer_clasificacion_laliga()
        return {"status": "success", "message": "Datos actualizados correctamente desde Wikipedia"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_classification_data():
    df = cargar_clasificacion()
    if df is None:
        return {"error": "No data"}
   
    df = df.fillna("") 
    return df.to_dict(orient='records')

def get_team_stats(nombre_equipo):
    df = cargar_clasificacion()
    if df is None:
        return None
        
    resultado = df[df['Equipo'].str.contains(nombre_equipo, case=False, na=False)]
    
    if resultado.empty:
        return None
        
    equipo = resultado.iloc[0]
    
    pj = equipo['PJ']
    extra_stats = {}
    if pj > 0:
        extra_stats = {
            "puntos_por_partido": equipo['Pts'] / pj,
            "tasa_victorias": (equipo['G'] / pj) * 100,
            "tasa_empates": (equipo['E'] / pj) * 100,
            "tasa_derrotas": (equipo['P'] / pj) * 100,
            "eficiencia_ofensiva": equipo['GF'] / pj,
            "eficiencia_defensiva": equipo['GC'] / pj
        }
        
    data = equipo.fillna("").to_dict()
    data.update(extra_stats)
    
    for k, v in data.items():
        if isinstance(v, float) and (v != v): 
             data[k] = 0
             
    return data
