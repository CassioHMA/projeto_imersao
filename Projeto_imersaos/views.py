from django.shortcuts import render
from .models import equipamento, emprestimo, colaborador, cadastro, usuario

def index(request):
    """"Página Principal do Pereirao Projeto_imersao"""
    context = {
        'equipamentos': equipamento.objects.filter(ativo=True).count(),
        'emprestimos': emprestimo.objects.filter(status="Em aberto").count(),
        'colaboradores': colaborador.objects.all(),
    }
    return render(request, 'projeto_imersao/index.html')

def dashboard_data(request):
    """Retorna dados para o dashboard em formato JSON"""
    from django.http import JsonResponse
    data = {
        'total_equipamentos': equipamento.objects.count(),
        'total_emprestimos': emprestimo.objects.count(),
        'total_colaboradores': colaborador.objects.count(),
    }
    return JsonResponse(data)

# Create your views here.
