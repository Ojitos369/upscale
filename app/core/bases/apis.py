# Python
import os
import json
import datetime
from pathlib import Path
from inspect import currentframe

# Django
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response

# Ojitos369
from ojitos369.utils import get_d, print_line_center, printwln as pln
from ojitos369_mysql_db.mysql_db import ConexionMySQL

# User
from app.settings import MYE, prod_mode, ce, DB_DATA

class BaseApi(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.status = 200
        self.response = {}
        self.ce = ce
        self.MYE = MYE
        self.response_mode = 'json'

    def create_conexion(self):
        try:
            self.conexion.close()
        except:
            pass
        self.conexion = ConexionMySQL(DB_DATA, ce=self.ce)

    def errors(self, e):
        try:
            raise e
        except MYE as e:
            error = self.ce.show_error(e)
            print_line_center(error)
            self.status = 400 if self.status == 200 else self.status
            self.response = {
                'message': str(e),
                'error': str(e)
            }
        except Exception as e:
            extra_error_info = ""
            if hasattr(self, 'eei'):
                extra_error_info = self.eei
            error = self.ce.show_error(e, send_email=prod_mode, extra=extra_error_info)
            print_line_center(error)
            self.status = 500 if self.status == 200 else self.status
            self.response = {
                'message': str(e),
                'error': str(e)
            }

    def get_post_data(self):
        try:
            self.data = json.loads(self.request.body.decode('utf-8'))
        except:
            try:
                self.data = self.request.data
            except:
                self.data = {}
    
    def validate_session(self):
        request = self.request
        cookies = request.COOKIES
        mi_cookie = get_d(cookies, 'miCookie', default='')
        pln(mi_cookie)

    def validar_permiso(self, usuarios_validos):
        pass

    def show_me(self):
        class_name = self.__class__.__name__
        cf = currentframe()
        line = cf.f_back.f_lineno
        file_name = cf.f_back.f_code.co_filename
        
        print_line_center(f"{class_name} - {file_name}:{line} ")
    
    def get_text_color(self, color):
        color = color.replace("#", "")

        if len(color) == 6:
            r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        elif len(color) == 3:
            r = f"{color[0]}{color[0]}"
            g = f"{color[1]}{color[1]}"
            b = f"{color[2]}{color[2]}"
            r, g, b = int(r, 16), int(g, 16), int(b, 16)

        r, g, b = r / 255.0, g / 255.0, b / 255.0
        luminancia = 0.2126 * r + 0.7152 * g + 0.0722 * b
        color_texto = '#ffffff' if luminancia <= 0.5 else '#000000'

        return color_texto

    def get_random_color(self):
        color = f"#{os.urandom(3).hex()}"
        return color

    def normalize_text(self, text: str, acentos=True, transform=None):
        while '  ' in text:
            text = text.replace('  ', ' ')
        text = text.strip()
        if acentos:
            text = text.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
            text = text.replace('Á', 'A').replace('É', 'E').replace('Í', 'I').replace('Ó', 'O').replace('Ú', 'U')
        if transform:
            text = transform(text)

        return text

    def exec(self, request, **kwargs):
        self.request = request
        self.kwargs = kwargs
        try:
            if self.request.method in ('POST', 'PUT', 'PATCH'):
                self.get_post_data()
            elif self.request.method == 'GET':
                data = self.request.query_params
                self.data = {}
                for key, value in data.items():
                    self.data[key] = value
            self.validate_session()
            self.main()
        except Exception as e:
            self.errors(e)

        if self.response_mode == 'blob': 
            return self.response
        elif self.response_mode == 'json':
            return Response(self.response, status=self.status)


class PostApi(BaseApi):
    def post(self, request, **kwargs):
        return self.exec(request, **kwargs)


class GetApi(BaseApi):
    def get(self, request, **kwargs):
        return self.exec(request, **kwargs)


class PutApi(BaseApi):
    def put(self, request, **kwargs):
        return self.exec(request, **kwargs)


class DeleteApi(BaseApi):
    def delete(self, request, **kwargs):
        return self.exec(request, **kwargs)


class PatchApi(BaseApi):
    def patch(self, request, **kwargs):
        return self.exec(request, **kwargs)


class FullApi(BaseApi):
    def gen(self, request, **kwargs):
        return self.exec(request, **kwargs)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.post = self.get = self.put = self.patch = self.delete = self.gen
        
