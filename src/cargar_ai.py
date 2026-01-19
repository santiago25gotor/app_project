import requests
import os 
from datetime import datetime

def descargar_y_guardar(url, nombre_jugador):
    
    nombre_carpeta = os.path.join("data", "photos")
    if not os.path.exists(nombre_carpeta):
        print(f" Creando carpeta '{nombre_carpeta}'...")
        os.makedirs(nombre_carpeta)
 
    nombre_limpio = nombre_jugador.replace(" ", "_")
    
   
    extension = "png" if ".png" in url else "jpg"
    ruta_archivo = f"{nombre_carpeta}/{nombre_limpio}.{extension}"

    print(f"  Descargando imagen de {url}...")
    
    try:
        
        imagen_response = requests.get(url)
        
        if imagen_response.status_code == 200:
           
            with open(ruta_archivo, 'wb') as f:
                f.write(imagen_response.content)
            print(f" ¡Guardada! Revisa el archivo: {ruta_archivo}")
        else:
            print(" Error al descargar la imagen (Enlace roto).")
            
    except Exception as e:
        print(f"  Error guardando el archivo: {e}")

def ojeador_avanzado():
    nombre = input(" Dime el nombre del jugador para fichar y archivar: ")
    
    url = f"https://www.thesportsdb.com/api/v1/json/3/searchplayers.php?p={nombre}"
    
    print(f"🔎 Analizando base de datos...")
    
    try:
        response = requests.get(url)
        data = response.json()

        if not data.get('player'):
            print("❌ Jugador no encontrado.")
            return

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

     
        print("\n" + "═"*50)
        print(f"EXPEDIENTE: {nombre_oficial.upper()}")
        print("═"*50)
        print(f"Estado:      {estado}")       
        print(f"Deporte:     {deporte}")      
        print(f"Género:      {genero}")       
        print("─"*50)
        print(f"Equipo:      {equipo}")
        print(f"País:        {nacionalidad}")
        print(f"Posición:    {posicion}")
        print(f"Edad:        {edad} años")
        print("═"*50)

        
        if foto_url:
            print(f"Foto detectada. Iniciando protocolo de guardado...")
            descargar_y_guardar(foto_url, nombre_oficial)
        else:
            print("No hay foto disponible para descargar.")

        print("\n")

    except Exception as e:
        print(f"Error crítico: {e}")

if __name__ == "__main__":
    ojeador_avanzado()
