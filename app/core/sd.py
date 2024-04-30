from datetime import datetime
import urllib.request
import base64
import json
import time
import os
from ftplib import FTP
from ojitos369.utils import get_d
from app.settings import MEDIA_DIR, FTP_DATA


class StableDiffApi:
    def __init__(self):
        # self.webui_server_url = "https://stablediff.aztlanlabs.net"
        self.webui_server_url = "https://lpfzrgtb-7860.usw3.devtunnels.ms"
        self.imgs_path = f"{MEDIA_DIR}/img/img2img"
        self.images_procesadas = []
        
    def timestamp(self):
        return datetime.fromtimestamp(time.time()).strftime("%Y%m%d-%H%M%S")

    def encode_file_to_base64(self, path):
        with open(path, 'rb') as file:
            return base64.b64encode(file.read()).decode('utf-8')

    def decode_and_save_base64(self, base64_str, save_path):
        with open(save_path, "wb") as file:
            file.write(base64.b64decode(base64_str))

    def call_api(self, api_endpoint, **payload):
        data = json.dumps(payload).encode('utf-8')
        request = urllib.request.Request(
            f'{self.webui_server_url}/{api_endpoint}',
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0",
                "Connection": "keep-alive",
            },
            data=data,
        )
        response = urllib.request.urlopen(request)
        return json.loads(response.read().decode('utf-8'))

    def call_txt2img_api(self, **payload):
        response = self.call_api('sdapi/v1/txt2img', **payload)
        for index, image in enumerate(response.get('images')):
            save_path = os.path.join(self.imgs_path, f'txt2img-{self.timestamp()}-{index}.png')
            self.decode_and_save_base64(image, save_path)

    def call_img2img_api(self, name = None, **payload):
        response = self.call_api('sdapi/v1/img2img', **payload)
        for index, image in enumerate(response.get('images')):
            name = name or f'img2img-{self.timestamp()}-{index}.png'
            path_save = f"{MEDIA_DIR}/img/img2img"
            save_path = os.path.join(path_save, name)
            self.decode_and_save_base64(image, save_path)
            return save_path

    def change_model(self):
        payload = {
            "sd_model_checkpoint": "instruct-pix2pix-00-22000",
            "CLIP_stop_at_last_layers": 2
        }
        endpoint = '/sdapi/v1/options'
        response = self.call_api(endpoint, **payload)
        print(response)

    def reescale(self, base, img_path, name, ext="jpg", scale=2):
        image_base = f"{img_path}/{name}.{ext}"
        init_images = [
            self.encode_file_to_base64(image_base),
        ]
        models = [
            {"model": "4x_foolhardy_Remacri", "clave": "fr"},
            {"model": "ScuNET PSNR", "clave": "snp"},
            {"model": "4xPurePhoto-span", "clave": "pp"},
            {"model": "DAT x4", "clave": "d4"},
        ]

        for m in models:
            model = m["model"]
            base = m["clave"]
            payload = {
                "sd_model_checkpoint": "instruct-pix2pix-00-22000",
                "sd_vae":"",
                "prompt": "",
                "negative_prompt":"",
                "init_images":init_images,
                "sampler_index":"Euler a",
                "steps": 20,
                "denoising_strength": 0.03,
                "script_name": "SD upscale",
                "script_args": [None, 64, model, scale],
                "alwayson_scripts":{
                }
            }
            n = f"{name}_{base}_{scale}x.png"
            print(f"\nUpscaling {n}", end="... ")
            from ojitos369.utils import print_json as pj
            # pj(payload)
            save_path = self.call_img2img_api(name=n ,**payload)
            self.images_procesadas.append({
                "path": save_path,
                "model": model,
                "scale": f"{scale}x"
            })
            print("Done")

        self.images_procesadas.append({
            "path": image_base, 
            "model": "Original",
            "scale": "1x"
        })

        print()
        print(f"-"*40)
    
    def move_to_ftp(self):
        host = FTP_DATA["host"]
        port = FTP_DATA["port"]
        user = FTP_DATA["user"]
        password = FTP_DATA["password"]
        path = "media/twice/ups"
        
        ftp = FTP(host)
        ftp.login(user, password)
        ftp.cwd('domains/ojitos369.com/public_html')
        ftp.cwd(path)

        for i in self.images_procesadas:
            image = i["path"]
            file_name = image.split("/")[-1]
            with open(image, 'rb') as file:
                ftp.storbinary(f"STOR {file_name}", file)
                print(f"Archivo {image} subido a FTP")
            os.remove(image)
            print(f"Archivo {image} eliminado")
        
        ftp.quit()

    def run(self, *args, **kwargs):
        base = kwargs["base"]
        name = kwargs["name"]
        ext = get_d(kwargs, "ext", default="jpg")
        scale = get_d(kwargs, "scale", default=2)

        self.reescale(base, self.imgs_path, name, ext=ext, scale=scale)
        