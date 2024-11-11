from django.shortcuts import render, redirect
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
@login_required(login_url='/auth/login')
def plataforma(request):
    print(request.user)
    return render(request, 'home.html')
    
@login_required(login_url='/auth/login')
def sair(request):
    logout(request)
    return redirect('/auth/login')