# 📘 Smart Gram Panchayat Digital Governance System (SGPDGS)

## 🚀 Django + PostgreSQL + Bootstrap 5

### Features
- ✅ Complaint Management System
- ✅ Certificate Management
- ✅ Budget Transparency Dashboard
- ✅ Public Notices System
- ✅ Role-Based Access Control
- ✅ Fully Responsive Design
- ✅ Modern Indian Theme

### Installation

1. **Create Virtual Environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup Environment**
```bash
copy .env.example .env
# Edit .env with your database credentials
```

4. **Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create Superuser**
```bash
python manage.py createsuperuser
```

6. **Run Server**
```bash
python manage.py runserver
```

Visit: http://localhost:8000

### Tech Stack
- Django 5.0
- PostgreSQL
- Bootstrap 5
- Chart.js
- Font Awesome

### Roles
- Administrator
- District Admin
- Block Officer
- Sarpanch
- Panchayat Secretary
- Accountant
- Citizen
