from django.urls import path
from . import views

urlpatterns = [
    path('', views.notice_list, name='notice_list'),
    path('<int:pk>/', views.notice_detail, name='notice_detail'),
    path('admin/manage/', views.admin_manage_notices, name='admin_manage_notices'),
    
    # API endpoints
    path('api/<int:pk>/', views.notice_api_detail, name='notice_api_detail'),
    path('api/<int:pk>/delete/', views.notice_api_delete, name='notice_api_delete'),
]
