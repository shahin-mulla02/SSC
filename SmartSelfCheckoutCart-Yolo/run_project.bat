@echo off
cd /d %~dp0

REM Start Scanner (background)
start "" python scanner.py

REM Start Customer Dashboard
start "" python customer_dashboard.py

REM Start Manager Dashboard
start "" python ManagerDashboard.py

REM Open browser links
timeout /t 3 >nul
start http://127.0.0.1:5001
start http://127.0.0.1:5000

exit
