from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Usuários
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    
    # Cadastros
    path('cadastros/', views.lista_cadastros, name='lista_cadastros'),
    
    # Colaboradores
    path('colaboradores/', views.lista_colaboradores, name='lista_colaboradores'),
    
    # Equipamentos
   
    path('Equipamentos/', views.Equipamentos, name='equipamentos'),

    
    # Empréstimos
    path('emprestimos/', views.lista_emprestimos, name='lista_emprestimos'),
    path('emprestimos/criar/', views.criar_emprestimo, name='criar_emprestimo'),
    path('emprestimos/<int:pk>/', views.detalhes_emprestimo, name='detalhes_emprestimo'),
    path('emprestimos/<int:pk>/devolver/', views.devolver_emprestimo, name='devolver_emprestimo'),
    
    # APIs
    path('api/equipamentos-disponiveis/', views.api_equipamentos_disponiveis, name='api_equipamentos_disponiveis'),
    path('api/colaboradores/', views.api_colaboradores, name='api_colaboradores'),
    path('api/equipamentos/', views.api_equipamentos, name='api_equipamentos'),
    #
    # path('api/emprestimos/', views.api_emprestimos, name='api_emprestimos'),
]