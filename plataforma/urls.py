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
    path('atualizar_registro/', views.atualizar_registro_reprovada, name='atualizar_registro'),
    path('renderizar_cadastro/', views.renderizar_cadastro, name='renderizar_cadastro'),
    path('novo_projeto/', views.novo_projeto, name='novo_projeto'),
    path("cadastrar_tarefa/", views.cadastrar_tarefa, name="cadastrar_tarefa"),
    path("cadastrar_informacoes/", views.cadastrar_informacoes, name="cadastrar_informacoes"),
    path("criar_cliente/", views.criar_cliente, name="criar_cliente"),
    path("atualizar_registro_aprovada/", views.atualizar_registro_aprovada, name="atualizar_registro_aprovada"),
    path("analisar/", views.exibir_grafico, name="analisar"),
    path('editar_usuario/', views.editar_usuario, name='editar_usuario'),
    path('salvar_perfil/', views.salvar_perfil, name='salvar_perfil'),
    path('cadastrar_projeto', views.criar_projeto, name='cadastrar_projeto'),
    path('projetos/', views.listar_projeto, name='projetos'),
    path('equipe/', views.renderizar_equipe, name='equipe'),
    path('cadastrar_funcionario/', views.cadastrar_funcionario, name='cadastrar_funcionario'),
    path('get-projetos/', views.projetos_clientes, name='get_projetos'),

]
