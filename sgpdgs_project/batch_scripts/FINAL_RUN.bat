@echo off
cls
color 0A
title SGPDGS - Smart Gram Panchayat System

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║                                                        ║
echo ║     SGPDGS - Smart Gram Panchayat System              ║
echo ║                                                        ║
echo ╚════════════════════════════════════════════════════════╝
echo.

echo [1/4] Installing dependencies...
pip install Django Pillow django-crispy-forms crispy-bootstrap5 python-decouple whitenoise --quiet

echo [2/4] Setting up database...
python manage.py makemigrations core complaints certificates budget notices
python manage.py migrate

echo [3/4] Creating admin and loading data...
python create_admin.py
python load_sample_data.py

echo [4/4] Starting server...
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║                  SERVER RUNNING!                       ║
echo ╠════════════════════════════════════════════════════════╣
echo ║                                                        ║
echo ║  Website:  http://localhost:8000                       ║
echo ║  Admin:    http://localhost:8000/admin                 ║
echo ║                                                        ║
echo ║  Username: admin                                       ║
echo ║  Password: admin123                                    ║
echo ║                                                        ║
echo ║  Press CTRL+C to stop server                           ║
echo ║                                                        ║
echo ╚════════════════════════════════════════════════════════╝
echo.

python manage.py runserver

pause
