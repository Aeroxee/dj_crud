from django.urls import path
from .views import (
    login_user,
    logout_user,
    register_user,
    home,
    tambah_data,
    edit_data,
    hapus_data,
)

app_name = "data"
urlpatterns = [
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    
    path("", home, name="home"),
    path("tambah/", tambah_data, name="tambah_data"),
    path("edit/<int:pk>/", edit_data, name="edit_data"),
    path("hapus/<int:pk>/", hapus_data, name="hapus_data"),
]