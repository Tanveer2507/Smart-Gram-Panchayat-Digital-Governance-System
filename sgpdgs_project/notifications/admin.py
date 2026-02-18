from django.contrib import admin
from .models import Notification, UserNotification, AdminNotification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'notification_type', 'priority', 'created_by', 'created_at', 'is_active']
    list_filter = ['notification_type', 'priority', 'is_active', 'created_at']
    search_fields = ['title', 'message']
    date_hierarchy = 'created_at'

@admin.register(UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification', 'is_read', 'read_at']
    list_filter = ['is_read', 'notification__notification_type']
    search_fields = ['user__username', 'notification__title']

@admin.register(AdminNotification)
class AdminNotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    date_hierarchy = 'created_at'
