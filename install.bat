@echo off
setlocal
if exist "%~dp0release-version.txt" set /p PERFCOMPARATOR_VERSION=<"%~dp0release-version.txt"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1"
if errorlevel 1 (
    echo.
    echo L'installation a echoue. Copiez le message ci-dessus pour obtenir de l'aide.
    pause
    exit /b 1
)
exit /b 0
