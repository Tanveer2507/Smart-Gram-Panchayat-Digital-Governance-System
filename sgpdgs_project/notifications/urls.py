from django.urls import path
from . import views

urlpatterns = [
    # Admin notification management
    path('admin/manage/', views.admin_manage_notifications, name='admin_manage_notifications'),
    path('admin/create/', views.admin_create_notification, name='admin_create_notification'),
    path('admin/edit/<int:notification_id>/', views.admin_edit_notification, name='admin_edit_notification'),
    path('admin/delete/<int:notification_id>/', views.admin_delete_notification, name='admin_delete_notification'),
    
    # Admin notification center (bell icon)
    path('admin/notification-center/', views.admin_notification_center, name='admin_notification_center'),
    path('admin/api/get-notifications/', views.get_admin_notifications, name='get_admin_notifications'),
    path('admin/api/mark-read/', views.mark_notification_read, name='mark_notification_read'),
    path('admin/api/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path('admin/notification/<int:notification_id>/delete/', views.delete_admin_notification, name='delete_admin_notification'),
    
    # User notifications
    path('my-notifications/', views.user_notifications, name='user_notifications'),
]
