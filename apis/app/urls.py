from django.urls import path

from .api import (
    UpdateInitData, UpdateCustomData, GetImages, GetCategorias, CreateImageUpscale
)

app_name = "app"
urlpatterns = [
    path("update_init_data/", UpdateInitData.as_view(), name=f"{app_name}_update_init_data"),
    path("update_custom_data/", UpdateCustomData.as_view(), name=f"{app_name}_update_custom_data"),
    path("get_images/", GetImages.as_view(), name=f"{app_name}_get_images"),
    path("get_categorias/", GetCategorias.as_view(), name=f"{app_name}_get_categorias"),
    path("create_image_upscale/", CreateImageUpscale.as_view(), name=f"{app_name}_create_image_upscale"),
]