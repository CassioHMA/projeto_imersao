from django import forms
from .models import usuario, cadastro, colaborador, Equipamentos, emprestimo, historico_emprestimo

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = usuario
        fields = ['nome', 'email', 'senha']


class CadastroForm(forms.ModelForm):
    class Meta:
        model = cadastro
        fields = ['nome', 'idade', 'locacao', 'contato']


class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = colaborador
        fields = ['nome', 'setor', 'contato']


class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamentos
        fields = ['nome', 'descricao', 'preco', 'estoque', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do equipamento'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição do equipamento'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'estoque': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'ativo': forms.Select(attrs={'class': 'form-control'}, choices=[(True, 'Ativo'), (False, 'Inativo')]),
        }
        labels = {
            'nome': 'Nome do Equipamento',
            'descricao': 'Descrição',
            'preco': 'Preço (R$)',
            'estoque': 'Quantidade em Estoque',
            'ativo': 'Status',
        }


class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = emprestimo
        fields = ['produto', 'colaborador', 'data_devolucao', 'status']
        widget = {
            
        }


class HistoricoEmprestimoForm(forms.ModelForm):
    class Meta:
        model = historico_emprestimo
        fields = ['emprestimo', 'descricao_alteracao']
