# Python
import os
import json

# Ojitos369
from ojitos369.utils import get_d

# User
from app.core.bases.apis import PostApi, GetApi

class UpdateData(PostApi):
    def main(self):
        self.show_me()
        
        self.create_conexion()
        items = [
            {"name": 'sn1_fh2', "link": 'https://ojitos369.com/media/twice/ups/sn1_fh2.png', "model": "4x_foolhardy_Remacri", "scale": 2, "group": "sn1",
                "categorias": ["Sana", "Twice"]
            },
            {"name": 'sn1_pp2', "link": 'https://ojitos369.com/media/twice/ups/sn1_pp2.png', "model": "4xPurePhoto-span", "scale": 2, "group": "sn1",
                "categorias": ["Sana", "Twice"]
            },
            {"name": 'sn1_sp2', "link": 'https://ojitos369.com/media/twice/ups/sn1_sp2.png', "model": "ScuNet PSNR", "scale": 2, "group": "sn1",
                "categorias": ["Sana", "Twice"]
            },
        ]
        
        items = get_d(self.data, 'items', [])
        
        query = """INSERT INTO images 
                    (name, url, model, fecha, scale, group_image)
                    values
                    (%s, %s, %s, now(), %s, %s)
                """
        
        for i in items:
            name = i["name"]
            model = i["model"]
            scale = str(i["scale"])
            if not scale.endswith("x"):
                scale += "x"

            group = get_d(i, "group", default=None)

            data = [name, i["link"], model, scale, group]
            
            if not self.conexion.ejecutar(query, data):
                self.conexion.rollback()
                raise self.MYE("Error al guardar la imagen")
            
            self.conexion.commit()
            
            qt = """SELECT id_image
                    FROM images
                    WHERE name = %s
                    and url = %s
                    """
            qd = (i["name"], i["link"])
            r = self.conexion.consulta_asociativa(qt, qd)
            image_id = r[0]["id_image"]
            
            categorias = get_d(i, "categorias", [])
            
            if model not in categorias:
                categorias.append(model)
            if scale not in categorias:
                categorias.append(scale)
            
            qc = """SELECT id_categoria
                    FROM categorias
                    WHERE upper(nombre) = %s """
            
            for cat in categorias:
                name = cat.upper()
                qcd = (name,)
                r = self.conexion.consulta_asociativa(qc, qcd)
                
                if not r:
                    bg = self.get_random_color()
                    color = self.get_text_color(bg)
                    
                    qt = """insert into categorias
                            (nombre, bg, color)
                            values
                            (%s, %s, %s) """
                    qd = (name, bg, color)
                    if not self.conexion.ejecutar(qt, qd):
                        self.conexion.rollback()
                        raise self.MYE("Error al guardar la categoria")
                    self.conexion.commit()
                    r = self.conexion.consulta_asociativa(qc, qcd)
                id_categoria = r[0]["id_categoria"]
                
                
                qt = """insert into image_categoria
                        (image_id, categoria_id)
                        values
                        (%s, %s) """
                qd = (image_id, id_categoria)
                if not self.conexion.ejecutar(qt, qd):
                    self.conexion.rollback()
                    raise self.MYE("Error al guardar la categoria")
                self.conexion.commit()

        self.conexion.commit()
        
        self.response = {
            "message": "Datos guardados correctamente"
        }