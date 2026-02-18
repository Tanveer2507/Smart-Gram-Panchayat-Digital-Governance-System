@echo off
echo ========================================
echo  SGPDGS - First Time Setup
echo ========================================
echo.

echo [1/6] Creating Virtual Environment...
python -m venv venv

echo [2/6] Activating Virtual Environment...
call venv\Scripts\activate

echo [3/6] Installing Dependencies...
pip install -r requirements.txt

echo [4/6] Setting up Environment File...
if not exist .env (
    copy .env.example .env
    echo Please edit .env file with your database credentials!
    pause
)

echo [5/6] Running Migrations...
python manage.py makemigrations
python manage.py migrate

echo [6/6] Creating Superuser...
echo Please enter admin credentials:
python manage.py createsuperuser

echo.
echo ========================================
echo  Setup Complete!
echo  Run RUN_PROJECT.bat to start server
echo ========================================
pause
