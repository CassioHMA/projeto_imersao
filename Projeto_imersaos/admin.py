from django.contrib import admin
from .models import Equipamento, EmprestimoEquipamento, Colaborador, Usuario

admin.site.register(Usuario)
admin.site.register(Colaborador)
admin.site.register(Equipamento)


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