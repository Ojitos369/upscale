from django.urls import path

from .api import Login, ValidateLogin, CloseSession

app_name = "user"
urlpatterns = [
    path("login/", Login.as_view(), name=f"{app_name}_login"),
    path("validate_login/", ValidateLogin.as_view(), name=f"{app_name}_validate_login"),
    path("close_session/", CloseSession.as_view(), name=f"{app_name}_close_session"),
]