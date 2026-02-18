from django.urls import path
from . import views

urlpatterns = [
    path('', views.certificate_list, name='certificate_list'),
    path('create/', views.certificate_create, name='certificate_create'),
    path('<int:pk>/', views.certificate_detail, name='certificate_detail'),
    path('admin/manage/', views.admin_manage_certificates, name='admin_manage_certificates'),
    
    # API endpoints
    path('api/<int:pk>/', views.certificate_api_detail, name='certificate_api_detail'),
    path('api/<int:pk>/delete/', views.certificate_api_delete, name='certificate_api_delete'),
    
    # Download certificate
    path('<int:pk>/download/', views.certificate_download, name='certificate_download'),
]
