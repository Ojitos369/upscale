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
            "lan": "Lanczos",
            "near": "Nearest",
            "4crv1": "4x-ClearRealityV1",
            "4crv1s": "4x-ClearRealityV1_Soft",
            "4ry": "4x-Rybu",
            "4us": "4x-UltraSharp",
            "fr": "4x_foolhardy_Remacri",
            "4rrg": "4x_RealisticRescaler_100000_G",
            "4vv1": "4x_Valar_v1",
            "4fu": "4xFaceUPDAT",
            "4n8hl": "4xNomos8kHAT-L_otf",
            "4ffd": "4xFrankendata_FullDegradation_g_460000",
            "4n8sc": "4xNomos8kSC",
            # "4ld": "4XLSDIRDAT",
            "4lpn": "4xLSDIRplusN",
            "4nurm": "4xNomosUni_rgt_multijpg",
            "4nud": "4xNomosUniDAT otf",
            "pp": "4xPurePhoto-span",
            "d2": "DAT x2",
            "d3": "DAT x3",
            "d4": "DAT x4",
            "dd2": "DAT_x2",
            "dd3": "DAT_x3",
            "dd4": "DAT_x4",
            "df2k": "DF2K",
            "e4": "ESRGAN 4x",
            "lds": "LDSR",
            "re4p": "R-ESRGAN 4x+",
            "re4a": "R-ESRGAN 4x+ Anime6B",
            "scu": "ScUNET",
            "snp": "ScUNET PSNR",
            "sw4": "SwinIR_4x",
        }
        
        models = {
            "scu": "ScUNET",
            "4fu": "4xFaceUPDAT",
            "snp": "ScuNet PSNR",
            # "d4": "DAT x4",
            # "pp": "4xPurePhoto-span",
            # "4ld": "4XLSDIRDAT",
            # "fr": "4x_foolhardy_Remacri",
            # "pp": "4xPurePhoto-span",
            # "d4": "DAT x4",
            # "re4p": "R-ESRGAN 4x+",
        }
        
        base_q = get_d(self.data, "bs", default=None)
        model_q = get_d(self.data, "mdl", default=None)
        

        bases = [
            {"name": "sn_bb", "cantidad": 40, "cats": ["Sana", "Twice"]},
            {"name": "mn_fd", "cantidad": 11, "cats": ["Mina", "Twice"]},
            {"name": "mm_ig_1", "cantidad": 10, "cats": ["Momo", "Twice"]},
            {"name": "mm_ig_2", "cantidad": 7, "cats": ["Momo", "Twice"]},
            {"name": "mm_igh_1", "cantidad": 2, "cats": ["Momo", "Twice"]},
            {"name": "cy_1", "cantidad": 1, "cats": ["Chaeyoung", "Twice"]},
            {"name": "mn_tbtied", "cantidad": 6, "cats": ["Mina", "Twice"]},
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
            {"name": "cy_ig_2", "cantidad": 1, "cats": ["Chaeyoung", "Twice"]},
            {"name": "sn_el", "cantidad": 3, "cats": ["Sana", "Twice"]},
            {"name": "ch_ig_300424_1", "cantidad": 5, "cats": ["Chaeyoung", "Twice"]},
            {"name": "tw_dv_1", "cantidad": 1, "cats": ["Twice", "Nayeon", "Jeongyeon", "Momo", "Sana", "Jihyo", "Mina", "Dahyun", "Chaeyoung", "Tzuyu", "Dive"]},
            {"name": "dy_ex", "cantidad": 1, "cats": ["Dahyun", "Twice"]},
            {"name": "cy_ig_010524", "cantidad": 1, "cats": ["Chaeyoung", "Twice"]},
            {"name": "cy_bl_1", "cantidad": 4, "cats": ["Chaeyoung", "Twice", "Bubble"]},
            {"name": "mn_ex_1", "cantidad": 2, "cats": ["Mina", "Twice"]},
            {"name": "sn_ttt_1", "cantidad": 3, "cats": ["Sana", "Twice", "Talk that Talk", "Between 1&2"]},
            {"name": "tw_pc_1", "cantidad": 9, "cats_obj": {
                1: ["Nayeon", "Twice", "Photo Card"],
                2: ["Jeongyeon", "Twice", "Photo Card"],
                3: ["Momo", "Twice", "Photo Card"],
                4: ["Sana", "Twice", "Photo Card"],
                5: ["Jihyo", "Twice", "Photo Card"],
                6: ["Mina", "Twice", "Photo Card"],
                7: ["Dahyun", "Twice", "Photo Card"],
                8: ["Chaeyoung", "Twice", "Photo Card"],
                9: ["Tzuyu", "Twice", "Photo Card"],
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
            if base_q and base_q != general_group:
                continue

            if general_group in ggs:
                print(f"Ya existe el grupo {general_group}")
                repetidos.append(general_group)
                continue

            for i in range(1, b["cantidad"] + 1):
                group = name = f"{b['name']}_{i}"
                link = f"https://storage.googleapis.com/ojitos369_ups/{name}.jpg"
                item = {"name": name, "link": link, "model": "Original", "scale": 1, "group": group, "general_group": general_group}
                
                if "cats" in b:
                    item["categorias"] = [*b["cats"]]
                elif "cats_obj" in b:
                    item["categorias"] = b["cats_obj"][i]
                else:
                    item["categorias"] = []
                items.append(item)

                for k, v in models.items():
                    
                    if model_q and model_q != k:
                        continue
                    
                    name = f"{b['name']}_{i}_{k}_2x"
                    link = f"https://storage.googleapis.com/ojitos369_ups/{name}.png"
                    item = {"name": name, "link": link, "model": v, "scale": 4, "group": group, "general_group": general_group}
                    
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
            if group: group = group.lower()
            general_group = get_d(i, "general_group", default=None)
            if general_group: general_group = general_group.lower()

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
                        (image_id, categoria_id, group_image)
                        values
                        (%s, %s, %s) """
                qd = (image_id, id_categoria, group)
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


class UpdateCustomData(PostApi, GetApi):
    def main(self):
        self.show_me()
        
        self.create_conexion()

        items = []
        
        models = {
            "lan": "Lanczos",
            "near": "Nearest",
            "4crv1": "4x-ClearRealityV1",
            "4crv1s": "4x-ClearRealityV1_Soft",
            "4ry": "4x-Rybu",
            "4us": "4x-UltraSharp",
            "fr": "4x_foolhardy_Remacri",
            "4rrg": "4x_RealisticRescaler_100000_G",
            "4vv1": "4x_Valar_v1",
            "4fu": "4xFaceUPDAT",
            "4n8hl": "4xNomos8kHAT-L_otf",
            "4ffd": "4xFrankendata_FullDegradation_g_460000",
            "4n8sc": "4xNomos8kSC",
            "4ld": "4XLSDIRDAT",
            "4lpn": "4xLSDIRplusN",
            "4nurm": "4xNomosUni_rgt_multijpg",
            "4nud": "4xNomosUniDAT otf",
            "pp": "4xPurePhoto-span",
            "d2": "DAT x2",
            "d3": "DAT x3",
            "d4": "DAT x4",
            "dd2": "DAT_x2",
            "dd3": "DAT_x3",
            "dd4": "DAT_x4",
            "df2k": "DF2K",
            "e4": "ESRGAN 4x",
            "lds": "LDSR",
            "re4p": "R-ESRGAN 4x+",
            "re4a": "R-ESRGAN 4x+ Anime6B",
            "scu": "ScUNET",
            "snp": "ScUNET PSNR",
            "sw4": "SwinIR_4x",
        }

        models = {
            # "fr": "4x_foolhardy_Remacri",
            # "pp": "4xPurePhoto-span",
            # "d4": "DAT x4",
            # "re4p": "R-ESRGAN 4x+",
            # "d4": "DAT x4",
            # "pp": "4xPurePhoto-span",
            # "4ld": "4XLSDIRDAT",
            "4fu": "4xFaceUPDAT",
            "scu": "ScUNET",
            "snp": "ScuNet PSNR",
        }

        # ?bs=tw_dvi_1&ctdi=1&ctdf=1&cats=Nayeon,Twice,Dive
        # ?bs=tw_dvi_1&ctdi=2&ctdf=2&cats=Jeongyeon,Twice,Dive
        # ?bs=tw_dvi_1&ctdi=3&ctdf=3&cats=Momo,Twice,Dive
        # ?bs=tw_dvi_1&ctdi=4&ctdf=4&cats=Sana,Twice,Dive
        # ?bs=tw_dvi_1&ctdi=5&ctdf=5&cats=Jihyo,Twice,Dive
        # ?bs=tw_dvi_1&ctdi=6&ctdf=6&cats=Mina,Twice,Dive
        # ?bs=tw_dvi_1&ctdi=7&ctdf=7&cats=Dahyun,Twice,Dive
        # ?bs=tw_dvi_1&ctdi=8&ctdf=8&cats=Chaeyoung,Twice,Dive
        # ?bs=tw_dvi_1&ctdi=9&ctdf=9&cats=Tzuyu,Twice,Dive
        
        # ?bs=jh_fd_1&ctd=7&cats=Jihyo,Twice,Fred
        # ?bs=jh_fd_1&ctd=7&cats=Jihyo,Twice,Fred

        general_group = base = get_d(self.data, "bs")
        models_q = get_d(self.data, "mdl", default=None)
        cantidad = int(get_d(self.data, "ctd", default=1))
        cantidad_inicial = int(get_d(self.data, "ctdi", default=0))
        cantidad_final = int(get_d(self.data, "ctdf", default=0))
        cats = get_d(self.data, "cats", default=[])

        if cats and type(cats) == str:
            cats = cats.replace(", ", ",").replace("{and}", "&").split(",")
        if models_q and type(models_q) == str:
            models_q = models_q.replace(", ", ",").replace("{and}", "&").split(",")
        
        if not models_q:
            models_q = models.keys()

        query_gg = """SELECT distinct name, model
                    FROM images
                    where general_group = '{0}'
                    """.format(base.lower())

        r = self.conexion.consulta_asociativa(query_gg)
        rs = [i["name"]+i["model"] for i in r]

        agregados = []
        repetidos = []
        my_range = range(1, cantidad + 1)

        if cantidad_inicial and cantidad_final:
            my_range = range(cantidad_inicial, cantidad_final + 1)
        elif cantidad_inicial and cantidad_inicial < cantidad:
            my_range = range(cantidad_inicial, cantidad + 1)

        for i in my_range:
            group = name = f"{base}_{i}"
            
            link = f"https://storage.googleapis.com/ojitos369_ups/{name}.jpg"
            item = {"name": name, "link": link, "model": "Original", "scale": 1, "group": group, "general_group": general_group}
            item["categorias"] = cats

            if f"{name}Original" not in rs:
                items.append(item)
                agregados.append(name)

            for m in models_q:
                try:
                    v = models[m]
                except:
                    continue

                name = f"{base}_{i}_{m}_4x"
                if f"{name}{v}" in rs:
                    repetidos.append(name)
                    continue
            
                link = f"https://storage.googleapis.com/ojitos369_ups/{name}.png"
                item = {"name": name, "link": link, "model": v, "scale": 4, "group": group, "general_group": general_group}
                item["categorias"] = cats

                items.append(item)
                agregados.append(name)
        

        query = """INSERT INTO images 
                    (name, url, model, fecha, scale, group_image, general_group)
                    values
                    (%s, %s, %s, now(), %s, %s, %s)
                """
        # self.response = {
        #     "items": items
        # }

        # return 
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
                        (image_id, categoria_id, group_image)
                        values
                        (%s, %s, %s) """
                qd = (image_id, id_categoria, group)
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

        filtro_categorias = ''
        filtros_pre_paginacion = ""

        if name:
            name = self.normalize_text(name).lower()
            filtros_pre_paginacion += "AND lower(i.name) like {0}\n".format(f"'%{name}%'")
        
        if model:
            model = self.normalize_text(model).lower()
            filtros_pre_paginacion += "AND lower(i.group_image) in (select distinct group_image from images where lower(modelo) like {0})\n".format(f"'%{model}%'")
        
        if fi:
            # fi dd/mm/yyyy
            # i.date date field
            filtros_pre_paginacion += "AND cast(i.fecha as date) >= {0}\n".format(f"'{fi}'")
        if ff:
            filtros_pre_paginacion += "AND cast(i.fecha as date) <= {0}\n".format(f"'{ff}'")
        
        if scale:
            scale = self.normalize_text(scale).lower()
            if not scale.endswith("x"):
                scale += "x"
            filtros_pre_paginacion += "AND lower(i.scale) = '{0}'\n".format(scale)
        
        if group_image:
            group_image = self.normalize_text(group_image).lower()
            filtros_pre_paginacion += "AND lower(i.group_image) = '{0}'\n".format(group_image)
        
        if categorias:
            categorias = self.normalize_text(categorias).lower()
            categorias = categorias.replace(", ", ",").split(",")
            cat_join = "', '".join(categorias)
            filtro_categorias += f"""WHERE lower(c.nombre) in ('{cat_join}') """

        if general_group:
            general_group = self.normalize_text(general_group).lower()
            filtros_pre_paginacion += "AND lower(i.general_group) = '{0}'\n".format(general_group)
            
        qc = """select distinct t.group_image
                from (SELECT i.id_image, i.name, i.url,
                            (select min(fecha)
                            from images
                            where general_group = i.general_group) fecha_carga,
                            i.model, i.scale, i.group_image, i.general_group
                    FROM images i
                    WHERE i.model = 'Original'
                    {1}
                    ) t
                inner join image_categoria ic on t.group_image = ic.group_image
                inner join categorias c on ic.categoria_id = c.id_categoria
                {0}
                group by t.group_image
                    """.format(filtro_categorias, filtros_pre_paginacion)
        
        qt = """select count(*) cantidad from (select distinct t.group_image
                from (SELECT i.id_image, i.name, i.url,
                            (select min(fecha)
                            from images
                            where general_group = i.general_group) fecha_carga,
                            i.model, i.scale, i.group_image, i.general_group
                    FROM images i
                    WHERE i.model = 'Original' ) t
                inner join image_categoria ic on t.group_image = ic.group_image
                inner join categorias c on ic.categoria_id = c.id_categoria
                group by t.group_image) dt"""

        rc = self.conexion.consulta_asociativa(qc)
        rct = self.conexion.consulta_asociativa(qt)
        cantidad = len(rc)
        cantidad_total = rct[0]["cantidad"]
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
            if not pagina:
                pagina = 1
            offset = (pagina - 1) * por_pagina # 0
            filtros_paginacion += f"LIMIT {por_pagina} OFFSET {offset}\n"
        
        filtros = ""
        if filtro_categorias:
            filtros = "AND lower(i.group_image) in ({0})\n".format(qc)

        query = """select dt.* from (select t.*
                    from (SELECT i.id_image, i.name, i.url,
                        (select min(fecha)
                            from images
                            where general_group = i.general_group) fecha_carga,
                        i.model, i.scale, i.group_image, i.general_group
                    FROM images i
                    WHERE i.model = 'Original'
                    {2}
                    {0} ) t
                    order by t.fecha_carga desc, t.general_group, t.group_image, t.name ) dt
                    order by dt.fecha_carga desc, dt.general_group, dt.group_image, dt.name
                    {1}
                    """.format(filtros, filtros_paginacion, filtros_pre_paginacion)

        # print(query)
        r = self.conexion.consulta_asociativa(query)
        
        qc = """select distinct t.group_image, c.*
                from (SELECT distinct i.group_image group_image
                        FROM images i
                        WHERE i.model = 'Original'
                        {0}
                        ) t
                inner join image_categoria ic on t.group_image = ic.group_image
                inner join categorias c on ic.categoria_id = c.id_categoria
                group by t.group_image, c.nombre""".format(filtros)
        cats = self.conexion.consulta_asociativa(qc)

        images = {}
        for i in r:
            image_id = i["id_image"]
            if image_id not in images:
                data_img = {
                    "id_image": i["id_image"],
                    "name": i["name"],
                    "url": i["url"],
                    "fecha_carga": i["fecha_carga"],
                    "model": i["model"],
                    "scale": i["scale"],
                    "group_image": i["group_image"],
                    "general_group": i["general_group"],
                }
                cats_img = []
                for c in cats:
                    if c["group_image"] != i["group_image"]:
                        continue

                    cat = {
                        "nombre": c["nombre"],
                        "bg": c["bg"],
                        "color": c["color"]
                    }
                    cats_img.append(cat)
                data_img["categorias"] = cats_img
                images[image_id] = data_img
        
        images = [i for i in images.values()]
        
        grupos = {}
        for i in images:
            if i["group_image"] not in grupos:
                grupos[i["group_image"]] = []
            grupos[i["group_image"]].append(i)
            
        # print(grupos)
        
        self.response = {
            # "images": images,
            "cantidad": cantidad,
            "pagina": pagina,
            "por_pagina": por_pagina,
            "paginas": paginas,
            "grupos": grupos
        }


class GetImageGroup(GetApi):
    def main(self):
        self.show_me()
        self.create_conexion()

        group_image = get_d(self.data, "gi", default=None)

        query = """SELECt * from images
                    where lower(group_image) = {0}
                    """.format(f"'{group_image.lower()}'")

        query
        r = self.conexion.consulta_asociativa(query)
        self.response = {"info": r}


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
            
            url_base = f"https://storage.googleapis.com/ojitos369_ups/"
            
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
                            (image_id, categoria_id, group_image)
                            values
                            ('{0}', '{1}', '{2}') """
                    qd = (image_id, id_categoria, group_image)
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

SET GLOBAL time_zone = 'America/Mexico_City';

tw_opf

"""