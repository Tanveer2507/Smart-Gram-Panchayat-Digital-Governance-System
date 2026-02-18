@echo off
color 0A
cls
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║   🔐 SGPDGS - LOGIN CREDENTIALS                           ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo 🌐 SERVER URL:
echo    http://localhost:1000
echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo 👑 ADMIN LOGIN:
echo.
echo    URL: http://localhost:1000/admin-login/
echo.
echo    Username: administrator
echo    Password: administrator@123
echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo 👥 CITIZEN LOGIN:
echo.
echo    URL: http://localhost:1000/login/
echo.
echo    Note: Citizens need to register first
echo    Registration: http://localhost:1000/register/
echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo ✅ Press any key to open admin login page...
pause >nul
start http://localhost:1000/admin-login/
