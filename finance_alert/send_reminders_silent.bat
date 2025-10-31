@echo off
REM Silent Daily Reminder Script - Runs without showing console window
REM Use this version for Task Scheduler to run quietly in background

cd /d "%~dp0finance_alert"

REM Activate virtual environment and run command
call "..\..venv\Scripts\activate.bat" && python manage.py send_daily_reminders >> ..\reminder_execution.log 2>&1

REM Log timestamp
echo Reminder sent at %date% %time% >> ..\reminder_execution.log
