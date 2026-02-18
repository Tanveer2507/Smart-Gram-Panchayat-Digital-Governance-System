from django.contrib import admin
from .models import Complaint

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'category', 'status', 'priority', 'created_at']
    list_filter = ['status', 'priority', 'category', 'created_at']
    search_fields = ['title', 'description', 'user__username', 'location']
    list_editable = ['status', 'priority']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Complaint Information', {
            'fields': ('user', 'title', 'description', 'category', 'location')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority', 'assigned_to')
        }),
        ('Attachments', {
            'fields': ('image',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_completed', 'mark_as_in_progress', 'mark_as_high_priority']
    
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
        self.message_user(request, f'{queryset.count()} complaints marked as completed.')
    mark_as_completed.short_description = 'Mark selected as Completed'
    
    def mark_as_in_progress(self, request, queryset):
        queryset.update(status='in_progress')
        self.message_user(request, f'{queryset.count()} complaints marked as in progress.')
    mark_as_in_progress.short_description = 'Mark selected as In Progress'
    
    def mark_as_high_priority(self, request, queryset):
        queryset.update(priority='high')
        self.message_user(request, f'{queryset.count()} complaints marked as high priority.')
    mark_as_high_priority.short_description = 'Mark as High Priority'
