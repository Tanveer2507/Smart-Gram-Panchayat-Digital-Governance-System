@echo off
echo ========================================
echo  SGPDGS - Smart Gram Panchayat System
echo ========================================
echo.

echo [1/5] Activating Virtual Environment...
call venv\Scripts\activate

echo [2/5] Installing Dependencies...
pip install -r requirements.txt

echo [3/5] Running Migrations...
python manage.py makemigrations
python manage.py migrate

echo [4/5] Collecting Static Files...
python manage.py collectstatic --noinput

echo [5/5] Starting Development Server...
echo.
echo ========================================
echo  Server Starting at http://localhost:8000
echo  Press CTRL+C to stop the server
echo ========================================
echo.

python manage.py runserver

pause
