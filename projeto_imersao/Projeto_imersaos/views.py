from django.shortcuts import render
from .models import equipamento, emprestimo, colaborador, cadastro, usuario

def index(request):
    """"Página Principal do Pereirao Projeto_imersao"""
    context = {
        'total_equipamentos': equipamento.objects.count(),  # Para exibir o total
        'equipamentos_list': equipamento.objects.all(),     # Para fazer o loop na template
        'total_emprestimos': emprestimo.objects.filter(data_devolucao__isnull=True).count(),
        'emprestimos_list': emprestimo.objects.filter(data_devolucao__isnull=True),
        'total_colaboradores': cadastro.objects.count(),
        'colaboradores_list': cadastro.objects.all(),

    }   
    return render(request, 'projeto_imersao/index.html', context)

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
