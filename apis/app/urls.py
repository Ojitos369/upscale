from django.urls import path

from .api import UpdateData

app_name = "app"
urlpatterns = [
    path("update_data/", UpdateData.as_view(), name=f"{app_name}_update_data"),
]