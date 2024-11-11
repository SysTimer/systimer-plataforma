from django.shortcuts import render
# Create your views here.
from django.contrib.auth.decorators import login_required

@login_required(login_url='/auth/login')
def plataforma(request):
    print(request.user)
    return render(request, 'home.html')
    