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

]
def api_root(request):
    return JsonResponse({"message": "API Root"}) 
urlpatterns += [
    path('api/', api_root, name='api-root'),
]
