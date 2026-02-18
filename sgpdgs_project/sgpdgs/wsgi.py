import os
import sys

# Add the project directory to sys.path
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sgpdgs.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# Vercel requires 'app' variable
app = application
