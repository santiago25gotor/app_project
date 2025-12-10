import json
import os
import hashlib

class Database:
    def __init__(self, data_folder='data'):
        self.data_folder = data_folder
        self.users_file = os.path.join(data_folder, 'users.json')
        self.users = {}
        self._ensure_data_folder()
        self._load_users()
    
    def _ensure_data_folder(self):
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
    
    def _load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
    
    def _save_users(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=4)
    
    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def user_exists(self, username):
        return username in self.users
    
    def email_exists(self, email):
        return any(user['email'] == email for user in self.users.values())
    
    def register_user(self, username, email, password):
        if self.user_exists(username):
            return False, "El usuario ya existe"
        
        self.users[username] = {
            'email': email,
            'password': self._hash_password(password)
        }
        self._save_users()
        return True, "Usuario registrado exitosamente"
    
    def authenticate(self, username, password):
        if not self.user_exists(username):
            return False, "Usuario no encontrado"
        
        if self.users[username]['password'] == self._hash_password(password):
            return True, "Inicio de sesión exitoso"
        
        return False, "Contraseña incorrecta"