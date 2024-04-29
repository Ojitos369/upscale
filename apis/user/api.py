# Python
import os
import json

# Django
from django.contrib.auth.hashers import make_password, check_password

# Ojitos369
from ojitos369.utils import get_d, generate_token

# User
from app.core.bases.apis import PostApi, GetApi
# 1046 -> 
class Login(PostApi):
    def main(self):
        self.show_me()
        self.create_conexion()
        login_error = "Error en las credenciales"

        user = self.data["user"]
        password = self.data["password"]
        query = """SELECT * 
                    FROM users
                    WHERE upper(username) = %s
                    or upper(correo) = %s
                    """ 
        params = (user.upper(), user.upper())

        r = self.conexion.consulta_asociativa(query, params)

        if not r:
            raise self.MYE(login_error)

        user = r[0]
        if not check_password(password, user["password"]):
            raise self.MYE(login_error)

        user.pop("password")
        exclude = "/{}();?+-<>!¡¿[]~^|="
        token = generate_token(exclude=exclude)
        
        query = """insert into sessions
                    (user_id, token)
                    values
                    (%s, %s) """
        query_data = (user["id_user"], token)
        
        if not self.conexion.ejecutar(query, query_data):
            self.conexion.rollback()
            raise self.MYE("Error al iniciar sesión")
    
        self.conexion.commit()

        user["token"] = token
        self.response = {
            "user": user,
        }


class ValidateLogin(GetApi):
    def main(self):
        self.show_me()
        self.create_conexion()
        
        query = """SELECT user_id
                    FROM sessions
                    WHERE token = %s """
        query_date = (self.token,)
        
        r = self.conexion.consulta_asociativa(query, query_date)
        
        if not r:
            raise self.MYE("Not Session")
        
        r = r[0]
        
        query = """SELECT *
                    FROM users
                    WHERE id_user = %s """
        query_data = (r["user_id"],)

        us = self.conexion.consulta_asociativa(query, query_data)
        
        if not us:
            raise self.MYE("Not Session")
        
        us = us[0]
        us.pop("password")
        us["token"] = self.token
        
        self.response = {
            "user": us,
        }
        
        

class CloseSession(GetApi):
    def main(self):
        self.show_me()
        self.create_conexion()
        
        query = """DELETE FROM sessions
                    WHERE token = %s """
        query_data = (self.token,)
        
        if not self.conexion.ejecutar(query, query_data):
            self.conexion.rollback()
            raise self.MYE("Error al cerrar sesión")
        
        self.conexion.commit()
        
        self.response = {
            "message": "Session closed"
        }
    

""" 
"""