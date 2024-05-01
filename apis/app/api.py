# Python
import os
import json

# Ojitos369
from ojitos369.utils import get_d

from app.core.sd import StableDiffApi as SDA

# User
from app.core.bases.apis import PostApi, GetApi, pln
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
            {"name": "mm_igh_1", "cantidad": 2, "cats": ["Momo", "Twice"]},
            {"name": "mn_tbtied", "cantidad": 6, "cats": ["Mina", "Twice"]},
            {"name": "ch_ig_300424_1", "cantidad": 5, "cats": ["Chaeyoung", "Twice"]},
            {"name": "sn_el", "cantidad": 3, "cats": ["Sana", "Twice"]},
            {"name": "tw_dv_1", "cantidad": 1, "cats": ["Twice", "Nayeon", "Jeongyeon", "Momo", "Sana", "Jihyo", "Mina", "Dahyun", "Chaeyoung", "Tzuyu", "Dive"]},
            {"name": "tw_opf", "cantidad": 9, "cats_obj": {
                1: ["Nayeon", "Twice"],
                2: ["Jeongyeon", "Twice"],
                3: ["Momo", "Twice"],
                4: ["Sana", "Twice"],
                5: ["Jihyo", "Twice"],
                6: ["Mina", "Twice"],
                7: ["Dahyun", "Twice"],
                8: ["Chaeyoung", "Twice"],
                9: ["Tzuyu", "Twice"],
            }},
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
                
                if "cats" in b:
                    item["categorias"] = [*b["cats"]]
                elif "cats_obj" in b:
                    item["categorias"] = b["cats_obj"][i]
                else:
                    item["categorias"] = []
                items.append(item)

                for k, v in models.items():
                    name = f"{b['name']}_{i}_{k}_2x"
                    link = f"https://ojitos369.com/media/twice/ups/{name}.png"
                    item = {"name": name, "link": link, "model": v, "scale": 2, "group": group, "general_group": general_group}
                    
                    if "cats" in b:
                        item["categorias"] = [*b["cats"]]
                    elif "cats_obj" in b:
                        item["categorias"] = b["cats_obj"][i]
                    else:
                        item["categorias"] = []

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

        pagina = get_d(self.data, "pagina", default=1)
        por_pagina = get_d(self.data, "por_pagina", default=25)

        filtros = "WHERE 1=1\n"
        filtros_pre_paginacion = "WHERE 1=1\n"
        
        if name:
            name = self.normalize_text(name).lower()
            filtros += "AND lower(i.name) like {0}\n".format(f"'%{name}%'")
            filtros_pre_paginacion += "AND lower(i.name) like {0}\n".format(f"'%{name}%'")
        
        if model:
            model = self.normalize_text(model).lower()
            filtros += "AND lower(i.model) like {0}\n".format(f"'%{model}%'")
        
        if fi:
            # fi dd/mm/yyyy
            # i.date date field
            filtros += "AND cast(i.fecha as date) >= {0}\n".format(f"'{fi}'")
        if ff:
            filtros += "AND cast(i.fecha as date) <= {0}\n".format(f"'{ff}'")
        
        if scale:
            scale = self.normalize_text(scale).lower()
            filtros += "AND lower(i.scale) = '{0}'\n".format(scale)
        
        if group_image:
            group_image = self.normalize_text(group_image).lower()
            filtros += "AND lower(i.group_image) = '{0}'\n".format(group_image)
        
        if categorias:
            categorias = self.normalize_text(categorias).lower()
            categorias = categorias.replace(", ", ",").split(",")
            cat_join = "', '".join(categorias)
            filtros += f"""AND i.group_image in (select distinct group_image
                        FROM images i
                        JOIN image_categoria ic
                        ON i.id_image = ic.image_id
                        JOIN categorias c
                        ON ic.categoria_id = c.id_categoria
                        where lower(c.nombre) in ('{cat_join}'))\n """

        if general_group:
            general_group = self.normalize_text(general_group).lower()
            filtros += "AND lower(i.general_group) = '{0}'\n".format(general_group)
            
        qc = """select distinct t.group_image
                    from (SELECT i.id_image, i.name, i.url,
                                (select min(fecha)
                                from images
                                where general_group = i.general_group) fecha_carga,
                            i.model, i.scale, i.group_image, i.general_group, c.nombre as categoria,
                            c.bg, c.color
                        FROM images i
                            JOIN image_categoria ic
                                ON i.id_image = ic.image_id
                            JOIN categorias c
                                ON ic.categoria_id = c.id_categoria
                            {0}
                        ) t
                    order by t.fecha_carga desc, t.general_group, t.group_image, t.name, t.categoria
                    """.format(filtros)
        
        rc = self.conexion.consulta_asociativa(qc)
        cantidad = len(rc)
        pagina = pagina
        por_pagina = int(por_pagina)
        pagina = int(pagina)
        if por_pagina:
            paginas = ((cantidad // por_pagina) + 1) if (cantidad % por_pagina) else (cantidad // por_pagina)
        else:
            paginas = pagina
        
        if pagina > paginas:
            pagina = paginas

        filtros_paginacion = ""
        if por_pagina:
            offset = (pagina - 1) * por_pagina # 0
            filtros_paginacion += f"LIMIT {por_pagina} OFFSET {offset}\n"
            
        
        
        query = """select t.*
                    from (SELECT i.id_image, i.name, i.url,
                                (select min(fecha)
                                from images
                                where general_group = i.general_group) fecha_carga,
                            i.model, i.scale, i.group_image, i.general_group, c.nombre as categoria,
                            c.bg, c.color
                        FROM images i
                            JOIN image_categoria ic
                                ON i.id_image = ic.image_id
                            JOIN categorias c
                                ON ic.categoria_id = c.id_categoria
                            Join (select distinct t1.group_image
                                    from (select pt.*
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
                                        {0}) pt
                                        order by pt.fecha_carga desc, pt.general_group, pt.group_image, pt.name, pt.categoria) t1
                                        order by t1.fecha_carga desc, t1.general_group, t1.group_image, t1.name, t1.categoria
                                        {1}
                                        ) lim
                                ON i.group_image = lim.group_image
                            {0}
                        ) t
                    order by t.fecha_carga desc, t.general_group, t.group_image, t.name, t.categoria
                    """.format(filtros, filtros_paginacion)

        # print(query)
        r = self.conexion.consulta_asociativa(query)
        
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
            "cantidad": cantidad,
            "pagina": pagina,
            "por_pagina": por_pagina,
            "paginas": paginas,
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
        self.create_conexion()
        
        # pln(self.data)
        base_name = self.data["base_name"]
        
        query = """SELECT count(*) cantidad
                    FROM images
                    WHERE general_group = %s 
                    AND model = 'Original'
                    """
        query_data = (base_name,)
        r = self.conexion.consulta_asociativa(query, query_data)
        c = r[0]["cantidad"] + 1
        
        scale = int(get_d(self.data, "scale", default="2"))
        cats = get_d(self.data, "cats", default="")
        cats = cats.replace(", ", ",").split(",")
        file = self.data["file"] # InMemoryUploadedFile
        name = file.name
        file = file.file
        ext = name.split(".")[-1]
        name = ".".join(name.split(".")[:-1])
        
        base_name_custom = f"{base_name}_{c}"

        path_save_path = path_save = f"{MEDIA_DIR}/img/img2img"
        # save file in path_save
        new_name = f"{base_name_custom}.{ext}"
        save_path = os.path.join(path_save, new_name)
        with open(save_path, "wb") as f:
            f.write(file.read())
        
        convert_files = []
        if ext == 'zip':
            valid_ext = ['jpg', 'png', 'jpeg']
            # descomprimir
            import zipfile
            with zipfile.ZipFile(save_path, 'r') as zip_ref:
                zip_ref.extractall(path_save)
            os.remove(save_path)
            files = os.listdir(path_save)
            for f in files:
                ext = f.split(".")[-1]
                if ext in valid_ext:
                    base_name_custom = f"{base_name}_{c}"
                    new_name = f"{base_name_custom}.{ext}"
                    os.rename(f"{path_save}/{f}", f"{path_save}/{new_name}")
                    convert_files.append({
                        "base": base_name_custom,
                        "name": base_name_custom,
                        "ext": ext
                    })
                    
                    c += 1
        else:
            convert_files = [{
                "base": base_name_custom,
                "name": base_name_custom,
                "ext": ext
            }]

        or_scale = scale
        # base, name, ext, scale
        self.create_conexion()
        for cf in convert_files:
            sd = SDA(ce=self.ce)
            base_name_custom = cf["base"]
            ext = cf["ext"]
            sd.run(base=base_name_custom, name=base_name_custom, ext=ext, scale=or_scale, cats=cats)
            files = sd.images_procesadas
            # sd.images_procesadas = files = [{'path': '/home/ojitos369/Documents/progra/ojitos369/upscale/media/img/img2img/jy_ex_1_1_fr_2x.png', 'model': '4x_foolhardy_Remacri', 'scale': '2x'}, {'path': '/home/ojitos369/Documents/progra/ojitos369/upscale/media/img/img2img/jy_ex_1_1_snp_2x.png', 'model': 'ScuNET PSNR', 'scale': '2x'}, {'path': '/home/ojitos369/Documents/progra/ojitos369/upscale/media/img/img2img/jy_ex_1_1_pp_2x.png', 'model': '4xPurePhoto-span', 'scale': '2x'}, {'path': '/home/ojitos369/Documents/progra/ojitos369/upscale/media/img/img2img/jy_ex_1_1_d4_2x.png', 'model': 'DAT x4', 'scale': '2x'}, {'path': '/home/ojitos369/Documents/progra/ojitos369/upscale/media/img/img2img/jy_ex_1_1.jpg', 'model': 'Original', 'scale': '1x'}]
            # print(files)
            sd.move_to_ftp()
            
            # now_db = "now() - interval 6 hour"
            query = """INSERT INTO images
                        (name, url, model, fecha, scale, group_image, general_group)
                        values
                        ('{0}', '{1}', '{2}', now(), '{3}', '{4}', '{5}')
                    """
            
            url_base = f"https://ojitos369.com/media/twice/ups/"
            
            qc = """SELECT id_categoria
                        FROM categorias
                        WHERE upper(nombre) = '{0}' """

            for file in files:
                path = file["path"]
                name = path.split("/")[-1]

                url = f"{url_base}{name}"
                model = file["model"]
                scale = file["scale"]
                name = ".".join(name.split(".")[:-1])
                group_image = name
                general_group = base_name
                
                qd = (name, url, model, scale, base_name_custom, general_group)

                qrt = query.format(*qd)
                
                # pln(qrt)
                if not self.conexion.ejecutar(qrt):
                    self.conexion.rollback()
                    raise self.MYE("Error al guardar la imagen")
                self.conexion.commit()
                
                qt = """SELECT id_image
                        FROM images
                        WHERE name = %s
                        and url = %s
                        """
                qdt = (name, url)
                r = self.conexion.consulta_asociativa(qt, qdt)
                image_id = r[0]["id_image"]
                
                temp_cats = [*cats]
                if model not in temp_cats:
                    temp_cats.append(model)
                if scale not in temp_cats:
                    temp_cats.append(scale)
                
                for cat in temp_cats:
                    name = cat.upper()
                    qrtc = qc.format(name)
                    r = self.conexion.consulta_asociativa(qrtc)
                    
                    if not r:
                        bg = self.get_random_color()
                        color = self.get_text_color(bg)
                        
                        qt = """insert into categorias
                                (nombre, bg, color)
                                values
                                ('{0}', '{1}', '{2}') """
                        qd = (name, bg, color)
                        qrt = qt.format(*qd)
                        if not self.conexion.ejecutar(qrt):
                            self.conexion.rollback()
                            raise self.MYE("Error al guardar la categoria")
                        self.conexion.commit()
                        r = self.conexion.consulta_asociativa(qrtc)
                    id_categoria = r[0]["id_categoria"]
                    
                    
                    qt = """insert into image_categoria
                            (image_id, categoria_id)
                            values
                            ('{0}', '{1}') """
                    qd = (image_id, id_categoria)
                    qrt = qt.format(*qd)
                    if not self.conexion.ejecutar(qrt):
                        self.conexion.rollback()
                        raise self.MYE("Error al guardar la categoria")
                    self.conexion.commit()
        
        self.response = {
            "message": "Imagenes guardadas correctamente",
        }



""" 


id_categoria	
nombre	
bg	
color	
icon	
	
TWICE, #fc5d9d, #000000, NULL
NAYEON, #49c0ec, #000000, NULL
JEONGYEON, #a3cc54, #000000, NULL
MOMO, #e67ea3, #000000, NULL
SANA, #8c79b4, #000000, NULL
JIHYO, #f9cc85, #000000, NULL
MINA, #71c7d4, #000000, NULL
DAHYUN, #fefefe, #000000, NULL
CHAEYOUNG, #e62722, #000000, NULL
TZUYU, #2253a3, #ffffff, NUL

insert into categorias (nombre, bg, color) values ('TWICE', '#fc5d9d', '#000000');
insert into categorias (nombre, bg, color) values ('NAYEON', '#49c0ec', '#000000');
insert into categorias (nombre, bg, color) values ('JEONGYEON', '#a3cc54', '#000000');
insert into categorias (nombre, bg, color) values ('MOMO', '#e67ea3', '#000000');
insert into categorias (nombre, bg, color) values ('SANA', '#8c79b4', '#000000');
insert into categorias (nombre, bg, color) values ('JIHYO', '#f9cc85', '#000000');
insert into categorias (nombre, bg, color) values ('MINA', '#71c7d4', '#000000');
insert into categorias (nombre, bg, color) values ('DAHYUN', '#fefefe', '#000000');
insert into categorias (nombre, bg, color) values ('CHAEYOUNG', '#e62722', '#000000');
insert into categorias (nombre, bg, color) values ('TZUYU', '#2253a3', '#ffffff');

update categorias set bg = '#fc5d9d', color = '#000000' where nombre = 'TWICE';
update categorias set bg = '#49c0ec', color = '#000000' where nombre = 'NAYEON';
update categorias set bg = '#a3cc54', color = '#000000' where nombre = 'JEONGYEON';
update categorias set bg = '#e67ea3', color = '#000000' where nombre = 'MOMO';
update categorias set bg = '#8c79b4', color = '#000000' where nombre = 'SANA';
update categorias set bg = '#f9cc85', color = '#000000' where nombre = 'JIHYO';
update categorias set bg = '#71c7d4', color = '#000000' where nombre = 'MINA';
update categorias set bg = '#fefefe', color = '#000000' where nombre = 'DAHYUN';
update categorias set bg = '#e62722', color = '#000000' where nombre = 'CHAEYOUNG';
update categorias set bg = '#2253a3', color = '#ffffff' where nombre = 'TZUYU';


tw_opf
"""