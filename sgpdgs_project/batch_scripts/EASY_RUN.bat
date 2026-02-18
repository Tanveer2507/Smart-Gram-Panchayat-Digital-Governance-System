@echo off
cls
color 0A
echo.
echo ========================================
echo   SGPDGS - Easy Setup and Run
echo ========================================
echo.

echo [Step 1/5] Installing packages...
pip install Django Pillow django-crispy-forms crispy-bootstrap5 python-decouple whitenoise

echo.
echo [Step 2/5] Creating database tables...
python manage.py makemigrations core complaints certificates budget notices
python manage.py migrate

echo.
echo [Step 3/5] Creating admin user...
python create_admin.py

echo.
echo [Step 4/5] Loading sample data...
python load_sample_data.py

echo.
echo [Step 5/5] Starting server...
echo.
echo ========================================
echo   SERVER RUNNING!
echo ========================================
echo.
echo   Open your browser and visit:
echo   http://localhost:8000
echo.
echo   Admin Panel:
echo   http://localhost:8000/admin
echo   Username: admin
echo   Password: admin123
echo.
echo   Press CTRL+C to stop server
echo ========================================
echo.

python manage.py runserver

pause
