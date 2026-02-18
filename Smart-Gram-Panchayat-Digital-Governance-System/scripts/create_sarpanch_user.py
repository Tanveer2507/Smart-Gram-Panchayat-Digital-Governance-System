import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sgpdgs.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import UserRole

# Create Sarpanch user if not exists
sarpanch_username = 'sarpanch_ramesh'
sarpanch_email = 'sarpanch@village.gov.in'
sarpanch_password = 'Sarpanch@2026'

if not User.objects.filter(username=sarpanch_username).exists():
    sarpanch_user = User.objects.create_user(
        username=sarpanch_username,
        email=sarpanch_email,
        password=sarpanch_password
    )
    sarpanch_user.first_name = 'Ramesh'
    sarpanch_user.last_name = 'Kumar'
    sarpanch_user.save()
    
    # Create sarpanch role
    UserRole.objects.create(
        user=sarpanch_user,
        role='sarpanch',
        phone='9876543210',
        village='Rampur',
        address='Village Office, Rampur'
    )
    
    print('✅ Sarpanch user created successfully!')
    print(f'Username: {sarpanch_username}')
    print(f'Password: {sarpanch_password}')
    print(f'Email: {sarpanch_email}')
else:
    print('⚠️ Sarpanch user already exists')
    print(f'Username: {sarpanch_username}')
    print(f'Password: {sarpanch_password}')
