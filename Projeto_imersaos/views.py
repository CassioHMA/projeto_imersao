from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import equipamento, emprestimo, colaborador, cadastro, usuario

def register(request):
    """Página de registro de usuários"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Conta criada para {username}!')
            return redirect('login')  # Redirecionar para a página de login
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

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


def profile(request):
    """Página de perfil do usuário"""
    return render(request, 'registration/profile.html')

def index(request):
    """Página Principal do Pereirao Projeto_imersao"""
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
