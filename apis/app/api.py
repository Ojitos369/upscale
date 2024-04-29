# Python
import os
import json

# Ojitos369
from ojitos369.utils import get_d

from app.core.sd import StableDiffApi as SDA

# User
from app.core.bases.apis import PostApi, GetApi
from app.settings import MEDIA_DIR

class UpdateInitData(PostApi, GetApi):
    def main(self):
        self.show_me()
        
        self.create_conexion()

        items = []

        models = {
            "fr": "4x_foolhardy_Remacri",
            "pp": "4xPurePhoto-span",
            "snp": "ScuNet PSNR",
            "d4": "DAT x4",
        }
        
        bases = [
            {"name": "cy_1", "cantidad": 1, "cats": ["Chaeyoung", "Twice"]},
            {"name": "mn_fd", "cantidad": 11, "cats": ["Mina", "Twice"]},
            {"name": "sn_bb", "cantidad": 40, "cats": ["Sana", "Twice"]},
            {"name": "cy_ig_2", "cantidad": 1, "cats": ["Chaeyoung", "Twice"]},
            {"name": "mm_ig_1", "cantidad": 10, "cats": ["Momo", "Twice"]},
            {"name": "mm_ig_2", "cantidad": 7, "cats": ["Momo", "Twice"]},
        ]
        
        query_gg = """SELECT distinct general_group
                    FROM images
                    """
        r = self.conexion.consulta_asociativa(query_gg)
        ggs = [i["general_group"] for i in r]
        
        agregados = []
        repetidos = []
        
        for b in bases:
            general_group = b["name"]
            if general_group in ggs:
                print(f"Ya existe el grupo {general_group}")
                repetidos.append(general_group)
                continue

            for i in range(1, b["cantidad"] + 1):
                group = name = f"{b['name']}_{i}"
                link = f"https://ojitos369.com/media/twice/ups/{name}.jpg"
                item = {"name": name, "link": link, "model": "Original", "scale": 1, "group": group, "general_group": general_group}
                item["categorias"] = [*b["cats"]]
                items.append(item)

                for k, v in models.items():
                    name = f"{b['name']}_{i}_{k}_2x"
                    link = f"https://ojitos369.com/media/twice/ups/{name}.png"
                    item = {"name": name, "link": link, "model": v, "scale": 2, "group": group, "general_group": general_group}
                    item["categorias"] = [*b["cats"]]
                    items.append(item)
            
            agregados.append(general_group)

        query = """INSERT INTO images 
                    (name, url, model, fecha, scale, group_image, general_group)
                    values
                    (%s, %s, %s, now(), %s, %s, %s)
                """

        for i in items:
            name = i["name"]
            model = i["model"]
            scale = str(i["scale"])
            if not scale.endswith("x"):
                scale += "x"

            group = get_d(i, "group", default=None)
            general_group = get_d(i, "general_group", default=None)

            data = [name, i["link"], model, scale, group, general_group]
            
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
            "message": "Datos guardados correctamente",
            "agregados": agregados,
            "repetidos": repetidos,
            "cantidad": len(items)
        }


class GetImages(GetApi):
    def main(self):
        self.show_me()
        
        self.create_conexion()
        # print(self.data)
        name = get_d(self.data, "name", default=None)
        model = get_d(self.data, "model", default=None)
        fi = get_d(self.data, "fi", default=None) # fecha_inicio
        ff = get_d(self.data, "ff", default=None) # fecha_fin
        scale = get_d(self.data, "scale", default=None)
        group_image = get_d(self.data, "gi", default=None)
        general_group = get_d(self.data, "gg", default=None)
        categorias = get_d(self.data, "cats", default=None)
        
        filtros = "WHERE 1=1\n"
        query_data = []
        
        if name:
            name = self.normalize_text(name).lower()
            filtros += "AND lower(i.name) like {0}\n".format(f"'%{name}%'")
            # query_data.append(f"'%{name}%'")
        
        if model:
            model = self.normalize_text(model).lower()
            filtros += "AND lower(i.model) like {0}\n".format(f"'%{model}%'")
            # query_data.append(f"%{model}%")
        
        if fi:
            # fi dd/mm/yyyy
            # i.date date field
            filtros += "AND cast(i.fecha as date) >= {0}\n".format(f"'{fi}'")
            # query_data.append(fi)
        if ff:
            filtros += "AND cast(i.fecha as date) <= {0}\n".format(f"'{ff}'")
            # query_data.append(ff)
        
        if scale:
            scale = self.normalize_text(scale).lower()
            filtros += "AND lower(i.scale) = '{0}'\n".format(scale)
            # query_data.append(scale)
        
        if group_image:
            group_image = self.normalize_text(group_image).lower()
            filtros += "AND lower(i.group_image) = '{0}'\n".format(group_image)
            # query_data.append(group_image)
        
        if categorias:
            categorias = self.normalize_text(categorias).lower()
            categorias = categorias.replace(", ", ",").split(",")
            cat_join = "', '".join(categorias)
            filtros += f"AND lower(c.nombre) in ('{cat_join}')\n"
        
        if general_group:
            general_group = self.normalize_text(general_group).lower()
            filtros += "AND lower(i.general_group) = '{0}'\n".format(general_group)
            # query_data.append(general_group)
        
        query = """select t.*
                    from (SELECT i.id_image, i.name, i.url, 
                            (select min(fecha) 
                                from images
                                where general_group = i.general_group
                            ) fecha_carga, 
                            i.model, i.scale, i.group_image, i.general_group, c.nombre as categoria,
                            c.bg, c.color
                    FROM images i
                    JOIN image_categoria ic
                    ON i.id_image = ic.image_id
                    JOIN categorias c
                    ON ic.categoria_id = c.id_categoria
                    {0}) t
                    order by cast(t.fecha_carga as date) desc, t.general_group, t.group_image, t.name
                    """.format(filtros)

        r = self.conexion.consulta_asociativa(query, query_data)
        
        images = {}
        for i in r:
            image_id = i["id_image"]
            if image_id not in images:
                images[image_id] = {
                    "id_image": i["id_image"],
                    "name": i["name"],
                    "url": i["url"],
                    "fecha_carga": i["fecha_carga"],
                    "model": i["model"],
                    "scale": i["scale"],
                    "group_image": i["group_image"],
                    "general_group": i["general_group"],
                    "categorias": []
                }
            cat = {
                "nombre": i["categoria"],
                "bg": i["bg"],
                "color": i["color"]
            }
            images[image_id]["categorias"].append(cat)
        
        images = [i for i in images.values()]
        
        grupos = {}
        for i in images:
            if i["group_image"] not in grupos:
                grupos[i["group_image"]] = []
            grupos[i["group_image"]].append(i)
        
        self.response = {
            # "images": images,
            "grupos": grupos
        }


class GetCategorias(GetApi):
    def main(self):
        self.show_me()
        
        self.create_conexion()
        nombre = get_d(self.data, "nombre", default=None)
        
        filtro = "WHERE 1=1\n"
        query_data = []
        if nombre:
            nombre = self.normalize_text(nombre).lower()
            filtro += "AND lower(nombre) like {0}\n".format(f"'%{nombre}%'")
            # query_data.append(f"%{nombre}%",)
        
        query = """SELECT id_categoria, nombre, bg, color
                    FROM categorias
                    {0}
                    order by nombre
                    """.format(filtro)

        # print(filtro)
        # print(query)
        r = self.conexion.consulta_asociativa(query, query_data)
        
        self.response = r


class CreateImageUpscale(PostApi):
    def main(self):
        self.show_me()

        path_save = f"{MEDIA_DIR}/img/img2img"
        sd = SDA()

        # base, name, ext, scale


