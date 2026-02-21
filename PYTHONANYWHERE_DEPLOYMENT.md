# PythonAnywhere Deployment Guide

## Why PythonAnywhere?
- ✅ Free tier available
- ✅ Django support built-in
- ✅ Easy to setup
- ✅ No credit card required
- ✅ Your website will be live at: `yourusername.pythonanywhere.com`

## Step-by-Step Deployment

### 1. Create Account
1. Go to https://www.pythonanywhere.com
2. Click "Start running Python online in less than a minute!"
3. Sign up for FREE "Beginner" account
4. Verify your email

### 2. Open Bash Console
1. After login, go to "Consoles" tab
2. Click "Bash" to open a new console

### 3. Clone Your Repository
```bash
git clone https://github.com/Tanveer2507/Smart-Gram-Panchayat-Digital-Governance-System.git
cd Smart-Gram-Panchayat-Digital-Governance-System/sgpdgs_project
```

### 4. Create Virtual Environment
```bash
mkvirtualenv --python=/usr/bin/python3.10 sgpdgs_env
```

### 5. Install Dependencies
```bash
pip install -r ../requirements.txt
```

### 6. Setup Database
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 7. Collect Static Files
```bash
python manage.py collectstatic
```

### 8. Configure Web App
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Select "Python 3.10"

### 9. Configure WSGI File
1. In "Web" tab, click on WSGI configuration file link
2. Delete all content and paste this:

```python
import os
import sys

# Add your project directory to the sys.path
project_home = '/home/yourusername/Smart-Gram-Panchayat-Digital-Governance-System/sgpdgs_project'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variable for Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'sgpdgs.settings'

# Activate virtual environment
activate_this = '/home/yourusername/.virtualenvs/sgpdgs_env/bin/activate_this.py'
with open(activate_this) as f:
    exec(f.read(), {'__file__': activate_this})

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Important**: Replace `yourusername` with your actual PythonAnywhere username!

### 10. Configure Static Files
In "Web" tab, add static files mapping:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/yourusername/Smart-Gram-Panchayat-Digital-Governance-System/sgpdgs_project/staticfiles` |
| `/media/` | `/home/yourusername/Smart-Gram-Panchayat-Digital-Governance-System/sgpdgs_project/media` |

### 11. Configure Virtual Environment
In "Web" tab, set virtualenv path:
```
/home/yourusername/.virtualenvs/sgpdgs_env
```

### 12. Update Settings
Edit settings.py to add your domain:
```bash
nano ~/Smart-Gram-Panchayat-Digital-Governance-System/sgpdgs_project/sgpdgs/settings.py
```

Update ALLOWED_HOSTS:
```python
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com', 'localhost', '127.0.0.1']
```

### 13. Reload Web App
1. Go to "Web" tab
2. Click green "Reload" button
3. Wait 30 seconds

### 14. Visit Your Site!
Your website is now live at:
- **Website**: `https://yourusername.pythonanywhere.com`
- **Admin**: `https://yourusername.pythonanywhere.com/admin/`

## Updating Your Site

When you make changes:

```bash
cd ~/Smart-Gram-Panchayat-Digital-Governance-System
git pull origin main
cd sgpdgs_project
python manage.py migrate
python manage.py collectstatic --noinput
```

Then reload web app from "Web" tab.

## Troubleshooting

### Error Logs
Check error logs in "Web" tab → "Log files" section

### Database Issues
```bash
cd ~/Smart-Gram-Panchayat-Digital-Governance-System/sgpdgs_project
python manage.py migrate
```

### Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
```

### Permission Errors
```bash
chmod -R 755 ~/Smart-Gram-Panchayat-Digital-Governance-System
```

## Free Tier Limitations

- ✅ 512 MB disk space
- ✅ 1 web app
- ✅ 100 seconds CPU time per day
- ⚠️ Site sleeps after 3 months of inactivity
- ⚠️ Custom domain not available (paid feature)

## Upgrade Options

If you need more:
- Custom domain: $5/month
- More CPU time: $5/month
- More disk space: $5/month

## Support

- Documentation: https://help.pythonanywhere.com
- Forums: https://www.pythonanywhere.com/forums/
- Email: support@pythonanywhere.com
