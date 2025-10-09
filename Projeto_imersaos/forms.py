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
        fields = ['nome', 'cpf', 'cargo', 'setor']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'setor': forms.TextInput(attrs={'class': 'form-control'}),
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
        # Removido 'status' e 'data_devolucao' que são controlados pela lógica do sistema
        fields = ['equipamento', 'colaborador', 'quantidade', 'data_devolucao_prevista', 'observacoes']
        widgets = {
            'equipamento': forms.Select(attrs={'class': 'form-control'}),
            'colaborador': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'data_devolucao_prevista': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'equipamento': 'Equipamento',
            'colaborador': 'Colaborador',
            'quantidade': 'Quantidade',
            'data_devolucao_prevista': 'Devolução Prevista',
            'observacoes': 'Observações',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra o queryset para mostrar apenas equipamentos com estoque > 0 e ativos
        self.fields['equipamento'].queryset = Equipamento.objects.filter(estoque__gt=0, ativo=True)

    def clean(self):
        """
        Valida se a quantidade solicitada está disponível no estoque do equipamento.
        """
        cleaned_data = super().clean()
        equipamento = cleaned_data.get('equipamento')
        quantidade = cleaned_data.get('quantidade')

        if equipamento and quantidade:
            if quantidade <= 0:
                self.add_error('quantidade', 'A quantidade deve ser um número positivo.')
            
            if equipamento.estoque < quantidade:
                self.add_error('quantidade', f'Estoque insuficiente. Apenas {equipamento.estoque} unidades disponíveis.')
        
        return cleaned_data
