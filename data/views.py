from django.shortcuts import render, redirect, get_list_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse, Http404
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

from django.contrib.auth.models import User
from django.db import IntegrityError

from .models import Data
# Create your views here.

def login_user(request: HttpRequest) -> HttpResponse:
    """Handler untuk login user.
    """
    if request.user.is_authenticated:
        # Jika user terautentikasi maka akan diredirect ke home.
        return redirect("data:home")
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        # Mendapatkan autentikasi user
        user = authenticate(request, username=username, password=password)
        
        # Cek apakah user dengan username dan password adalah benar.
        if user is not None:
            login(request, user) # Menyimpan data user di dalam session.
            return redirect("data:home")
        else:
            messages.error(request, "Username atau katasandi yang anda masukkan salah.")
            return redirect("data:login")
    else:
        return render(request, "data/login.html")


def register_user(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        
        if password1 != password2:
            messages.info(request, "Harap masukkan katasandi yang sama.")
            return redirect("data:register")
        
        try:
            user = User(first_name=first_name, last_name=last_name, username=username, email=email)
            user.set_password(password2)
            user.save()
            messages.success(request, "Berhasil mendaftarkan satu akun.")
            return redirect("data:login")
        except IntegrityError:
            messages.error(request, "User dengan informasi ini sudah ada.")
            return redirect("data:register")
    else:
        return render(request, "data/register.html")
        

def logout_user(request: HttpRequest) -> HttpResponse:
    """Handler untuk logout user.
    """
    logout(request)
    return redirect("data:login")


def home(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        # Jika user belum login atau terautentikasi.
        return redirect("data:login")
    
    data = Data.objects.filter(owner=request.user)
    return render(request, "data/home.html", {"data": data})

def tambah_data(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        # Jika user belum login atau terautentikasi.
        return redirect("data:login")
    
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        image = request.FILES["image"]

        data = Data(owner=request.user, title=title, description=description, image=image)
        data.save()
        
        messages.success(request, "Berhasil menambahkan satu data.")
        return redirect("data:home")
    else:
        return render(request, "data/tambah.html")

def edit_data(request: HttpRequest, pk: int) -> HttpResponse:
    if request.method == "GET":
        try:
            data = Data.objects.get(pk=pk)
            return render(request, "data/edit.html", {"data": data})
        except Data.DoesNotExist:
            raise Http404("Data tidak ditemukan.")
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        image = request.FILES["image"]
        try:
            data = Data.objects.get(pk=pk)
            data.title = title
            data.description = description
            data.image = image
            data.save()
            
            messages.success(request, "Berhasil memperbaharui data.")
            return redirect("data:home")
        except Data.DoesNotExist:
            raise Http404("Data tidak ditemukan.")


def hapus_data(request: HttpRequest, pk: int) -> HttpResponse:
    try:
        data = Data.objects.get(pk=pk)
        data.delete()
        messages.success(request, "Berhasil menghapus satu data.")
        return redirect("data:home")
    except Data.DoesNotExist:
        raise Http404("Data tidak ditemukan.")