"""
Vercel-compatible WSGI application wrapper
"""
import os
import sys
from pathlib import Path

# Add project to path
project_dir = Path(__file__).resolve().parent.parent
if str(project_dir) not in sys.path:
    sys.path.insert(0, str(project_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sgpdgs.settings')

# Import Django WSGI application
import django
django.setup()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Vercel handler
app = application
