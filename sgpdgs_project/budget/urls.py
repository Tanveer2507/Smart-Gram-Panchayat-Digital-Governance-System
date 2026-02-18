from django.urls import path
from . import views

urlpatterns = [
    path('', views.budget_dashboard, name='budget_dashboard'),
    path('admin/manage/', views.admin_manage_budget, name='admin_manage_budget'),
    
    # API endpoints
    path('api/<int:pk>/', views.budget_api_detail, name='budget_api_detail'),
    path('api/<int:pk>/delete/', views.budget_api_delete, name='budget_api_delete'),
]
