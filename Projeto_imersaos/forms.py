from django import forms
from .models import usuario, cadastro, colaborador, equipamento, emprestimo, historico_emprestimo

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
        model = equipamento
        fields = ['nome', 'descricao', 'preco', 'estoque', 'ativo']


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
