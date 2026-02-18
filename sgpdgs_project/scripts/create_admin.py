import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sgpdgs.settings')
django.setup()

from django.contrib.auth.models import User

# Create superuser if not exists
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@sgpdgs.gov.in', 'admin123')
    print('✅ Superuser created successfully!')
    print('Username: admin')
    print('Password: admin123')
else:
    print('⚠️ Admin user already exists')
