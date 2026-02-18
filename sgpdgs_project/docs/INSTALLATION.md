# 🚀 SGPDGS Installation Guide

## Prerequisites
- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

## Step-by-Step Installation

### 1. Navigate to Project Directory
```bash
cd sgpdgs_project
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Setup Environment Variables
```bash
copy .env.example .env
```

Edit `.env` file with your database credentials:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_NAME=sgpdgs_db
DATABASE_USER=postgres
DATABASE_PASSWORD=your-password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

### 6. Create PostgreSQL Database
```sql
CREATE DATABASE sgpdgs_db;
```

### 7. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```
Enter username, email, and password when prompted.

### 9. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 10. Run Development Server
```bash
python manage.py runserver
```

### 11. Access Application
- **Frontend:** http://localhost:8000
- **Admin Panel:** http://localhost:8000/admin

## Default Login
Use the superuser credentials you created in Step 8.

## Troubleshooting

### Database Connection Error
- Ensure PostgreSQL is running
- Check database credentials in `.env`
- Verify database exists

### Module Not Found Error
```bash
pip install -r requirements.txt
```

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

## Production Deployment
For production, set `DEBUG=False` in `.env` and configure proper database and static file settings.

## Support
For issues, check the README.md file or contact support.
