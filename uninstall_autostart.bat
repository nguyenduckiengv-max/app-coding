@echo off
title Huy bo Tu dong chay cung Windows
set "SHORTCUT_PATH=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\BiKipLuyenRongJudge.lnk"

if exist "%SHORTCUT_PATH%" (
    del "%SHORTCUT_PATH%"
    echo [THANH CONG] Da huy che do tu dong khoi dong cung Windows.
) else (
    echo Khong tim thay shortcut khoi dong tu dong.
)
pause
