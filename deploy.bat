@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo ======================================================
echo    Al-Aaqil Market - Auto Deploy to PythonAnywhere
echo ======================================================

set "MSG=%~1"
if "%MSG%"=="" set "MSG=Auto deploy update from local machine"

python deploy.py "%MSG%"

echo.
pause
