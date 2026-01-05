import pandas as pd
import matplotlib.pyplot as plt
import os

def cargar_clasificacion():
    
    try:
        archivo = os.path.join("csv's", 'clasificacion_laliga_24_25.csv')
        df = pd.read_csv(archivo, encoding='utf-8-sig')
        
        
        df.columns = df.columns.str.strip().str.rstrip('.')
        
        print(f"Columnas encontradas: {list(df.columns)}")
        
        return df
    except FileNotFoundError:
        print("Error: No se encontró el archivo de clasificación.")
        print("Primero ejecuta scrape_premier_league.py para generar los datos.")
        return None

def mostrar_clasificacion_completa(df):
    
    print("\n" + "="*100)
    print("CLASIFICACIÓN LA LIGA 2024-25".center(100))
    print("="*100)
    print(df.to_string(index=False))
    print("="*100 + "\n")

def buscar_equipo(df, nombre_equipo):
    
    resultado = df[df['Equipo'].str.contains(nombre_equipo, case=False, na=False)]
    
    if resultado.empty:
        print(f"\nNo se encontró ningún equipo con el nombre '{nombre_equipo}'")
        print("\nEquipos disponibles:")
        for i, equipo in enumerate(df['Equipo'], 1):
            print(f"{i}. {equipo}")
        return None
    
    equipo = resultado.iloc[0]
    
    print("\n" + "="*80)
    print(f"ESTADÍSTICAS DE {equipo['Equipo']}".center(80))
    print("="*80)

    print(f"\nPosición: {equipo['Pos']}")
    print(f"Puntos: {equipo['Pts']}")
    print(f"Partidos Jugados: {equipo['PJ']}")
  
    print(f"\nVictorias: {equipo['G']}")
    print(f"Empates: {equipo['E']}")
    print(f"Derrotas: {equipo['P']}")

    print(f"\nGoles a Favor: {equipo['GF']}")
    print(f"Goles en Contra: {equipo['GC']}")
    print(f"Diferencia de Goles: {equipo['Dif']}")
    

    pj = equipo['PJ']
    if pj > 0:
        
        puntos_por_partido = equipo['Pts'] / pj
        print(f"\n--- MÉTRICAS AVANZADAS ---")
        print(f"Puntos por Partido: {puntos_por_partido:.2f}")
        
      
        tasa_victorias = (equipo['G'] / pj) * 100
        print(f"Tasa de Victorias: {tasa_victorias:.1f}%")
        
    
        tasa_empates = (equipo['E'] / pj) * 100
        print(f"Tasa de Empates: {tasa_empates:.1f}%")
        
   
        tasa_derrotas = (equipo['P'] / pj) * 100
        print(f"Tasa de Derrotas: {tasa_derrotas:.1f}%")
        
      
        eficiencia_ofensiva = equipo['GF'] / pj
        print(f"\nEficiencia Ofensiva: {eficiencia_ofensiva:.2f} goles/partido")
        
        
        eficiencia_defensiva = equipo['GC'] / pj
        print(f"Eficiencia Defensiva: {eficiencia_defensiva:.2f} goles recibidos/partido")
        
       
        if eficiencia_defensiva > 0:
            solidez = 1 / eficiencia_defensiva
            print(f"Solidez Defensiva: {solidez:.2f}")
        

        if eficiencia_defensiva > 0:
            balance = eficiencia_ofensiva / eficiencia_defensiva
            print(f"Balance Ofensivo/Defensivo: {balance:.2f}")
            if balance > 1.5:
                print("  → Equipo muy ofensivo")
            elif balance > 1:
                print("  → Equipo equilibrado con ventaja ofensiva")
            elif balance > 0.7:
                print("  → Equipo equilibrado")
            else:
                print("  → Equipo defensivo")
    
    print("="*80 + "\n")
    
    return equipo

def generar_graficos_equipo(df, nombre_equipo):
    
    resultado = df[df['Equipo'].str.contains(nombre_equipo, case=False, na=False)]
    
    if resultado.empty:
        print(f"\nNo se encontró ningún equipo con el nombre '{nombre_equipo}'")
        return
    
    equipo = resultado.iloc[0]
    nombre = equipo['Equipo']
    
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'Estadísticas de {nombre} - La Liga 2024/25', fontsize=16, fontweight='bold')
    

    ax1 = axes[0, 0]
    resultados = [equipo['G'], equipo['E'], equipo['P']]
    colores = ['#2ecc71', '#f39c12', '#e74c3c']
    wedges, texts, autotexts = ax1.pie(resultados, labels=['Victorias', 'Empates', 'Derrotas'], 
            autopct='%1.1f%%', colors=colores, startangle=90)
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    ax1.set_title('Distribución de Resultados')
    

    ax2 = axes[0, 1]
    categorias = ['Goles a Favor', 'Goles en Contra']
    valores = [equipo['GF'], equipo['GC']]
    colores_goles = ['#3498db', '#e74c3c']
    barras = ax2.bar(categorias, valores, color=colores_goles, edgecolor='black', linewidth=1.5)
    ax2.set_ylabel('Goles', fontweight='bold')
    ax2.set_title('Goles a Favor vs Goles en Contra')
    ax2.grid(axis='y', alpha=0.3)

    for barra in barras:
        altura = barra.get_height()
        ax2.text(barra.get_x() + barra.get_width()/2., altura,
                f'{int(altura)}', ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    
    ax3 = axes[1, 0]
    pj = equipo['PJ']
    if pj > 0:
        eficiencias = {
            'Puntos/Partido': equipo['Pts'] / pj,
            'Goles/Partido': equipo['GF'] / pj,
            'Goles Rec./Partido': equipo['GC'] / pj
        }
        colores_ef = ['#9b59b6', '#2ecc71', '#e74c3c']
        barras = ax3.barh(list(eficiencias.keys()), list(eficiencias.values()), 
                color=colores_ef, edgecolor='black', linewidth=1.5)
        ax3.set_xlabel('Promedio', fontweight='bold')
        ax3.set_title('Promedios por Partido')
        ax3.grid(axis='x', alpha=0.3)
       
        for i, (k, v) in enumerate(eficiencias.items()):
            ax3.text(v + 0.05, i, f'{v:.2f}', va='center', fontweight='bold')
    

    ax4 = axes[1, 1]
    if pj > 0:
        tasas = {
            'Victorias': (equipo['G'] / pj) * 100,
            'Empates': (equipo['E'] / pj) * 100,
            'Derrotas': (equipo['P'] / pj) * 100
        }
        colores_tasas = ['#2ecc71', '#f39c12', '#e74c3c']
        barras = ax4.bar(list(tasas.keys()), list(tasas.values()), color=colores_tasas,
                        edgecolor='black', linewidth=1.5)
        ax4.set_ylabel('Porcentaje (%)', fontweight='bold')
        ax4.set_title('Tasa de Resultados')
        ax4.set_ylim(0, 100)
        ax4.grid(axis='y', alpha=0.3)

        for barra in barras:
            altura = barra.get_height()
            ax4.text(barra.get_x() + barra.get_width()/2., altura + 1,
                    f'{altura:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    
    carpeta_graficos = "graficos"
    if not os.path.exists(carpeta_graficos):
        os.makedirs(carpeta_graficos)
    
    nombre_archivo = os.path.join(carpeta_graficos, f'{nombre.replace(" ", "_").replace(".", "")}_estadisticas.png')
    plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight')
    print(f"\n✓ Gráfico guardado en: {nombre_archivo}")
    
    plt.show()
    plt.close(fig)
    

def generar_grafico_clasificacion_top10(df):
    top10 = df.head(10).copy()
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    colores = plt.cm.RdYlGn(top10['Pts'] / top10['Pts'].max())
    barras = ax.barh(range(len(top10)), top10['Pts'], color=colores, edgecolor='black', linewidth=1.5)
    
    ax.set_yticks(range(len(top10)))
    ax.set_yticklabels(top10['Equipo'])
    ax.invert_yaxis()  
    ax.set_xlabel('Puntos', fontsize=12, fontweight='bold')
    ax.set_title('Top 10 - Clasificación La Liga 2024/25', fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3)
    
    for i, (idx, row) in enumerate(top10.iterrows()):
        ax.text(row['Pts'] + 1, i, f"{int(row['Pts'])} pts", 
               va='center', fontweight='bold')
    
    plt.tight_layout()

    carpeta_graficos = "graficos"
    if not os.path.exists(carpeta_graficos):
        os.makedirs(carpeta_graficos)
    
    nombre_archivo = os.path.join(carpeta_graficos, 'top10_clasificacion.png')
    plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight')
    print(f"\n✓ Gráfico guardado en: {nombre_archivo}")
    
    plt.show()
    plt.close(fig)

def menu_principal():
    
    df = cargar_clasificacion()
    
    if df is None:
        return
    
    while True:
        print("\n" + "="*80)
        print("MENÚ LA LIGA 2024-25".center(80))
        print("="*80)
        print("\n1. Ver clasificación completa")
        print("2. Buscar equipo por nombre")
        print("3. Generar gráficos de un equipo")
        print("4. Ver gráfico Top 10")
        print("5. Salir")
        print("\n" + "="*80)
        
        opcion = input("\nSelecciona una opción (1-5): ").strip()
        
        if opcion == '1':
            mostrar_clasificacion_completa(df)
        
        elif opcion == '2':
            nombre = input("\nIngresa el nombre del equipo (o parte del nombre): ").strip()
            if nombre:
                buscar_equipo(df, nombre)
            else:
                print("\n❌ Debes ingresar un nombre.")
        
        elif opcion == '3':
            nombre = input("\nIngresa el nombre del equipo (o parte del nombre): ").strip()
            if nombre:
                generar_graficos_equipo(df, nombre)
            else:
                print("\n❌ Debes ingresar un nombre.")
        
        elif opcion == '4':
            generar_grafico_clasificacion_top10(df)
        
        elif opcion == '5':
            print("\n¡Hasta luego!")
            break
        
        else:
            print("\n❌ Opción no válida. Por favor, selecciona entre 1 y 5.")

if __name__ == "__main__":
    menu_principal()