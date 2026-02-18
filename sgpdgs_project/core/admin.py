from django.contrib import admin
from .models import UserRole

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone', 'village', 'created_at']
    list_filter = ['role', 'village']
    search_fields = ['user__username', 'user__email', 'phone', 'village']
    list_editable = ['role']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Role & Permissions', {
            'fields': ('role',)
        }),
        ('Contact Details', {
            'fields': ('phone', 'address', 'village')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user')
