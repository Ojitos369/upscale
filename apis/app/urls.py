from django.urls import path

from .api import (
    UpdateInitData, GetImages, GetCategorias, CreateImageUpscale
)

app_name = "app"
urlpatterns = [
    path("update_init_data/", UpdateInitData.as_view(), name=f"{app_name}_update_init_data"),
    path("get_images/", GetImages.as_view(), name=f"{app_name}_get_images"),
    path("get_categorias/", GetCategorias.as_view(), name=f"{app_name}_get_categorias"),
    path("create_image_upscale/", CreateImageUpscale.as_view(), name=f"{app_name}_create_image_upscale"),
]