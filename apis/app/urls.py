from django.urls import path

from .api import (
    UpdateData, GetImages, GetCategorias
)

app_name = "app"
urlpatterns = [
    path("update_data/", UpdateData.as_view(), name=f"{app_name}_update_data"),
    path("get_images/", GetImages.as_view(), name=f"{app_name}_get_images"),
    path("get_categorias/", GetCategorias.as_view(), name=f"{app_name}_get_categorias"),
]