
from django.urls import path
from . import views
from django.shortcuts import redirect

urlpatterns = [
    path("login/", views.login, name='login'),
    path("cadastro/", views.cadastro, name='cadastro'),
    path("validar_login/", views.validar_login, name='validar_login'),
    path("validar_cadastro/", views.validar_cadastro, name='validar_cadastro'),
    path("recuperar/", views.recuperar_senha, name='recuperar_senha'),
    path("validar_token/", views.validar_token, name='validar_token'),
    path("recuperar_acesso/", views.recuperar_acesso, name='recuperar_acesso'),
    path("update/", views.update_view, name='update'),
    path("update_password/", views.update_password, name='update_password'),
    path("funcionario_novo/", views.update_view_funcionario, name='funcionario_novo'),
    path("update_funcionario/", views.update_funcionario, name='update_funcionario'),

]
