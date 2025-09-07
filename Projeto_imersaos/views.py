from django.shortcuts import render

def index(request):
    """"Página Principal do Pereirao Projeto_imersao"""
    return render(request, 'projeto_imersao/index.html')

# Create your views here.
