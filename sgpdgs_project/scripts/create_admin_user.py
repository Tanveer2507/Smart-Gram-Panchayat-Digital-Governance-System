import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sgpdgs.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import UserRole

# Create admin user if not exists
admin_username = 'sgpdgs_admin'
admin_email = 'admin@sgpdgs.gov.in'
admin_password = 'Admin@SGPDGS2026'

if not User.objects.filter(username=admin_username).exists():
    admin_user = User.objects.create_superuser(
        username=admin_username,
        email=admin_email,
        password=admin_password
    )
    admin_user.first_name = 'SGPDGS'
    admin_user.last_name = 'Administrator'
    admin_user.save()
    
    # Create admin role
    UserRole.objects.create(
        user=admin_user,
        role='administrator',
        phone='1800-XXX-XXXX',
        village='District Office',
        address='Smart Gram Panchayat HQ'
    )
    
    print('✅ Admin user created successfully!')
    print(f'Username: {admin_username}')
    print(f'Password: {admin_password}')
    print(f'Email: {admin_email}')
else:
    print('⚠️ Admin user already exists')
    print(f'Username: {admin_username}')
    print(f'Password: {admin_password}')
