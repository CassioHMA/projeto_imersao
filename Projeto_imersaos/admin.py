from django.contrib import admin
from .models import Equipamento, EmprestimoEquipamento, Colaborador, Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'date_added')
    search_fields = ('nome', 'email')

@admin.register(Colaborador)
class ColaboradorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'matricula', 'setor', 'date_added')
    search_fields = ('nome', 'matricula', 'setor')

@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'estoque', 'ativo', 'data_cadastro')
    search_fields = ('nome',)
    list_filter = ('ativo', 'data_cadastro')

@admin.register(EmprestimoEquipamento)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ['get_equipamento', 'get_colaborador', 'data_emprestimo', 'status']
    list_filter = ['status', 'data_emprestimo']
    search_fields = ['equipamento__nome', 'colaborador__nome']
    
    def get_equipamento(self, obj):
        return obj.equipamento.nome  # ou o campo que você quer mostrar
    get_equipamento.short_description = 'Equipamento'
    
    def get_colaborador(self, obj):
        return obj.colaborador.nome  # ou o campo que você quer mostrar
    get_colaborador.short_description = 'Colaborador'