# Money Mates - Daily Reminder Setup Guide

## Quick Start

### 1. Add Member Emails to .env
Add these lines to your `.env` file with actual email addresses:

```env
# Money Mates Member Emails
SULTAN_EMAIL=sultan@example.com
BLESSING_EMAIL=blessing@example.com
CYNTHIA_EMAIL=cynthia@example.com
ALLAN_EMAIL=allan@example.com
```

### 2. Test the Command (Dry Run)
```bash
python manage.py send_daily_reminders --dry-run
```

This will show what emails would be sent without actually sending them.

### 3. Send Actual Reminders
```bash
python manage.py send_daily_reminders
```

## Email Setup

### Development (Console Backend)
- Emails print to console
- Good for testing
- Already configured in settings.py

### Production (SMTP)
Update your `.env`:
```env
ENVIRONMENT=development
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
DEFAULT_FROM_EMAIL=moneymates@example.com
```

**For Gmail:**
1. Enable 2-factor authentication
2. Generate an app-specific password
3. Use that password in EMAIL_HOST_PASSWORD

## Scheduling Daily Reminders

### Option 1: Windows Task Scheduler
1. Open Task Scheduler
2. Create Basic Task
3. Name: "Money Mates Daily Reminder"
4. Trigger: Daily at 9:00 AM
5. Action: Start a program
   - Program: `C:\path\to\python.exe`
   - Arguments: `C:\path\to\manage.py send_daily_reminders`
   - Start in: `C:\path\to\finance_alert\`

### Option 2: Linux/Mac (cron)
Edit crontab:
```bash
crontab -e
```

Add line (runs daily at 9 AM):
```
0 9 * * * /path/to/venv/bin/python /path/to/manage.py send_daily_reminders
```

### Option 3: Heroku Scheduler (Cloud)
Add to your Heroku app:
```bash
heroku addons:create scheduler:standard
```

Add job:
```bash
python manage.py send_daily_reminders
```

Schedule: Daily at 9:00 AM

## SMS Reminders (Optional)

To add SMS via Twilio:

### 1. Install Twilio
```bash
pip install twilio
```

### 2. Add to .env
```env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# Member phone numbers
SULTAN_PHONE=+1234567890
BLESSING_PHONE=+1234567890
CYNTHIA_PHONE=+1234567890
ALLAN_PHONE=+1234567890
```

### 3. Update the command
Add SMS sending code to `send_daily_reminders.py` (I can help with this)

## Troubleshooting

### Emails not sending
1. Check ENVIRONMENT variable
2. Verify SMTP credentials
3. Check spam folder
4. Test with --dry-run first

### "No contribution data found"
1. Verify sheet name: "money mates tracker"
2. Verify tab name: "daily log"
3. Check service account has access

### Command not found
```bash
python manage.py help
```
Should list `send_daily_reminders`

## Testing

### Test with one email
Temporarily set all emails to yours in .env:
```env
SULTAN_EMAIL=yourtest@email.com
BLESSING_EMAIL=yourtest@email.com
CYNTHIA_EMAIL=yourtest@email.com
ALLAN_EMAIL=yourtest@email.com
```

Run: `python manage.py send_daily_reminders`

You should receive 4 emails.
