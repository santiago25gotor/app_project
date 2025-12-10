from src.auth import AuthSystem

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
    print("2. Cerrar sesión")
    print("3. Salir")
    print("="*40)

def main():
    auth = AuthSystem()
    
    print("\n¡Bienvenido al sistema de autenticación!")
    print("Este sistema usa validaciones con expresiones regulares\n")
    
    while True:
        if not auth.is_logged_in():
            display_menu()
            choice = input("\nSelecciona una opción: ").strip()
            
            if choice == "1":
                auth.login()
            elif choice == "2":
                auth.register()
            elif choice == "3":
                print("\n ¡Hasta pronto!")
                break
            else:
                print("\n Opción inválida")
        else:
            display_user_menu(auth.current_user)
            choice = input("\nSelecciona una opción: ").strip()
            
            if choice == "1":
                print(f"\n Usuario: {auth.current_user}")
                print(f" Email: {auth.db.users[auth.current_user]['email']}")
            elif choice == "2":
                auth.logout()
            elif choice == "3":
                auth.logout()
                print("\n ¡Hasta pronto!")
                break
            else:
                print("\n Opción inválida")

if __name__ == "__main__":
    main()