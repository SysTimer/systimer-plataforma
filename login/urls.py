
from django.urls import path
from . import views
from django.shortcuts import redirect
urlpatterns = [
    path("login/", views.login, name='login'),
    path("cadastro/", views.cadastro, name='cadastro'),
    path("validar_login/", views.validar_login, name='validar_login'),
    path("validar_cadastro/", views.validar_cadastro, name='validar_cadastro')

]
