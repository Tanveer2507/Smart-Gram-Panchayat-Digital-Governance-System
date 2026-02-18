from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.change_password, name='change_password'),
    
    # Admin login
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-users/', views.admin_manage_users, name='admin_manage_users'),
    path('manage-users/create/', views.admin_create_user, name='admin_create_user'),
    path('manage-users/<int:user_id>/edit/', views.admin_edit_user, name='admin_edit_user'),
    path('manage-users/<int:user_id>/delete/', views.admin_delete_user, name='admin_delete_user'),
    path('settings/', views.admin_settings, name='admin_settings'),
    
    # Role-specific logins (Kept for backward compatibility but not shown in menu)
    # path('sarpanch/login/', views.sarpanch_login, name='sarpanch_login'),
    # path('sarpanch/dashboard/', views.sarpanch_dashboard, name='sarpanch_dashboard'),
    # path('secretary/login/', views.secretary_login, name='secretary_login'),
    # path('accountant/login/', views.accountant_login, name='accountant_login'),
    # path('block-officer/login/', views.block_officer_login, name='block_officer_login'),
    
    # Public information pages
    path('about-us/', views.about_us, name='about_us'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('faqs/', views.faqs, name='faqs'),
]
