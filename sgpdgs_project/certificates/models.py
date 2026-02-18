from django.db import models
from django.contrib.auth.models import User

class Certificate(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('issued', 'Issued'),
    ]
    
    TYPE_CHOICES = [
        ('income', 'Income Certificate'),
        ('residence', 'Residence Certificate'),
        ('caste', 'Caste Certificate'),
        ('birth', 'Birth Certificate'),
        ('death', 'Death Certificate'),
        ('bonafide', 'Bonafide Certificate'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates')
    certificate_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    applicant_name = models.CharField(max_length=200)
    father_name = models.CharField(max_length=200)
    address = models.TextField()
    purpose = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    application_number = models.CharField(max_length=50, unique=True)
    document = models.FileField(upload_to='certificates/documents/', blank=True, null=True)
    remarks = models.TextField(blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_certificates')
    approved_date = models.DateTimeField(null=True, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    digital_signature = models.ImageField(upload_to='certificates/signatures/', blank=True, null=True)
    verification_status = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.application_number} - {self.get_certificate_type_display()}"
