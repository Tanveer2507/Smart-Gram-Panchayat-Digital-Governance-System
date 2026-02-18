from django.contrib import admin
from .models import Notice

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'notice_type', 'is_urgent', 'is_active', 'published_date', 'created_at']
    list_filter = ['notice_type', 'is_urgent', 'is_active', 'published_date']
    search_fields = ['title', 'description']
    list_editable = ['is_active', 'is_urgent']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Notice Information', {
            'fields': ('title', 'description', 'notice_type')
        }),
        ('Status & Priority', {
            'fields': ('is_urgent', 'is_active')
        }),
        ('Dates', {
            'fields': ('published_date', 'expiry_date')
        }),
        ('Attachments', {
            'fields': ('document',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_urgent', 'mark_as_active', 'mark_as_inactive']
    
    def mark_as_urgent(self, request, queryset):
        queryset.update(is_urgent=True)
        self.message_user(request, f'{queryset.count()} notices marked as urgent.')
    mark_as_urgent.short_description = 'Mark as Urgent'
    
    def mark_as_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f'{queryset.count()} notices activated.')
    mark_as_active.short_description = 'Activate selected notices'
    
    def mark_as_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f'{queryset.count()} notices deactivated.')
    mark_as_inactive.short_description = 'Deactivate selected notices'
