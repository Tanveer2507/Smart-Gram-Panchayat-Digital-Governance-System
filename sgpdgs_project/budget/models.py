from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class BudgetRecord(models.Model):
    DEPARTMENT_CHOICES = [
        ('roads', 'Roads & Infrastructure'),
        ('water', 'Water Supply'),
        ('education', 'Education'),
        ('health', 'Health'),
        ('administration', 'Administration'),
        ('sanitation', 'Sanitation'),
        ('agriculture', 'Agriculture'),
        ('welfare', 'Social Welfare'),
    ]
    
    STATUS_CHOICES = [
        ('on_track', 'On Track'),
        ('near_limit', 'Near Limit'),
        ('over_budget', 'Over Budget'),
    ]
    
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    allocated_amount = models.DecimalField(max_digits=12, decimal_places=2)
    spent_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    financial_year = models.CharField(max_length=20)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='on_track')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_budgets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Legacy fields for backward compatibility
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    month = models.CharField(max_length=20, blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.department}"
    
    @property
    def remaining_amount(self):
        return self.allocated_amount - self.spent_amount
    
    @property
    def utilization_percentage(self):
        if self.allocated_amount > 0:
            return float((self.spent_amount / self.allocated_amount) * 100)
        return 0.0
    
    def update_status(self):
        """Auto-update status based on utilization"""
        percentage = self.utilization_percentage
        if percentage >= 100:
            self.status = 'over_budget'
        elif percentage >= 80:
            self.status = 'near_limit'
        else:
            self.status = 'on_track'
        self.save()


class ExpenseEntry(models.Model):
    CATEGORY_CHOICES = [
        ('materials', 'Materials'),
        ('labor', 'Labor'),
        ('equipment', 'Equipment'),
        ('services', 'Services'),
        ('utilities', 'Utilities'),
        ('maintenance', 'Maintenance'),
        ('other', 'Other'),
    ]
    
    budget = models.ForeignKey(BudgetRecord, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    date = models.DateField()
    receipt = models.FileField(upload_to='budget/receipts/', blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Expense Entries'
    
    def __str__(self):
        return f"{self.title} - ₹{self.amount}"
