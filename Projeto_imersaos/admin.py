from django.contrib import admin
from .models import equipamento, emprestimo, colaborador, cadastro, usuario

admin.site.register(cadastro)

@admin.register(emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ['produto', 'get_colaborador', 'data_emprestimo', 'status']
    list_filter = ['status', 'data_emprestimo']
    
    def get_equipamento(self, obj):
        return obj.equipamento.nome  # ou o campo que você quer mostrar
    get_equipamento.short_description = 'Equipamento'
    
    def get_colaborador(self, obj):
        return obj.colaborador.nome  # ou o campo que você quer mostrar
    get_colaborador.short_description = 'Colaborador'