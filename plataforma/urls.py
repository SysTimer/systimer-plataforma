from django.urls import path
from . import views
from django.shortcuts import redirect
urlpatterns = [
    path("", views.plataforma, name='plataforma'),
    path("novo/", views.renderizar_cadastro, name='cadastro_projeto'),
    path("sair/", views.sair, name="sair"),
    path("cadastrar_projeto/", views.cadastro_projeto, name='cadastro_projeto'),
    path("selecionar_empresa/", views.selecionar_empresa, name='selecionar_empresa'),
    path("home/", views.renderizar_plataforma, name='renderizar_plataforma'),
]
