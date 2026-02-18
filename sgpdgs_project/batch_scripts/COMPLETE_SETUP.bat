@echo off
cls
color 0A
title SGPDGS - Complete Setup

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║                                                        ║
echo ║     SGPDGS - Complete Setup Script                    ║
echo ║                                                        ║
echo ╚════════════════════════════════════════════════════════╝
echo.

echo [Step 1/6] Installing Python packages...
pip install Django Pillow django-crispy-forms crispy-bootstrap5 python-decouple whitenoise --quiet

echo.
echo [Step 2/6] Creating migrations...
python manage.py makemigrations core complaints certificates budget notices

echo.
echo [Step 3/6] Applying all migrations...
python manage.py migrate

echo.
echo [Step 4/6] Creating admin user...
python create_admin.py

echo.
echo [Step 5/6] Loading sample data...
python load_sample_data.py

echo.
echo [Step 6/6] Starting development server...
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║              🎉 SERVER IS RUNNING! 🎉                  ║
echo ╠════════════════════════════════════════════════════════╣
echo ║                                                        ║
echo ║  🌐 Website:  http://localhost:8000                    ║
echo ║  🔐 Admin:    http://localhost:8000/admin              ║
echo ║                                                        ║
echo ║  👤 Username: admin                                    ║
echo ║  🔑 Password: admin123                                 ║
echo ║                                                        ║
echo ║  📊 Sample Data Loaded:                                ║
echo ║     - 4 Complaints                                     ║
echo ║     - 3 Certificates                                   ║
echo ║     - 5 Budget Records                                 ║
echo ║     - 4 Public Notices                                 ║
echo ║                                                        ║
echo ║  ⚠️  Press CTRL+C to stop server                       ║
echo ║                                                        ║
echo ╚════════════════════════════════════════════════════════╝
echo.

python manage.py runserver

pause
