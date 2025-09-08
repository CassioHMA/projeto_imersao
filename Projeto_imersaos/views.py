from django.shortcuts import render
from .models import Equipamentos, Emprestimos, colaboradores, Cadastro, usuario

def index(request):
    """"Página Principal do Pereirao Projeto_imersao"""
    context = {
        'equipamentos': Equipamentos.objects.filter(ativo=True).count(),
        'emprestimos': Emprestimos.objects.filter(status="Em aberto").count(),
        'colaboradores': colaboradores.objects.all(),
    }
    return render(request, 'projeto_imersao/index.html')

# Create your views here.
