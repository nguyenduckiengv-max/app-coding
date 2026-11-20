@echo off
title Bi Kip Luyen Rong Judge - Server Launcher
cd /d "%~dp0"

echo ===================================================
echo   DANG KHOI DONG HE THONG BI KIP LUYEN RONG JUDGE
echo ===================================================
echo Đang mở trình duyệt web tại: http://localhost:5000
echo Để tắt server: Hãy đóng cửa sổ này (hoặc bấm Ctrl + C).
echo.

start "" "http://localhost:5000"
python app.py
pause
