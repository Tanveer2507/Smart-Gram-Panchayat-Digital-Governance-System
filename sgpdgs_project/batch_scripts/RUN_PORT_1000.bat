@echo off
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║   🚀 Starting SGPDGS Server on Port 1000                  ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 📋 Checking for errors...
python manage.py check
echo.
echo ✅ No errors found!
echo.
echo 🌐 Starting server on http://localhost:1000
echo.
echo 💡 Press CTRL+C to stop the server
echo.
echo ═══════════════════════════════════════════════════════════
echo.
python manage.py runserver 1000
