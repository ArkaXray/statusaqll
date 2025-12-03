@echo off
REM AQI Iran - One-Click Installation Script (Windows)
REM نصب خودکار برای Windows

setlocal enabledelayedexpansion

cls
echo.
echo ================================================================================
echo           AQI Iran - One-Click Installation (Windows)
echo ================================================================================
echo.

REM بررسی Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.8+ first
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% found

REM بررسی pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip not found!
    pause
    exit /b 1
)
echo [OK] pip found

REM ایجاد دایرکتوری‌های لازم
echo.
echo [SETUP] Creating directories...
if not exist "logs" mkdir logs
if not exist "data" mkdir data
if not exist "data\backups" mkdir data\backups
echo [OK] Directories created

REM نصب dependencies
echo.
echo [INSTALL] Installing Python packages...
echo This may take a few minutes...
echo.
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install packages!
    pause
    exit /b 1
)
echo [OK] Packages installed successfully

REM بررسی فایل‌های ضروری
echo.
echo [CHECK] Verifying essential files...
for %%F in (config.py scraper.py scheduler.py api.py) do (
    if not exist "%%F" (
        echo [ERROR] Missing file: %%F
        pause
        exit /b 1
    )
)
echo [OK] All essential files found

REM نصب Playwright browsers
echo.
echo [INSTALL] Setting up Playwright browsers...
echo This will download ~300MB, please wait...
echo.
python -m playwright install chromium --quiet
if errorlevel 1 (
    echo [WARNING] Playwright setup had issues, but continuing...
)
echo [OK] Playwright ready

REM تست syntax
echo.
echo [TEST] Testing Python syntax...
python -m py_compile config.py scraper.py scheduler.py api.py >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Syntax error in Python files!
    pause
    exit /b 1
)
echo [OK] All Python files are valid

REM خلاصه
cls
echo.
echo ================================================================================
echo                       INSTALLATION SUCCESSFUL!
echo ================================================================================
echo.
echo [OK] AQI Iran is ready to use!
echo.
echo Usage:
echo   python run.py              - Interactive menu
echo   python scheduler.py         - Start scheduler (30-min interval)
echo   python api.py              - Start API server (port 5000)
echo.
echo Next steps:
echo   1. python run.py
echo   2. Select option 1 or 2
echo   3. Check http://localhost:5000/api/health
echo.
echo Documentation:
echo   - README.md              - فارسی راهنما
echo   - USAGE.md              - نحوه استفاده
echo   - RETRY_LOGIC.md        - توضیح Retry Logic
echo   - INSTALL_UBUNTU.md     - نصب بر Ubuntu/Linux
echo.
echo ================================================================================
echo.

REM پرسش برای اجرای برنامه
echo.
set /p choice="Start program now? (y/n): "
if /i "%choice%"=="y" (
    python run.py
) else (
    echo Setup complete! Run 'python run.py' to start.
)

pause
