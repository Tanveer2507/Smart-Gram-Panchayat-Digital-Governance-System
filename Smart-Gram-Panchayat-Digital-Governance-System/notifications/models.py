from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('info', 'Information'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('announcement', 'Announcement'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='info')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    # Target audience
    target_all_users = models.BooleanField(default=True)
    target_roles = models.CharField(max_length=500, blank=True, help_text="Comma-separated role codes")
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class UserNotification(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_notifications')
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    related_link = models.CharField(max_length=500, blank=True, help_text="URL to redirect when clicked")
    
    class Meta:
        unique_together = ['notification', 'user']
        ordering = ['-notification__created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.notification.title}"


class AdminNotification(models.Model):
    """Individual notifications for admin users"""
    NOTIFICATION_TYPES = [
        ('complaint', 'New Complaint'),
        ('certificate', 'Certificate Request'),
        ('user', 'New User Registration'),
        ('budget', 'Budget Alert'),
        ('notice', 'Notice Published'),
        ('system', 'System Alert'),
        ('info', 'Information'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='info')
    related_link = models.CharField(max_length=500, blank=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
