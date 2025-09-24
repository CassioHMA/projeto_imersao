from django import forms
from .models import Usuario, Colaborador, Equipamento, EmprestimoEquipamento

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'senha']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'senha': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = Colaborador
        fields = ['nome', 'setor', 'contato']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'setor': forms.TextInput(attrs={'class': 'form-control'}),
            'contato': forms.TextInput(attrs={'class': 'form-control'}),
        }

class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
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
        model = EmprestimoEquipamento
        fields = ['equipamento', 'colaborador', 'data_devolucao', 'status']
        widgets = {
            'equipamento': forms.Select(attrs={'class': 'form-control'}),
            'colaborador': forms.Select(attrs={'class': 'form-control'}),
            'data_devolucao': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'equipamento': 'Equipamento',
            'colaborador': 'Colaborador',
            'data_devolucao': 'Data de Devolução',
            'status': 'Status',
        }
