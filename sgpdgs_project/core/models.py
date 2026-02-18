from django.db import models
from django.contrib.auth.models import User

class UserRole(models.Model):
    ROLE_CHOICES = [
        ('administrator', 'Administrator'),
        ('citizen', 'Citizen'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='role')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='citizen')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    village = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
