
import sys
import os
# Add current directory to path so we can import src
sys.path.append(os.getcwd())

from src.ver_laliga import cargar_clasificacion

print("Probando carga de clasificación...")
try:
    df = cargar_clasificacion()
    if df is not None:
        print("Carga exitosa!")
        print(df.head())
    else:
        print("Carga fallida: devolvió None")
except Exception as e:
    print(f"Excepción durante carga: {e}")
