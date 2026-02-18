@echo off
echo ========================================
echo   SETUP CERTIFICATES MODULE
echo ========================================
echo.
echo This will apply database migrations for the new certificate fields...
echo.
pause
echo.
echo Running migrations...
python manage.py makemigrations certificates
python manage.py migrate certificates
echo.
echo ========================================
echo   SETUP COMPLETE!
echo ========================================
echo.
echo You can now use the Manage Certificates module.
echo Run OPEN_MANAGE_CERTIFICATES.bat to access it.
echo.
pause
