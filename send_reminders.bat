@echo off
REM Daily Reminder Script - Sends contribution balance reminders to all members
REM This script activates the virtual environment and runs the Django management command

cd /d "%~dp0finance_alert"

REM Activate virtual environment
call "..\..venv\Scripts\activate.bat"

REM Run the reminder command
python manage.py send_daily_reminders

REM Log the execution
echo Reminder sent at %date% %time% >> ..\reminder_execution.log

pause
