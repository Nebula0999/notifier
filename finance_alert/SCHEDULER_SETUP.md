# Daily Reminder Scheduler Setup

This folder contains scripts to automatically send daily contribution reminders at 8 PM and 9 PM.

## Files Created

- **send_reminders.bat** - Manual batch script (shows console output)
- **send_reminders_silent.bat** - Silent batch script for Task Scheduler
- **task_8pm.xml** - Task Scheduler configuration for 8 PM
- **task_9pm.xml** - Task Scheduler configuration for 9 PM
- **reminder_execution.log** - Auto-generated log file

## Setup Instructions

### Method 1: Import Pre-configured Tasks (Easiest)

1. **Open Task Scheduler**
   - Press `Win + R`, type `taskschd.msc`, press Enter

2. **Import 8 PM Task**
   - Right-click "Task Scheduler Library" → "Import Task..."
   - Navigate to: `C:\Users\Allan N\OneDrive\Desktop\python_introduction\notifier\task_8pm.xml`
   - Click "Open"
   - Review settings and click "OK"
   - Enter your Windows password if prompted

3. **Import 9 PM Task**
   - Repeat step 2 with `task_9pm.xml`

4. **Verify Tasks**
   - You should see two tasks: "Daily Reminders 8PM" and "Daily Reminders 9PM"
   - Right-click each → "Run" to test immediately

### Method 2: PowerShell Import (Quick)

Run these commands in PowerShell as Administrator:

```powershell
# Navigate to the folder
cd "C:\Users\Allan N\OneDrive\Desktop\python_introduction\notifier"

# Import both tasks
Register-ScheduledTask -Xml (Get-Content task_8pm.xml | Out-String) -TaskName "Daily Reminders 8PM"
Register-ScheduledTask -Xml (Get-Content task_9pm.xml | Out-String) -TaskName "Daily Reminders 9PM"

# Verify
Get-ScheduledTask | Where-Object {$_.TaskName -like "*Daily Reminders*"}
```

### Method 3: Manual Setup (Full Control)

1. Open Task Scheduler (`taskschd.msc`)
2. Click "Create Basic Task..." in the Actions panel
3. Configure as follows:

**For 8 PM Task:**
- Name: `Daily Reminders 8PM`
- Description: `Send contribution balance reminders`
- Trigger: Daily, at 8:00 PM
- Action: Start a program
  - Program: `C:\Users\Allan N\OneDrive\Desktop\python_introduction\notifier\send_reminders_silent.bat`
  - Start in: `C:\Users\Allan N\OneDrive\Desktop\python_introduction\notifier`

**For 9 PM Task:**
- Same as above, but trigger at 9:00 PM

## Testing

### Test the batch script manually:
```powershell
cd "C:\Users\Allan N\OneDrive\Desktop\python_introduction\notifier"
.\send_reminders.bat
```

### Test a specific member only:
Edit `send_reminders.bat` and change:
```batch
python manage.py send_daily_reminders
```
to:
```batch
python manage.py send_daily_reminders --only Allan --override-email "alijunior072@gmail.com"
```

### Dry-run (preview without sending):
```batch
python manage.py send_daily_reminders --dry-run
```

## Important Settings

Before the tasks run, ensure:

1. **Environment Variables** in `.env`:
   ```
   SULTAN_EMAIL=sultan@example.com
   BLESSING_EMAIL=blessing@example.com
   CYNTHIA_EMAIL=cynthia@example.com
   ALLAN_EMAIL=allan@example.com
   ```

2. **SMTP Settings** are configured (Gmail, Outlook, etc.)

3. **Google Sheets credentials** are valid

## Monitoring

- **View logs**: Check `reminder_execution.log`
- **Database logs**: Visit `http://localhost:8000/reminder-logs/` or Django Admin
- **Task History**: Task Scheduler → Select task → "History" tab

## Troubleshooting

### Task doesn't run:
- Check Task Scheduler → Task History for errors
- Ensure "Run whether user is logged on or not" is NOT checked (use default)
- Verify the batch file path is correct

### Emails not sending:
- Run `python manage.py send_test_email your@email.com` to verify SMTP
- Check `reminder_execution.log` for error messages
- View logs at `/reminder-logs/` in the web interface

### Need to change time:
- Open Task Scheduler → Right-click task → Properties → Triggers → Edit

## Disabling Tasks

To temporarily stop reminders:
1. Open Task Scheduler
2. Right-click task → Disable

To remove completely:
1. Right-click task → Delete

## Advanced: Wake Computer to Send

If you want the computer to wake from sleep to send reminders:

1. Task Scheduler → Select task → Properties
2. Conditions tab → Check "Wake the computer to run this task"
3. Settings tab → "Allow task to be run on demand"
