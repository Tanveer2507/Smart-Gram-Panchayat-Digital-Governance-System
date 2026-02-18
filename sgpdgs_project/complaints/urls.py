from django.urls import path
from . import views

urlpatterns = [
    path('', views.complaint_list, name='complaint_list'),
    path('create/', views.complaint_create, name='complaint_create'),
    path('<int:pk>/', views.complaint_detail, name='complaint_detail'),
    path('admin/manage/', views.admin_manage_complaints, name='admin_manage_complaints'),
    
    # API endpoints
    path('api/<int:pk>/', views.complaint_api_detail, name='complaint_api_detail'),
    path('api/<int:pk>/delete/', views.complaint_api_delete, name='complaint_api_delete'),
]
