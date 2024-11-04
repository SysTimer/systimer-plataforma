from django.shortcuts import render

def login(request):
    return render(request,'login.html')

def cadastro(request):
    return render(request, 'cadastro.html')

def validar_login(request):
    pass

def validar_cadastro(request):
    pass