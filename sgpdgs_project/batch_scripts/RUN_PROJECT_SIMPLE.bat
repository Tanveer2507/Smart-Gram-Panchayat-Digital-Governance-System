@echo off
cls
echo ========================================
echo  SGPDGS - Starting Server
echo ========================================
echo.
echo Installing dependencies...
pip install Django==5.0.2 psycopg2-binary Pillow django-crispy-forms crispy-bootstrap5 python-decouple whitenoise gunicorn

echo.
echo Running migrations...
python manage.py makemigrations
python manage.py migrate

echo.
echo Creating admin user...
python create_admin.py

echo.
echo Loading sample data...
python load_sample_data.py

echo.
echo ========================================
echo  Server Starting...
echo  URL: http://localhost:8000
echo  Admin: http://localhost:8000/admin
echo  Username: admin
echo  Password: admin123
echo ========================================
echo.

python manage.py runserver

pause
