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
    path('iniciar_tarefa/', views.iniciar_tarefa, name='iniciar_tarefa'),
    path('enviar_banco_horas/', views.enviar_banco_horas, name='enviar_banco_horas'),
    path('atualizar_registro/', views.atualizar_registro, name='atualizar_registro'),
    path('renderizar_cadastro/', views.renderizar_cadastro, name='renderizar_cadastro'),
    path('get-projetos/', views.projetos_clientes, name='get_projetos'),
    path('novo_projeto/', views.novo_projeto, name='novo_projeto'),
    path("cadastrar_tarefa/", views.cadastrar_tarefa, name="cadastrar_tarefa"),
]
