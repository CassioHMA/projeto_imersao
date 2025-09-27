from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Usuários
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/criar/', views.criar_usuario, name='criar_usuario'),
    path('usuarios/editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    
    # Colaboradores
    path('colaboradores/', views.lista_colaboradores, name='lista_colaboradores'),
    path('colaboradores/criar/', views.criar_colaborador, name='criar_colaborador'),
    path('colaboradores/editar/<int:pk>/', views.editar_colaborador, name='editar_colaborador'),
    path('colaboradores/deletar/<int:pk>/', views.deletar_colaborador, name='deletar_colaborador'),
    
    # Equipamentos
    path('equipamentos/', views.lista_equipamentos, name='lista_equipamentos'),
    path('equipamentos/criar/', views.criar_equipamento, name='criar_equipamento'),
    path('equipamentos/editar/<int:id>/', views.editar_equipamento, name='editar_equipamento'),
    path('equipamentos/excluir/<int:id>/', views.excluir_equipamento, name='excluir_equipamento'),
    
    # Empréstimos - URLs consolidadas e organizadas
    path('emprestimos/', views.emprestimo_equipamento, name='emprestimos'),
    path('emprestimos/', views.emprestimo_equipamento, name='lista_emprestimos'),  # Alias para compatibilidade
    path('emprestimos/criar/', views.emprestimo_equipamento, name='criar_emprestimo'),  # Mesma view, método POST
    
    # APIs
    path('api/equipamentos-disponiveis/', views.api_equipamentos_disponiveis, name='api_equipamentos_disponiveis'),
    path('api/colaboradores/', views.api_colaboradores, name='api_colaboradores'),
    path('api/colaboradores/<int:pk>/', views.api_colaborador_detail, name='api_colaborador_detail'),
    path('api/equipamentos/', views.api_equipamentos, name='api_equipamentos'),
]