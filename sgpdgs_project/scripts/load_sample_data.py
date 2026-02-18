import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sgpdgs.settings')
django.setup()

from django.contrib.auth.models import User
from complaints.models import Complaint
from certificates.models import Certificate
from budget.models import BudgetRecord
from notices.models import Notice
from core.models import UserRole

print('Loading sample data...')

# Get or create admin user
admin = User.objects.filter(username='admin').first()
if not admin:
    admin = User.objects.create_superuser('admin', 'admin@sgpdgs.gov.in', 'admin123')

# Create sample complaints
complaints_data = [
    {'title': 'Road Repair Needed', 'description': 'Main road has potholes', 'category': 'Roads', 'priority': 'high', 'status': 'submitted'},
    {'title': 'Water Supply Issue', 'description': 'No water supply for 3 days', 'category': 'Water', 'priority': 'high', 'status': 'in_progress'},
    {'title': 'Street Light Not Working', 'description': 'Street light broken near temple', 'category': 'Electricity', 'priority': 'medium', 'status': 'assigned'},
    {'title': 'Garbage Collection Delay', 'description': 'Garbage not collected for a week', 'category': 'Sanitation', 'priority': 'medium', 'status': 'completed'},
]

for data in complaints_data:
    if not Complaint.objects.filter(title=data['title']).exists():
        Complaint.objects.create(user=admin, **data)

# Create sample certificates
certificates_data = [
    {'certificate_type': 'income', 'applicant_name': 'Rajesh Kumar', 'father_name': 'Ram Kumar', 'address': 'Village Rampur', 'purpose': 'Bank Loan', 'status': 'approved', 'application_number': 'CERT12345678'},
    {'certificate_type': 'residence', 'applicant_name': 'Priya Sharma', 'father_name': 'Vijay Sharma', 'address': 'Village Shyampur', 'purpose': 'School Admission', 'status': 'under_review', 'application_number': 'CERT12345679'},
    {'certificate_type': 'caste', 'applicant_name': 'Amit Patel', 'father_name': 'Suresh Patel', 'address': 'Village Ganeshpur', 'purpose': 'Government Job', 'status': 'pending', 'application_number': 'CERT12345680'},
]

for data in certificates_data:
    if not Certificate.objects.filter(application_number=data['application_number']).exists():
        Certificate.objects.create(user=admin, **data)

# Create sample budget records
budget_data = [
    {'department': 'roads', 'title': 'Road Construction Project', 'description': 'Main village road construction', 'amount': 500000, 'allocated_amount': 500000, 'spent_amount': 350000, 'financial_year': '2025-26', 'month': 'January'},
    {'department': 'water', 'title': 'Water Pipeline Installation', 'description': 'New water pipeline for ward 3', 'amount': 300000, 'allocated_amount': 300000, 'spent_amount': 200000, 'financial_year': '2025-26', 'month': 'February'},
    {'department': 'education', 'title': 'School Building Repair', 'description': 'Primary school maintenance', 'amount': 150000, 'allocated_amount': 150000, 'spent_amount': 100000, 'financial_year': '2025-26', 'month': 'January'},
    {'department': 'health', 'title': 'Health Center Equipment', 'description': 'Medical equipment purchase', 'amount': 200000, 'allocated_amount': 200000, 'spent_amount': 150000, 'financial_year': '2025-26', 'month': 'February'},
    {'department': 'administration', 'title': 'Office Supplies', 'description': 'Panchayat office supplies', 'amount': 50000, 'allocated_amount': 50000, 'spent_amount': 30000, 'financial_year': '2025-26', 'month': 'January'},
]

for data in budget_data:
    if not BudgetRecord.objects.filter(title=data['title']).exists():
        BudgetRecord.objects.create(**data)

# Create sample notices
notices_data = [
    {'title': 'Gram Sabha Meeting', 'description': 'Monthly gram sabha meeting on 20th February', 'notice_type': 'meeting', 'is_urgent': True, 'published_date': date.today()},
    {'title': 'Road Construction Tender', 'description': 'Tender for village road construction work', 'notice_type': 'tender', 'is_urgent': False, 'published_date': date.today() - timedelta(days=2)},
    {'title': 'Water Supply Scheme', 'description': 'New water supply scheme launched for all households', 'notice_type': 'scheme', 'is_urgent': False, 'published_date': date.today() - timedelta(days=5)},
    {'title': 'Emergency: Water Disruption', 'description': 'Water supply will be disrupted tomorrow for maintenance', 'notice_type': 'emergency', 'is_urgent': True, 'published_date': date.today()},
]

for data in notices_data:
    if not Notice.objects.filter(title=data['title']).exists():
        Notice.objects.create(**data)

print('✅ Sample data loaded successfully!')
print(f'Complaints: {Complaint.objects.count()}')
print(f'Certificates: {Certificate.objects.count()}')
print(f'Budget Records: {BudgetRecord.objects.count()}')
print(f'Notices: {Notice.objects.count()}')
