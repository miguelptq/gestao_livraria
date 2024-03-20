import sqlite3
import os
import hashlib


class User:
    def __init__(self, username=None, password=None, email=None, role_id = 1):
        self._username = username
        self._password = password
        self._email = email
        self._logged_in_user = None
        self._role_id = role_id

    def get_username(self):
        return self._username
    
    def set_username(self, username):
        self._username = username
    
    def get_password(self):
        return self._password
    
    def set_password(self, password):
        self._password = password

    def get_email(self):
        return self._email
    
    def set_email(self, email):
        self._email = email

    def get_role_id(self):
        return self._role_id
    
    def set_role_id(self, role_id):
        self._role_id = role_id
    
    def register(self, permissions = None):
        if not self._username or not self._password or not self._email or not self._role_id:
            return False, "Error: Username, password and email must be provided..","Red"

        salt = os.urandom(16) # 16 ou 32

        # Gerar o hash sha-256
        password_hash = hashlib.pbkdf2_hmac('sha256', self._password.encode('UTF-8'), salt, 100000)

        # Converter salt e password hash para hexadecimal
        salt_hex = salt.hex()
        password_hash_hex = password_hash.hex()

        # Valor a ser gravado
        password_to_save = f'{salt_hex}:{password_hash_hex}'

        # Ligar a Base de Dados
        conn = sqlite3.connect('livraria.db')

        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO users (username, password, email, role_id) VALUES (?,?,?,?)", (self._username, password_to_save, self._email, self._role_id,)
            )
            new_user_id = cursor.lastrowid
            cursor.execute(f"""
                    INSERT INTO user_permissions (user_id, permission_id)
                        SELECT
                            {new_user_id} AS user_id,
                            p.id AS permission_id
                        FROM 
                           permissions p
                        WHERE
                           p.permission_name IN {permissions}
                """)
            # Commit the transaction
            conn.commit()
            return True, f"The user {self._username} was registered successfully.", "Green"
        except sqlite3.IntegrityError:
            # User with the same name or email already exists
            return False, "Error: Username or email is already in use.","Red"
        finally:
            # Close the connection
            conn.close()

    def login(self):
        if not self._username or not self._password:
            return False, "Error: Username and password must be provided.","Red"

        conn = sqlite3.connect('livraria.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (self._username,))
        result = cursor.fetchone()
        conn.close()

        if result:
            stored_password = result[2]
            salt_hex, stored_password_hash_hex = stored_password.split(':')
            salt = bytes.fromhex(salt_hex)
            password_hash = hashlib.pbkdf2_hmac('sha256', self._password.encode('UTF-8'), salt, 100000)
            password_hash_hex = password_hash.hex()
            
            if password_hash_hex == stored_password_hash_hex:
                self._logged_in_user = {
                    'id': result[0],
                    'username': result[1],
                    'role': result[4]
                }
                return True, f"Login successful as {self._username}.", "Green"
            else:
                return False, "Error: Incorrect password.", "Red"
        else:
            return False, "Error: User not found.", "Red"
        
    def get_logged_in_user(self):
        return self._logged_in_user

    def clear_logged_in_user(self):
        self._logged_in_user = None