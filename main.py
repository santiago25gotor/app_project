from src.auth import AuthSystem
from src.cargar_ai import ojeador_avanzado
from src.scrape_laliga import extraer_clasificacion_laliga
from src.ver_laliga import (
    cargar_clasificacion,
    mostrar_clasificacion_completa,
    buscar_equipo,
    generar_graficos_equipo,
    generar_grafico_clasificacion_top10
)

def display_menu():
    print("\n" + "="*40)
    print("    SISTEMA DE LOGIN - MENÚ PRINCIPAL")
    print("="*40)
    print("1. Iniciar sesión")
    print("2. Registrarse")
    print("3. Salir")
    print("="*40)

def display_user_menu(username):
    print("\n" + "="*40)
    print(f"    Sesión activa: {username}")
    print("="*40)
    print("1. Ver perfil")
    print("2. Buscar jugador (Ojeador AI)")
    print("3. Menú La Liga")
    print("4. Actualizar datos de La Liga")
    print("5. Cerrar sesión")
    print("6. Salir")
    print("="*40)

def menu_laliga():
    """Menú completo de La Liga"""
    df = cargar_clasificacion()
    
    if df is None:
        print("\n⚠️  No hay datos de La Liga disponibles.")
        print("💡 Ve a la opción 4 del menú principal para actualizar los datos.")
        input("\nPresiona Enter para continuar...")
        return
    
    while True:
        print("\n" + "="*80)
        print("MENÚ LA LIGA 2024-25".center(80))
        print("="*80)
        print("\n1. Ver clasificación completa")
        print("2. Buscar equipo por nombre")
        print("3. Generar gráficos de un equipo")
        print("4. Ver gráfico Top 10")
        print("5. Volver al menú principal")
        print("\n" + "="*80)
        
        opcion = input("\nSelecciona una opción (1-5): ").strip()
        
        if opcion == '1':
            mostrar_clasificacion_completa(df)
            input("\nPresiona Enter para continuar...")
        
        elif opcion == '2':
            nombre = input("\nIngresa el nombre del equipo (o parte del nombre): ").strip()
            if nombre:
                buscar_equipo(df, nombre)
                input("\nPresiona Enter para continuar...")
            else:
                print("\n❌ Debes ingresar un nombre.")
        
        elif opcion == '3':
            nombre = input("\nIngresa el nombre del equipo (o parte del nombre): ").strip()
            if nombre:
                generar_graficos_equipo(df, nombre)
                input("\nPresiona Enter para continuar...")
            else:
                print("\n❌ Debes ingresar un nombre.")
        
        elif opcion == '4':
            generar_grafico_clasificacion_top10(df)
            input("\nPresiona Enter para continuar...")
        
        elif opcion == '5':
            break
        
        else:
            print("\n❌ Opción no válida. Por favor, selecciona entre 1 y 5.")

def main():
    auth = AuthSystem()
    
    print("\n" + "="*60)
    print("    ⚽ SISTEMA DE GESTIÓN DE FÚTBOL ⚽".center(60))
    print("="*60)
    print("\n¡Bienvenido al sistema de autenticación!")
    print("Este sistema usa validaciones con expresiones regulares")
    print("Gestiona jugadores, equipos y estadísticas de La Liga\n")
    
    while True:
        if not auth.is_logged_in():
            display_menu()
            choice = input("\nSelecciona una opción: ").strip()
            
            if choice == "1":
                auth.login()
            elif choice == "2":
                auth.register()
            elif choice == "3":
                print("\n⚽ ¡Hasta pronto!")
                break
            else:
                print("\n❌ Opción inválida")
        else:
            display_user_menu(auth.current_user)
            choice = input("\nSelecciona una opción: ").strip()
            
            if choice == "1":
                print("\n" + "="*50)
                print("📋 PERFIL DE USUARIO".center(50))
                print("="*50)
                print(f"\n👤 Usuario: {auth.current_user}")
                print(f"📧 Email: {auth.db.users[auth.current_user]['email']}")
                print("="*50)
                input("\nPresiona Enter para continuar...")
                
            elif choice == "2":
                print("\n" + "="*50)
                print("🔍 OJEADOR DE JUGADORES".center(50))
                print("="*50)
                ojeador_avanzado()
                input("\nPresiona Enter para continuar...")
                
            elif choice == "3":
                menu_laliga()
                
            elif choice == "4":
                print("\n" + "="*50)
                print("📥 ACTUALIZAR DATOS DE LA LIGA".center(50))
                print("="*50)
                print("\nDescargando datos desde Wikipedia...")
                extraer_clasificacion_laliga()
                input("\nPresiona Enter para continuar...")
                
            elif choice == "5":
                auth.logout()
                
            elif choice == "6":
                auth.logout()
                print("\n⚽ ¡Hasta pronto!")
                break
                
            else:
                print("\n❌ Opción inválida")

if __name__ == "__main__":
    main()