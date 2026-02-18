from django.contrib import admin
from .models import Certificate

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['application_number', 'applicant_name', 'certificate_type', 'status', 'created_at']
    list_filter = ['status', 'certificate_type', 'created_at']
    search_fields = ['application_number', 'applicant_name', 'father_name', 'user__username']
    list_editable = ['status']
    readonly_fields = ['application_number', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Application Details', {
            'fields': ('application_number', 'user', 'certificate_type')
        }),
        ('Applicant Information', {
            'fields': ('applicant_name', 'father_name', 'address', 'purpose')
        }),
        ('Status & Review', {
            'fields': ('status', 'remarks')
        }),
        ('Documents', {
            'fields': ('document',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_certificates', 'reject_certificates', 'mark_under_review']
    
    def approve_certificates(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, f'{queryset.count()} certificates approved.')
    approve_certificates.short_description = 'Approve selected certificates'
    
    def reject_certificates(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f'{queryset.count()} certificates rejected.')
    reject_certificates.short_description = 'Reject selected certificates'
    
    def mark_under_review(self, request, queryset):
        queryset.update(status='under_review')
        self.message_user(request, f'{queryset.count()} certificates marked under review.')
    mark_under_review.short_description = 'Mark as Under Review'
