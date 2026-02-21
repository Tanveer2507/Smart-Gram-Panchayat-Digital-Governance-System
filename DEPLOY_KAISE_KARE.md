# 🚀 Apni Website Ko Live Kaise Karein (Hindi Guide)

## ⚠️ IMPORTANT: GitHub Pages Kaam Nahi Karega!

GitHub Pages sirf **static HTML files** dikha sakta hai. Aapka Django project ko **Python server** chahiye.

## ✅ Solution: PythonAnywhere Use Karein (100% FREE)

### Step 1: PythonAnywhere Account Banayein

1. Yahan jayein: https://www.pythonanywhere.com/registration/register/beginner/
2. **Username** choose karein (example: `tanveer2507`)
3. Email aur password dalein
4. "Create a Beginner account" click karein
5. Email verify karein

### Step 2: Bash Console Kholein

1. PythonAnywhere dashboard par jayein
2. **"Consoles"** tab click karein
3. **"Bash"** click karein (naya console khulega)

### Step 3: Code Upload Karein

Bash console mein yeh commands type karein:

```bash
# 1. Git se code download karein
git clone https://github.com/Tanveer2507/Smart-Gram-Panchayat-Digital-Governance-System.git

# 2. Project folder mein jayein
cd Smart-Gram-Panchayat-Digital-Governance-System/sgpdgs_project

# 3. Virtual environment banayein
python3.10 -m venv venv

# 4. Virtual environment activate karein
source venv/bin/activate

# 5. Dependencies install karein
pip install -r ../requirements.txt

# 6. Database setup karein
python manage.py migrate

# 7. Static files collect karein
python manage.py collectstatic --noinput

# 8. Admin user banayein
python manage.py createsuperuser
```

**Note**: Step 8 mein username aur password dalein (yaad rakhein!)

### Step 4: Web App Setup Karein

1. Dashboard par **"Web"** tab click karein
2. **"Add a new web app"** click karein
3. Domain name confirm karein (example: `tanveer2507.pythonanywhere.com`)
4. **"Manual configuration"** select karein
5. **Python 3.10** select karein
6. "Next" click karein

### Step 5: Web App Configure Karein

**A. Source Code Path Set Karein:**
- "Code" section mein jayein
- **Source code** field mein dalein:
  ```
  /home/YOURUSERNAME/Smart-Gram-Panchayat-Digital-Governance-System/sgpdgs_project
  ```
  (YOURUSERNAME ko apne username se replace karein)

**B. Virtual Environment Set Karein:**
- **Virtualenv** field mein dalein:
  ```
  /home/YOURUSERNAME/Smart-Gram-Panchayat-Digital-Governance-System/sgpdgs_project/venv
  ```

**C. WSGI File Edit Karein:**
1. "Code" section mein **WSGI configuration file** link click karein
2. **Sab kuch delete karein**
3. Yeh code paste karein:

```python
import os
import sys

# Path setup
path = '/home/YOURUSERNAME/Smart-Gram-Panchayat-Digital-Governance-System/sgpdgs_project'
if path not in sys.path:
    sys.path.append(path)

# Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'sgpdgs.settings'

# WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

4. **YOURUSERNAME** ko apne username se replace karein
5. **Save** karein (Ctrl+S ya top-right corner mein button)

**D. Static Files Setup:**
1. "Static files" section mein jayein
2. Naya entry add karein:
   - **URL**: `/static/`
   - **Directory**: `/home/YOURUSERNAME/Smart-Gram-Panchayat-Digital-Governance-System/sgpdgs_project/staticfiles`

3. Ek aur entry add karein:
   - **URL**: `/media/`
   - **Directory**: `/home/YOURUSERNAME/Smart-Gram-Panchayat-Digital-Governance-System/sgpdgs_project/media`

### Step 6: Settings.py Update Karein

1. Bash console mein jayein
2. Yeh command run karein:

```bash
cd ~/Smart-Gram-Panchayat-Digital-Governance-System/sgpdgs_project
nano sgpdgs/settings.py
```

3. **ALLOWED_HOSTS** line ko dhundein aur aise change karein:

```python
ALLOWED_HOSTS = ['tanveer2507.pythonanywhere.com', 'localhost', '127.0.0.1']
```
(Apna username use karein)

4. Save karein: **Ctrl+O**, **Enter**, phir **Ctrl+X**

### Step 7: Website Start Karein

1. Web tab par wapas jayein
2. Top par **green "Reload" button** click karein
3. 30 seconds wait karein

### Step 8: Website Dekho! 🎉

Apna browser kholein aur jayein:
```
https://tanveer2507.pythonanywhere.com
```
(Apna username use karein)

## 🔐 Login Credentials

- **Admin Panel**: `https://tanveer2507.pythonanywhere.com/admin/`
- **Username**: Jo aapne Step 3.8 mein banaya
- **Password**: Jo aapne Step 3.8 mein banaya

## ❌ GitHub Pages Ko Disable Karein

Ab GitHub Pages ki zarurat nahi hai:

1. GitHub repository settings mein jayein
2. **Pages** section mein jayein
3. **Source** dropdown mein **"None"** select karein
4. Save karein

## 🆘 Agar Problem Aaye

### Error: "Something went wrong"
- Web tab par **Error log** click karein
- Last 100 lines dekho
- Agar samajh na aaye to mujhe batayein

### Static Files Load Nahi Ho Rahe
```bash
cd ~/Smart-Gram-Panchayat-Digital-Governance-System/sgpdgs_project
source venv/bin/activate
python manage.py collectstatic --noinput
```
Phir web app reload karein

### Database Error
```bash
cd ~/Smart-Gram-Panchayat-Digital-Governance-System/sgpdgs_project
source venv/bin/activate
python manage.py migrate
```

## 📝 Important Notes

- **FREE account** mein daily ek baar website sleep mode mein jaati hai
- Subah 3 months baad renew karna padega (free hai)
- Agar website slow lage to reload karein

## 🎯 Summary

1. ✅ PythonAnywhere account banayein
2. ✅ Code upload karein (git clone)
3. ✅ Dependencies install karein
4. ✅ Web app configure karein
5. ✅ WSGI file edit karein
6. ✅ Settings.py update karein
7. ✅ Reload karein
8. ✅ Website live hai! 🚀

**Aapki website ab live hogi**: `https://YOURUSERNAME.pythonanywhere.com`

---

**Need Help?** Agar koi step samajh na aaye to mujhe batayein!
