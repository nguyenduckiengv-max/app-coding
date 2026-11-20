@echo off
title Cai dat Tu dong chay cung Windows
echo =======================================================
echo   CAI DAT AUTO-START CHO BI KIP LUYEN RONG JUDGE
echo =======================================================

set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "TARGET_SCRIPT=%~dp0start_hidden.vbs"
set "SHORTCUT_PATH=%STARTUP_FOLDER%\BiKipLuyenRongJudge.lnk"

echo Dang tao shortcut trong thu muc khoi dong Windows...
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%SHORTCUT_PATH%'); $s.TargetPath = '%TARGET_SCRIPT%'; $s.WorkingDirectory = '%~dp0'; $s.Save()"

if exist "%SHORTCUT_PATH%" (
    echo.
    echo [THANH CONG] Tu bay gio moi khi mo may tinh Windows, 
    echo he thong Luyen Code se tu dong khoi dong ngam!
    echo Ban chi can go http://localhost:5000 vao trinh duyet la dung duoc ngay.
) else (
    echo [LOI] Khong the tao shortcut tu dong.
)
pause
