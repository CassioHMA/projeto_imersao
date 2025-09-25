from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Usuario, Colaborador, Equipamento, EmprestimoEquipamento
from .forms import UsuarioForm, ColaboradorForm, EquipamentoForm, EmprestimoForm
from django.utils import timezone
from django.db import transaction
from django.contrib.auth.hashers import make_password


# Views para Usuario
def lista_usuarios(request):
    usuarios = Usuario.objects.all().order_by('-date_added')
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios})

def criar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            # É CRUCIAL fazer o hash da senha, nunca salvar em texto plano.
            usuario = form.save(commit=False)
            usuario.senha = make_password(form.cleaned_data['senha'])
            usuario.save()
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'form_usuario.html', {'form': form, 'titulo': 'Criar Usuário'})

def editar_usuario(request, pk):
    usuario_obj = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario_obj)
        if form.is_valid():
            usuario = form.save(commit=False)
            # Apenas atualiza a senha se uma nova foi fornecida
            if form.cleaned_data['senha']:
                 usuario.senha = make_password(form.cleaned_data['senha'])
            usuario.save()
            messages.success(request, 'Usuário atualizado com sucesso!')
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm(instance=usuario_obj)
    return render(request, 'form_usuario.html', {'form': form, 'titulo': 'Editar Usuário'})

# Views para Colaborador
def lista_colaboradores(request):
    colaboradores = Colaborador.objects.all().order_by('-date_added')
    return render(request, 'lista_colaboradores.html', {'colaboradores': colaboradores})

def criar_colaborador(request):
    if request.method == 'POST':
        form = ColaboradorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Colaborador criado com sucesso!')
            return redirect('lista_colaboradores')
    else:
        form = ColaboradorForm()
    return render(request, 'form_colaborador.html', {'form': form, 'titulo': 'Criar Colaborador'})

def editar_colaborador(request, pk):
    colaborador_obj = get_object_or_404(Colaborador, pk=pk)
    if request.method == 'POST':
        form = ColaboradorForm(request.POST, instance=colaborador_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Colaborador atualizado com sucesso!')
            return redirect('lista_colaboradores')
    else:
        form = ColaboradorForm(instance=colaborador_obj)
    return render(request, 'form_colaborador.html', {'form': form, 'titulo': 'Editar Colaborador'})

@require_POST
def deletar_colaborador(request, pk):
    colaborador_obj = get_object_or_404(Colaborador, pk=pk)
    colaborador_obj.delete()
    messages.success(request, 'Colaborador deletado com sucesso!')
    return redirect('lista_colaboradores')

# Views para Equipamento
def lista_equipamentos(request):
    equipamentos = Equipamento.objects.all().order_by('nome')
    form = EquipamentoForm() # Formulário para o modal de criação
    context = {
        'equipamentos': equipamentos,
        'form': form
    }
    return render(request, 'equipamentos.html', context)

def criar_equipamento(request):
    if request.method == 'POST':
        form = EquipamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipamento criado com sucesso!')
            return redirect('lista_equipamentos')
    else:
        form = EquipamentoForm()
    
    context = {
        'form': form,
        'criar': True
    }
    return render(request, 'equipamentos.html', context)

def editar_equipamento(request, id):
    equipamento = get_object_or_404(Equipamento, id=id)
    
    if request.method == 'POST':
        form = EquipamentoForm(request.POST, instance=equipamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipamento atualizado com sucesso!')
            return redirect('lista_equipamentos')
    else:
        form = EquipamentoForm(instance=equipamento)
    
    context = {
        'form': form,
        'equipamento': equipamento,
        'editar': True
    }
    return render(request, 'equipamentos.html', context)

def excluir_equipamento(request, id):
    equipamento = get_object_or_404(Equipamento, id=id)
    
    if request.method == 'POST':
        equipamento.delete()
        messages.success(request, 'Equipamento excluído com sucesso!')
        return redirect('lista_equipamentos')
    
    context = {
        'equipamento': equipamento
    }
    return render(request, 'confirmar_exclusao.html', context)

def api_equipamentos(request):
    equipamentos = Equipamento.objects.all().values('id', 'nome', 'descricao', 'preco', 'estoque', 'ativo')
    return JsonResponse(list(equipamentos), safe=False)


# Views para Empréstimo de Equipamento
def emprestimo_equipamento(request):
    if request.method == 'POST':
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    emprestimo = form.save(commit=False)
                    equipamento = emprestimo.equipamento
                    if equipamento.estoque > 0:
                        equipamento.estoque -= 1
                        equipamento.save()
                        emprestimo.save()
                        messages.success(request, 'Empréstimo registrado com sucesso!')
                    else:
                        messages.error(request, 'Equipamento sem estoque disponível.')
            except Exception as e:
                messages.error(request, f'Ocorreu um erro: {e}')
            return redirect('emprestimo_equipamento')
    else:
        form = EmprestimoForm()
    
    emprestimos = EmprestimoEquipamento.objects.select_related('equipamento', 'colaborador').all().order_by('-data_emprestimo')
    
    context = {
        'form': form,
        'emprestimos': emprestimos
    }
    return render(request, 'emprestimos.html', context)



# Dashboard e relatórios
def dashboard(request):
    total_equipamentos = Equipamento.objects.count()
    total_emprestimos_ativos = EmprestimoEquipamento.objects.filter(status='ativo').count()
    total_emprestimos_atraso = EmprestimoEquipamento.objects.filter(status='em_atraso').count()
    total_colaboradores = Colaborador.objects.count()

    ultimos_emprestimos = EmprestimoEquipamento.objects.select_related('equipamento', 'colaborador').order_by('-data_emprestimo')[:5]
    equipamentos_estoque_baixo = Equipamento.objects.filter(estoque__lt=5)

    context = {
        'total_equipamentos': total_equipamentos,
        'total_emprestimos_ativos': total_emprestimos_ativos,
        'total_emprestimos_atraso': total_emprestimos_atraso,
        'total_colaboradores': total_colaboradores,
        'ultimos_emprestimos': ultimos_emprestimos,
        'equipamentos_estoque_baixo': equipamentos_estoque_baixo,
    }

    return render(request, 'partials/dashboard.html', context)
    

# API para buscar equipamentos disponíveis
def api_equipamentos_disponiveis(request):
    equipamentos = Equipamento.objects.filter(ativo=True, estoque__gt=0).values('id', 'nome')
    return JsonResponse(list(equipamentos), safe=False)

# API para buscar colaboradores
def api_colaboradores(request):
    colaboradores = Colaborador.objects.all().values('id', 'nome')
    return JsonResponse(list(colaboradores), safe=False)