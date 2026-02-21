# Smart Gram Panchayat Digital Governance System (SGPDGS)

A comprehensive digital governance system for Gram Panchayats (village councils) built with Django.

> **⚠️ Important**: This is a Django web application and **cannot be deployed on GitHub Pages**. Please use PythonAnywhere, Railway, or Render for deployment.

## 🚀 Deploy Your Website

To see this project live, follow these guides:

1. **PythonAnywhere** (Recommended - FREE): Read `PYTHONANYWHERE_DEPLOYMENT.md`
2. **Railway.app or Render**: Read `QUICK_DEPLOY.md`

**Your site will be live at**: `yourusername.pythonanywhere.com` (or similar)

## ✨ Features

- 📜 **Certificate Management**: Issue and manage various certificates
- 📝 **Complaint Management**: Track and resolve citizen complaints
- 💰 **Budget Management**: Monitor panchayat budgets
- 📢 **Notice Board**: Publish official notices
- 🔔 **Notification System**: Real-time notifications
- 👥 **User Management**: Role-based access (Admin, Citizen)

## 🛠️ Tech Stack

- **Backend**: Django (Python)
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Authentication**: Django built-in

## 📦 Local Installation

1. Clone the repository:
```bash
git clone https://github.com/Tanveer2507/Smart-Gram-Panchayat-Digital-Governance-System.git
cd Smart-Gram-Panchayat-Digital-Governance-System
```

2. Navigate to project:
```bash
cd sgpdgs_project
```

3. Install dependencies:
```bash
pip install -r ../requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Run server:
```bash
python manage.py runserver
```

7. Open browser: `http://localhost:8000`

## 🚀 Quick Start (Windows)

Use batch scripts:
- `SETUP_FIRST_TIME.bat` - First-time setup
- `EASY_RUN.bat` - Quick start
- `SHOW_CREDENTIALS.bat` - View credentials

## 📁 Project Structure

```
sgpdgs_project/
├── budget/          # Budget management
├── certificates/    # Certificate issuance
├── complaints/      # Complaint tracking
├── core/           # Core functionality
├── notices/        # Notice board
├── notifications/  # Notification system
├── static/         # CSS, JS, images
├── templates/      # HTML templates
└── sgpdgs/         # Settings
```

## 🌐 Deployment Options

### Option 1: PythonAnywhere (FREE - Recommended)

✅ Best for Django projects  
✅ Free forever  
✅ Easy setup  

**Guide**: `PYTHONANYWHERE_DEPLOYMENT.md`  
**URL**: `yourusername.pythonanywhere.com`

### Option 2: Railway.app or Render.com

**Guide**: `QUICK_DEPLOY.md`

## 📚 Documentation

- [Installation Guide](sgpdgs_project/docs/INSTALLATION.md)
- [Notification System](sgpdgs_project/docs/NOTIFICATION_SYSTEM_COMPLETE.md)
- [Testing Guide](sgpdgs_project/docs/TEST_ADMIN_SECTIONS.md)

## 🔐 Default Credentials

After setup:
- **Username**: admin
- **Password**: admin123

## ⚠️ Important Notes

- **NOT for GitHub Pages**: This requires a Python server
- **Production**: Change SECRET_KEY, set DEBUG=False
- **Database**: Use PostgreSQL for production

## 🤝 Contributing

Contributions welcome! Submit a Pull Request.

## 📄 License

MIT License

## 📞 Support

- Deployment help: Check `PYTHONANYWHERE_DEPLOYMENT.md`
- Issues: Open a GitHub issue
