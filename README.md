<<<<<<< HEAD
# Smart Gram Panchayat Digital Governance System (SGPDGS)

A comprehensive digital governance system for Gram Panchayats (village councils) built with Django.

## Features

- **Certificate Management**: Issue and manage various certificates (income, residence, caste, etc.)
- **Complaint Management**: Track and resolve citizen complaints
- **Budget Management**: Monitor and manage panchayat budgets
- **Notice Board**: Publish and manage official notices
- **Notification System**: Real-time notifications for users
- **User Management**: Role-based access control (Admin, Sarpanch, Citizens)

## Tech Stack

- **Backend**: Django (Python)
- **Database**: SQLite (development)
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Django built-in authentication

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sgpdgs-project.git
cd sgpdgs-project
```

2. Navigate to the project directory:
```bash
cd sgpdgs_project
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Quick Start (Windows)

Use the provided batch scripts for easy setup:

- `SETUP_FIRST_TIME.bat` - First-time setup
- `EASY_RUN.bat` - Quick start the server
- `SHOW_CREDENTIALS.bat` - Display default credentials

## Project Structure

```
sgpdgs_project/
├── budget/          # Budget management module
├── certificates/    # Certificate issuance module
├── complaints/      # Complaint tracking module
├── core/           # Core functionality and authentication
├── notices/        # Notice board module
├── notifications/  # Notification system
├── static/         # Static files (CSS, JS, images)
├── templates/      # HTML templates
└── sgpdgs/         # Project settings
```

## Documentation

For detailed documentation, see the `docs/` folder:
- [Installation Guide](sgpdgs_project/docs/INSTALLATION.md)
- [Notification System](sgpdgs_project/docs/NOTIFICATION_SYSTEM_COMPLETE.md)
- [Testing Guide](sgpdgs_project/docs/TEST_ADMIN_SECTIONS.md)

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
=======
# Smart-Gram-Panchayat-Digital-Governance-System
Smart-Gram-Panchayat-Digital-Governance-System
>>>>>>> 0435f5ed5a8e5ceb9ba1429c30530cd8d7044a68
