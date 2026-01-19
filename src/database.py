# src/database.py
import json
import os
import hashlib
from datetime import datetime, timedelta
import random

class Database:
    def __init__(self, data_folder='data'):
        self.data_folder = data_folder
        self.users_file = os.path.join(data_folder, 'users.json')
        self.pending_file = os.path.join(data_folder, 'pending_users.json')

        self.users = {}
        self.pending = {}

        self._ensure_data_folder()
        self._load_users()
        self._load_pending()

    def _ensure_data_folder(self):
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)

    def _load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r', encoding='utf-8') as f:
                self.users = json.load(f)

    def _save_users(self):
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, indent=4, ensure_ascii=False)

    def _load_pending(self):
        if os.path.exists(self.pending_file):
            with open(self.pending_file, 'r', encoding='utf-8') as f:
                self.pending = json.load(f)

    def _save_pending(self):
        with open(self.pending_file, 'w', encoding='utf-8') as f:
            json.dump(self.pending, f, indent=4, ensure_ascii=False)

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def _new_code(self):
        code = str(random.randint(100000, 999999))
        expires_at = (datetime.now() + timedelta(minutes=10)).isoformat()
        return code, expires_at

    def user_exists(self, username: str) -> bool:
        return username in self.users

    def pending_exists(self, username: str) -> bool:
        return username in self.pending

    def email_exists(self, email: str) -> bool:
        return any(user.get('email') == email for user in self.users.values())

    def pending_email_exists(self, email: str) -> bool:
        return any(u.get('email') == email for u in self.pending.values())

    def find_username_by_email(self, email: str):
        for uname, u in self.users.items():
            if u.get("email") == email:
                return uname
        return None

    def find_pending_username_by_email(self, email: str):
        for uname, u in self.pending.items():
            if u.get("email") == email:
                return uname
        return None

    
    def register_user(self, username: str, email: str, password: str):
        if self.user_exists(username):
            return False, "El usuario ya existe"

        if self.email_exists(email):
            return False, "El email ya está registrado"

        
        if self.pending_exists(username) or self.pending_email_exists(email):
            return False, "Ya existe un registro pendiente de verificación. Revisa tu correo o reenvía el código."

        verification_code, expires_at = self._new_code()

        self.pending[username] = {
            "email": email,
            "password": self._hash_password(password),
            "verification_code": verification_code,
            "code_expires_at": expires_at
        }
        self._save_pending()

        return True, verification_code

   
    def verify_user(self, username: str, code: str):
        if not self.pending_exists(username):
            
            if self.user_exists(username):
                if self.users[username].get("verified", False):
                    return True, "La cuenta ya está verificada"
                return False, "Cuenta existente pero en estado inválido. Contacta soporte."
            return False, "Usuario no encontrado (no hay registro pendiente)."

        p = self.pending[username]

        if p.get("verification_code") != code:
            return False, "Código incorrecto"

        expires_at = p.get("code_expires_at")
        if expires_at and datetime.now() > datetime.fromisoformat(expires_at):
            return False, "Código expirado"

        # mover a users
        self.users[username] = {
            "email": p["email"],
            "password": p["password"],
            "verified": True,
            "verification_code": None,
            "code_expires_at": None,
            "reset_code": None,
            "reset_expires_at": None
        }
        del self.pending[username]

        self._save_users()
        self._save_pending()

        return True, "Cuenta verificada correctamente"

    def resend_verification_code(self, username: str = None, email: str = None):
        if not username and not email:
            return False, "Debe enviarse username o email"

        if not username and email:
            username = self.find_pending_username_by_email(email)

        if not username or not self.pending_exists(username):
            return False, "Usuario no encontrado o no hay registro pendiente"

        p = self.pending[username]

        new_code, expires_at = self._new_code()
        p["verification_code"] = new_code
        p["code_expires_at"] = expires_at
        self._save_pending()

        return True, {"username": username, "email": p.get("email"), "code": new_code}

    def authenticate(self, username: str, password: str):
        if not self.user_exists(username):
            
            if self.pending_exists(username):
                return False, "Cuenta pendiente de verificación. Revisa tu correo."
            return False, "Usuario no encontrado"

        user = self.users[username]

        if user.get('password') != self._hash_password(password):
            return False, "Contraseña incorrecta"

        if not user.get("verified", False):
            return False, "Cuenta no verificada. Revisa tu correo."

        return True, "Inicio de sesión exitoso"

    
    def request_password_reset(self, username: str = None, email: str = None):
        if not username and not email:
            return False, "Debe enviarse username o email"

        if not username and email:
            username = self.find_username_by_email(email)

        if not username or not self.user_exists(username):
            return False, "Usuario no encontrado"

        code, expires_at = self._new_code()
        self.users[username]["reset_code"] = code
        self.users[username]["reset_expires_at"] = expires_at
        self._save_users()

        return True, {"username": username, "email": self.users[username]["email"], "code": code}

    def reset_password(self, username: str, code: str, new_password: str):
        if not self.user_exists(username):
            return False, "Usuario no encontrado"

        u = self.users[username]

        if u.get("reset_code") != code:
            return False, "Código incorrecto"

        expires_at = u.get("reset_expires_at")
        if expires_at and datetime.now() > datetime.fromisoformat(expires_at):
            return False, "Código expirado"

        u["password"] = self._hash_password(new_password)
        u["reset_code"] = None
        u["reset_expires_at"] = None
        self._save_users()

        return True, "Contraseña actualizada correctamente"
