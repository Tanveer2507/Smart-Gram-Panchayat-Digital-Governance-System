from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Notice(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('scheduled', 'Scheduled'),
        ('expired', 'Expired'),
    ]
    
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('urgent', 'Urgent'),
        ('event', 'Event'),
        ('academic', 'Academic'),
        ('public', 'Public'),
        ('tender', 'Tender'),
        ('emergency', 'Emergency'),
        ('meeting', 'Meeting'),
        ('scheme', 'Scheme'),
        ('circular', 'Circular'),
    ]
    
    AUDIENCE_CHOICES = [
        ('all', 'All'),
        ('students', 'Students'),
        ('teachers', 'Teachers'),
        ('citizens', 'Citizens'),
        ('staff', 'Staff'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField(default='')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    target_audience = models.CharField(max_length=20, choices=AUDIENCE_CHOICES, default='all')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_urgent = models.BooleanField(default=False)
    document = models.FileField(upload_to='notices/documents/', blank=True, null=True)
    publish_date = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_notices')
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Legacy fields for backward compatibility
    description = models.TextField(blank=True, null=True)
    notice_type = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    published_date = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def update_status(self):
        """Auto-update status based on dates"""
        now = timezone.now()
        if self.status == 'published' and self.expiry_date and now > self.expiry_date:
            self.status = 'expired'
            self.save()
        elif self.status == 'scheduled' and self.publish_date and now >= self.publish_date:
            self.status = 'published'
            self.save()
