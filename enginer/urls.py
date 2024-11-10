from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path("auth/", include("login.urls")), 
    path("plataforma/", include("plataforma.urls")),
    path("", lambda request: redirect('auth/login/'))


]
