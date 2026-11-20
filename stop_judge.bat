@echo off
title Tat Server Bi Kip Luyen Rong
echo Dang dung tien trinh server app.py tren cong 5000...

for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":5000" ^| findstr "LISTENING"') do (
    echo Tim thay tien trinh PID %%a tren port 5000, dang tat...
    taskkill /f /pid %%a >nul 2>&1
)

echo.
echo Da dung server thanh cong!
pause
