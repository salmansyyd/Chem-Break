@echo off

REM Define variables
set INSTALL_LOG=installation_logs\install.log
set PYTHON_EXE=python.exe
set REQUIREMENTS_FILE=requirements.txt

REM Check if Python 3.10 is installed
%PYTHON_EXE% --version | findstr /i "3.10" >nul
if errorlevel 1 (
    echo Python 3.10 is not installed. Please install it and try again.
    echo Python 3.10 is required for this installation. >>%INSTALL_LOG%
    exit /b 1
)

REM Install required libraries
echo Installing required libraries...
pip install -r %REQUIREMENTS_FILE% >>%INSTALL_LOG% 2>&1

REM Check for errors during installation
if errorlevel 1 (
    echo An error occurred during installation. Please check %INSTALL_LOG% for more details.
    exit /b 1
)

echo Installation completed successfully. >>%INSTALL_LOG%
