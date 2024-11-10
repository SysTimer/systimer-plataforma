from django.shortcuts import render
# Create your views here.


def plataforma(request):
    return render(request, 'home.html')
    