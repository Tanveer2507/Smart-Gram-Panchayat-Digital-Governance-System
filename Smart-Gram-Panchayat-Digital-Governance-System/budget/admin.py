from django.contrib import admin
from .models import BudgetRecord

@admin.register(BudgetRecord)
class BudgetRecordAdmin(admin.ModelAdmin):
    list_display = ['title', 'department', 'allocated_amount', 'spent_amount', 'remaining_amount', 'financial_year', 'created_at']
    list_filter = ['department', 'financial_year', 'month']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at', 'remaining_amount']
    
    fieldsets = (
        ('Budget Information', {
            'fields': ('title', 'description', 'department')
        }),
        ('Financial Details', {
            'fields': ('amount', 'allocated_amount', 'spent_amount', 'remaining_amount')
        }),
        ('Period', {
            'fields': ('financial_year', 'month')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def remaining_amount(self, obj):
        return obj.allocated_amount - obj.spent_amount
    remaining_amount.short_description = 'Remaining Amount'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs
