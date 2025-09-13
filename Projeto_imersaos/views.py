from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import usuario, cadastro, colaborador, equipamento, emprestimo, historico_emprestimo
from .forms import UsuarioForm, CadastroForm, ColaboradorForm, EquipamentoForm, EmprestimoForm
from django.utils import timezone
from django.db.models import Q

# Views para Usuario
def lista_usuarios(request):
    usuarios = usuario.objects.all().order_by('-date_added')
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios})

def criar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'form_usuario.html', {'form': form, 'titulo': 'Criar Usuário'})

def editar_usuario(request, pk):
    usuario_obj = get_object_or_404(usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário atualizado com sucesso!')
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm(instance=usuario_obj)
    return render(request, 'form_usuario.html', {'form': form, 'titulo': 'Editar Usuário'})

@require_POST
def deletar_usuario(request, pk):
    usuario_obj = get_object_or_404(usuario, pk=pk)
    usuario_obj.delete()
    messages.success(request, 'Usuário deletado com sucesso!')
    return redirect('lista_usuarios')

# Views para Cadastro
def lista_cadastros(request):
    cadastros = cadastro.objects.all().order_by('-date_added')
    return render(request, 'lista_cadastros.html', {'cadastros': cadastros})

def criar_cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro criado com sucesso!')
            return redirect('lista_cadastros')
    else:
        form = CadastroForm()
    return render(request, 'form_cadastro.html', {'form': form, 'titulo': 'Criar Cadastro'})

def editar_cadastro(request, pk):
    cadastro_obj = get_object_or_404(cadastro, pk=pk)
    if request.method == 'POST':
        form = CadastroForm(request.POST, instance=cadastro_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro atualizado com sucesso!')
            return redirect('lista_cadastros')
    else:
        form = CadastroForm(instance=cadastro_obj)
    return render(request, 'form_cadastro.html', {'form': form, 'titulo': 'Editar Cadastro'})

@require_POST
def deletar_cadastro(request, pk):
    cadastro_obj = get_object_or_404(cadastro, pk=pk)
    cadastro_obj.delete()
    messages.success(request, 'Cadastro deletado com sucesso!')
    return redirect('lista_cadastros')

# Views para Colaborador
def lista_colaboradores(request):
    colaboradores = colaborador.objects.all().order_by('-date_added')
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
    colaborador_obj = get_object_or_404(colaborador, pk=pk)
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
    colaborador_obj = get_object_or_404(colaborador, pk=pk)
    colaborador_obj.delete()
    messages.success(request, 'Colaborador deletado com sucesso!')
    return redirect('lista_colaboradores')

# Views para Equipamento
def lista_equipamentos(request):
    equipamentos = equipamento.objects.filter(ativo=True).order_by('-date_added')
    return render(request, 'lista_equipamentos.html', {'equipamentos': equipamentos})

def criar_equipamento(request):
    if request.method == 'POST':
        form = EquipamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipamento criado com sucesso!')
            return redirect('lista_equipamentos')
    else:
        form = EquipamentoForm()
    return render(request, 'form_equipamento.html', {'form': form, 'titulo': 'Criar Equipamento'})

def editar_equipamento(request, pk):
    equipamento_obj = get_object_or_404(equipamento, pk=pk)
    if request.method == 'POST':
        form = EquipamentoForm(request.POST, instance=equipamento_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipamento atualizado com sucesso!')
            return redirect('lista_equipamentos')
    else:
        form = EquipamentoForm(instance=equipamento_obj)
    return render(request, 'form_equipamento.html', {'form': form, 'titulo': 'Editar Equipamento'})

@require_POST
def deletar_equipamento(request, pk):
    equipamento_obj = get_object_or_404(equipamento, pk=pk)
    equipamento_obj.ativo = False
    equipamento_obj.save()
    messages.success(request, 'Equipamento desativado com sucesso!')
    return redirect('lista_equipamentos')

# Views para Empréstimo
def lista_emprestimos(request):
    status_filter = request.GET.get('status', '')
    
    if status_filter:
        emprestimos = emprestimo.objects.filter(status=status_filter).order_by('-data_emprestimo')
    else:
        emprestimos = emprestimo.objects.all().order_by('-data_emprestimo')
    
    return render(request, 'lista_emprestimos.html', {
        'emprestimos': emprestimos,
        'status_filter': status_filter
    })

def criar_emprestimo(request):
    if request.method == 'POST':
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            emprestimo_obj = form.save(commit=False)
            
            # Verificar se o equipamento está disponível
            equipamento_obj = emprestimo_obj.equipamento
            if equipamento_obj.estoque <= 0:
                messages.error(request, 'Equipamento não disponível em estoque!')
                return render(request, 'form_emprestimo.html', {'form': form, 'titulo': 'Criar Empréstimo'})
            
            # Reduzir o estoque do equipamento
            equipamento_obj.estoque -= 1
            equipamento_obj.save()
            
            emprestimo_obj.save()
            
            # Criar histórico
            historico_emprestimo.objects.create(
                emprestimo=emprestimo_obj,
                descricao_alteracao=f'Empréstimo criado para {emprestimo_obj.colaborador.nome}'
            )
            
            messages.success(request, 'Empréstimo criado com sucesso!')
            return redirect('lista_emprestimos')
    else:
        form = EmprestimoForm()
    
    return render(request, 'form_emprestimo.html', {'form': form, 'titulo': 'Criar Empréstimo'})

def detalhes_emprestimo(request, pk):
    emprestimo_obj = get_object_or_404(emprestimo, pk=pk)
    historico = historico_emprestimo.objects.filter(emprestimo=emprestimo_obj).order_by('-data_alteracao')
    
    return render(request, 'detalhes_emprestimo.html', {
        'emprestimo': emprestimo_obj,
        'historico': historico
    })

@require_POST
def devolver_emprestimo(request, pk):
    emprestimo_obj = get_object_or_404(emprestimo, pk=pk)
    
    if emprestimo_obj.esta_devolvido():
        messages.warning(request, 'Este empréstimo já foi devolvido!')
        return redirect('lista_emprestimos')
    
    # Marcar devolução
    emprestimo_obj.marcar_devolucao()
    emprestimo_obj.status = 'devolvido'
    emprestimo_obj.save()
    
    # Aumentar o estoque do equipamento
    equipamento_obj = emprestimo_obj.equipamento
    equipamento_obj.estoque += 1
    equipamento_obj.save()
    
    # Criar histórico
    historico_emprestimo.objects.create(
        emprestimo=emprestimo_obj,
        descricao_alteracao=f'Empréstimo devolvido em {timezone.now().strftime("%d/%m/%Y %H:%M")}'
    )
    
    messages.success(request, 'Empréstimo devolvido com sucesso!')
    return redirect('lista_emprestimos')

@require_POST
def marcar_atraso(request, pk):
    emprestimo_obj = get_object_or_404(emprestimo, pk=pk)
    
    if emprestimo_obj.status != 'em atraso':
        emprestimo_obj.status = 'em atraso'
        emprestimo_obj.save()
        
        # Criar histórico
        historico_emprestimo.objects.create(
            emprestimo=emprestimo_obj,
            descricao_alteracao='Empréstimo marcado como em atraso'
        )
        
        messages.warning(request, 'Empréstimo marcado como em atraso!')
    
    return redirect('detalhes_emprestimo', pk=pk)

# Dashboard e relatórios
def dashboard(request):
    total_equipamentos = equipamento.objects.filter(ativo=True).count()
    total_emprestimos_ativos = emprestimo.objects.filter(status='ativo').count()
    total_emprestimos_atraso = emprestimo.objects.filter(status='em atraso').count()
    total_colaboradores = cadastro.objects.count()
    
    # Últimos empréstimos
    ultimos_emprestimos = emprestimo.objects.all().order_by('-data_emprestimo')[:5]
    
    # Equipamentos com estoque baixo
    equipamentos_estoque_baixo = equipamento.objects.filter(estoque__lte=2, ativo=True)
    
    return render(request, 'dashboard.html', {
        'total_equipamentos': total_equipamentos,
        'total_emprestimos_ativos': total_emprestimos_ativos,
        'total_emprestimos_atraso': total_emprestimos_atraso,
        'total_colaboradores': total_colaboradores,
        'ultimos_emprestimos': ultimos_emprestimos,
        'equipamentos_estoque_baixo': equipamentos_estoque_baixo
    })

# API para buscar equipamentos disponíveis
def api_equipamentos_disponiveis(request):
    equipamentos = equipamento.objects.filter(ativo=True, estoque__gt=0).values('id', 'nome')
    return JsonResponse(list(equipamentos), safe=False)

# API para buscar colaboradores
def api_colaboradores(request):
    colaboradores = cadastro.objects.all().values('id', 'nome')
    return JsonResponse(list(colaboradores), safe=False)