from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Usuários
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/criar/', views.criar_usuario, name='criar_usuario'),
    path('usuarios/editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/deletar/<int:pk>/', views.deletar_usuario, name='deletar_usuario'),
    
    # Cadastros
    path('cadastros/', views.lista_cadastros, name='lista_cadastros'),
    path('cadastros/criar/', views.criar_cadastro, name='criar_cadastro'),
    path('cadastros/editar/<int:pk>/', views.editar_cadastro, name='editar_cadastro'),
    path('cadastros/deletar/<int:pk>/', views.deletar_cadastro, name='deletar_cadastro'),
    
    # Colaboradores
    path('colaboradores/', views.lista_colaboradores, name='lista_colaboradores'),
    path('colaboradores/criar/', views.criar_colaborador, name='criar_colaborador'),
    path('colaboradores/editar/<int:pk>/', views.editar_colaborador, name='editar_colaborador'),
    path('colaboradores/deletar/<int:pk>/', views.deletar_colaborador, name='deletar_colaborador'),
    
    # Equipamentos
    path('equipamentos/', views.lista_equipamentos, name='lista_equipamentos'),
    path('equipamentos/criar/', views.criar_equipamento, name='criar_equipamento'),
    path('equipamentos/editar/<int:pk>/', views.editar_equipamento, name='editar_equipamento'),
    path('equipamentos/deletar/<int:pk>/', views.deletar_equipamento, name='deletar_equipamento'),
    
    # Empréstimos
    path('emprestimos/', views.lista_emprestimos, name='lista_emprestimos'),
    path('emprestimos/criar/', views.criar_emprestimo, name='criar_emprestimo'),
    path('emprestimos/detalhes/<int:pk>/', views.detalhes_emprestimo, name='detalhes_emprestimo'),
    path('emprestimos/devolver/<int:pk>/', views.devolver_emprestimo, name='devolver_emprestimo'),
    path('emprestimos/marcar-atraso/<int:pk>/', views.marcar_atraso, name='marcar_atraso'),
    
    # APIs
    path('api/equipamentos-disponiveis/', views.api_equipamentos_disponiveis, name='api_equipamentos_disponiveis'),
    path('api/colaboradores/', views.api_colaboradores, name='api_colaboradores'),
]