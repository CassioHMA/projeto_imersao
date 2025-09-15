from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import usuario, cadastro, colaborador, Equipamentos, emprestimo, historico_emprestimo
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
def Equipamentos(request):
    # Obter todos os equipamentos do banco de dados
    equipamentos = Equipamentos.objects.all()
    
    # Verificar se é uma requisição POST (envio de formulário)
    if request.method == 'POST':
        form = EquipamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipamento salvo com sucesso!')
            return redirect('equipamentos')
    else:
        form = EquipamentoForm()
    
    context = {
        'equipamentos': equipamentos,
        'form': form
    }
    return render(request, 'equipamentos.html', context)

def editar_equipamento(request, id):
    equipamento = get_object_or_404(Equipamentos, id=id)
    
    if request.method == 'POST':
        form = EquipamentoForm(request.POST, instance=equipamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipamento atualizado com sucesso!')
            return redirect('equipamentos')
    else:
        form = EquipamentoForm(instance=equipamento)
    
    context = {
        'form': form,
        'equipamento': equipamento,
        'editar': True
    }
    return render(request, 'equipamentos.html', context)

def excluir_equipamento(request, id):
    equipamento = get_object_or_404(Equipamentos, id=id)
    
    if request.method == 'POST':
        equipamento.delete()
        messages.success(request, 'Equipamento excluído com sucesso!')
        return redirect('equipamentos')
    
    context = {
        'equipamento': equipamento
    }
    return render(request, 'confirmar_exclusao.html', context)

def api_equipamentos(request):
    equipamentos = Equipamentos.objects.all().values('id', 'nome', 'descricao', 'preco', 'estoque', 'ativo')
    return JsonResponse(list(equipamentos), safe=False)

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
        try:
            # Processar o formulário
            produto_id = request.POST.get('produto')
            colaborador_id = request.POST.get('colaborador')
            data_emprestimo = request.POST.get('data_emprestimo')
            data_devolucao = request.POST.get('data_devolucao') or None
            status = request.POST.get('status')
            
            # Criar o empréstimo
            emprestimo_obj = emprestimo(
                produto_id=produto_id,
                colaborador_id=colaborador_id,
                data_emprestimo=data_emprestimo,
                data_devolucao=data_devolucao,
                status=status
            )
            emprestimo_obj.save()
            
            messages.success(request, 'Empréstimo criado com sucesso!')
            return redirect('partials/emprestimos/lista_emprestimos')  # Ou o nome da sua URL de lista
            
        except Exception as e:
            messages.error(request, f'Erro ao criar empréstimo: {str(e)}')
    
    # GET request - mostrar formulário
    equipamentos = Equipamentos.objects.all()
    colaboradores = colaborador.objects.all()
    
    # CORRIJA ESTA LINHA - use o nome correto do template
    return render(request, 'partials/emprestimos/criar_emprestimo.html', {
        'equipamentos': equipamentos,
        'colaboradores': colaboradores
    })

def detalhes_emprestimo(request, pk):
    emprestimo_obj = get_object_or_404(emprestimo, pk=pk)
    historico = historico_emprestimo.objects.filter(emprestimo=emprestimo_obj).order_by('-data_alteracao')
    
    return render(request, 'partials/emprestimos/detalhes_emprestimo.html', {
        'emprestimo': emprestimo_obj,
        'historico': historico
    })

def lista_emprestimos(request):
    emprestimos = emprestimo.objects.all().order_by('-data_emprestimo')
    return render(request, 'partials/emprestimos/lista_emprestimos.html', {'emprestimos': emprestimos})

@require_POST
def devolver_emprestimo(request, pk):
    emprestimo_obj = get_object_or_404(emprestimo, pk=pk)
    
    if emprestimo_obj.esta_devolvido():
        messages.warning(request, 'Este empréstimo já foi devolvido!')
        return redirect('partials/emprestimos/lista_emprestimos')
    
    # Marcar devolução
    emprestimo_obj.marcar_devolucao()
    emprestimo_obj.status = 'devolvido'
    emprestimo_obj.save()
    
    # Aumentar o estoque do produto
    produto_obj = emprestimo_obj.produto
    produto_obj.estoque += 1
    produto_obj.save()
    
    # Criar histórico
    historico_emprestimo.objects.create(
        emprestimo=emprestimo_obj,
        descricao_alteracao=f'Empréstimo devolvido em {timezone.now().strftime("%d/%m/%Y %H:%M")}'
    )
    
    messages.success(request, 'Empréstimo devolvido com sucesso!')
    return redirect('partials/emprestimos/lista_emprestimos')

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
    
    return redirect('partials/emprestimos/detalhes_emprestimo', pk=pk)

# Dashboard e relatórios
def dashboard(request):
    total_equipamentos = Equipamentos.objects.count()
    total_emprestimos_ativos = emprestimo.objects.filter(status='ativo').count()
    total_emprestimos_atraso = emprestimo.objects.filter(status='em atraso').count()
    total_colaboradores = colaborador.objects.count()

    ultimos_emprestimos = emprestimo.objects.order_by('-data_emprestimo')[:5]
    equipamentos_estoque_baixo = Equipamentos.objects.filter(estoque__lt=5)

    context = {
        'total_equipamentos': total_equipamentos,
        'total_emprestimos_ativos': total_emprestimos_ativos,
        'total_emprestimos_atraso': total_emprestimos_atraso,
        'total_colaboradores': total_colaboradores,
        'ultimos_emprestimos': ultimos_emprestimos,
        'equipamentos_estoque_baixo': equipamentos_estoque_baixo,
    }

    # sempre usa o caminho do app
    return render(request, 'partials/dashboard.html', context)
    

# API para buscar equipamentos disponíveis
def api_equipamentos_disponiveis(request):
    equipamentos = Equipamentos.objects.filter(ativo=True, estoque__gt=0).values('id', 'nome')
    return JsonResponse(list(equipamentos), safe=False)

# API para buscar colaboradores
def api_colaboradores(request):
    colaboradores = colaborador.objects.all().values('id', 'nome')
    return JsonResponse(list(colaboradores), safe=False)