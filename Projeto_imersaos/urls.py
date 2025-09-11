from django.urls import path
from django.contrib import admin
from django.views.generic import TemplateView
from . import views
from django.contrib.auth import views as auth_views
from django.http import JsonResponse

urlpatterns = [
    path('', views.index, name='index'),
    path('api/dashboard/', views.dashboard_data, name='dashboard_data'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('dashboard/', TemplateView.as_view(template_name='projeto_imersao/dashboard.html'), name='dashboard'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('equipamentos/', views.equipamento_list, name='equipamento_list'),
    path('equipamentos/<int:pk>/', views.equipamento_detail, name='equipamento_detail'),
    path('emprestimos/', views.emprestimo_list, name='emprestimo_list'),
    path('emprestimos/<int:pk>/', views.emprestimo_detail,  name='emprestimo_detail'),
    path('colaboradores/', views.colaborador_list, name='colaborador_list'),
    path('colaboradores/<int:pk>/', views.colaborador_detail, name='colaborador_detail'),
    path('cadastros/', views.cadastro_list, name='cadastro_list'),
    path('cadastros/<int:pk>/', views.cadastro_detail, name='cadastro_detail'),
    path('usuarios/', views.usuario_list, name='usuario_list'),
    path('usuarios/<int:pk>/', views.usuario_detail, name='usuario_detail'),

]
def api_root(request):
    return JsonResponse({"message": "API Root"}) 
urlpatterns += [
    path('api/', api_root, name='api-root'),
]
