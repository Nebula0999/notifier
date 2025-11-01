# Setting Up Automated Daily Reminders with Cron-Job.org

This guide shows you how to schedule your daily contribution reminders at 8 PM and 9 PM using cron-job.org (free external scheduler) since Render's free tier doesn't support built-in cron jobs.

## 📋 Prerequisites

Before you start, make sure:
1. ✅ Your app is deployed on Render and accessible
2. ✅ The `/cron/send-reminders/` endpoint exists (already added)
3. ✅ Email (SMTP) is configured and working on Render
4. ✅ Member emails are set in Render environment variables

## 🔐 Step 1: Generate a Secret Token

Your cron endpoint is protected by a secret token to prevent unauthorized access.

**Generate a secure random token:**

### Option A: Online Generator
- Visit: https://www.uuidgenerator.net/
- Copy the generated UUID (e.g., `a1b2c3d4-e5f6-7890-abcd-ef1234567890`)

### Option B: PowerShell
```powershell
[guid]::NewGuid().ToString()
```

### Option C: Python
```python
import secrets
print(secrets.token_urlsafe(32))
```

**Save this token** - you'll need it for both Render and cron-job.org.

## 🔧 Step 2: Add Token to Render

1. Go to your Render Dashboard
2. Open your **Web Service** (finance-alert-web)
3. Go to **Environment** tab
4. Click **Add Environment Variable**
5. Add:
   - **Key:** `REMINDER_CRON_KEY`
   - **Value:** Your generated token (paste it)
6. Click **Save Changes**
7. Wait for the service to redeploy

## 🌐 Step 3: Set Up Cron-Job.org

### Create Account
1. Go to https://cron-job.org/en/
2. Click **Sign up** (it's free!)
3. Verify your email address
4. Log in to your dashboard

### Create First Job (8 PM Reminder)

1. Click **"Create cronjob"** button

2. **General Settings:**
   - **Title:** `Money Mates 8PM Reminder`
   - **Address (URL):**
     ```
     https://notifier-dpvz.onrender.com/cron/send-reminders/?key=YOUR_SECRET_TOKEN
     ```
     ⚠️ Replace `YOUR_SECRET_TOKEN` with the token from Step 1
     ⚠️ Replace `notifier-dpvz.onrender.com` with your actual Render URL

3. **Schedule:**
   - Select **"Every day"**
   - **Time:** `20:00` (8:00 PM)
   - **Timezone:** Select `Africa/Nairobi` or your local timezone

4. **Advanced Settings (Optional but Recommended):**
   - **Request method:** `GET` (default)
   - **Request timeout:** `30` seconds
   - **Execution:** Check "Execute even when computer is in standby"
   - **Notifications:** Enter your email to get alerts if it fails

5. Click **"Create cronjob"**

### Create Second Job (9 PM Reminder)

Repeat the process for 9 PM:

1. Click **"Create cronjob"** again

2. **General Settings:**
   - **Title:** `Money Mates 9PM Reminder`
   - **Address (URL):**
     ```
     https://notifier-dpvz.onrender.com/cron/send-reminders/?key=YOUR_SECRET_TOKEN
     ```

3. **Schedule:**
   - Select **"Every day"**
   - **Time:** `21:00` (9:00 PM)
   - **Timezone:** `Africa/Nairobi`

4. Click **"Create cronjob"**

## ✅ Step 4: Test Your Setup

### Test Now (Before Waiting Until 8 PM)

**Option A: Test via cron-job.org**
1. In your cron-job.org dashboard
2. Find your cronjob
3. Click the **"▶ Execute now"** button
4. Check the execution log - it should show HTTP 200 (success)

**Option B: Test via Browser**
1. Open your browser
2. Visit:
   ```
   https://notifier-dpvz.onrender.com/cron/send-reminders/?key=YOUR_SECRET_TOKEN
   ```
3. You should see: `{"ok": true}`

**Option C: Test with Dry-Run (No Emails Sent)**
```
https://notifier-dpvz.onrender.com/cron/send-reminders/?key=YOUR_SECRET_TOKEN&dry=1
```

### Check the Results

**1. Check Render Logs:**
   - Render Dashboard → Your service → **Logs** tab
   - Look for: `✓ Sent reminder to [member] at [email]`

**2. Check Reminder Logs in Your App:**
   - Visit: `https://notifier-dpvz.onrender.com/reminder-logs/`
   - You should see the sent reminders listed

**3. Check Email Inbox:**
   - Check all member emails for the reminder emails
   - Don't forget to check spam folders!

## 🔍 Advanced Options

### Send to Specific Members Only

Add `&only=Member1,Member2` to the URL:
```
https://notifier-dpvz.onrender.com/cron/send-reminders/?key=TOKEN&only=Allan,Blessing
```

### Test Without Sending Emails

Add `&dry=1` to preview what would be sent:
```
https://notifier-dpvz.onrender.com/cron/send-reminders/?key=TOKEN&dry=1
```

### Check Execution History

In cron-job.org dashboard:
1. Click on your cronjob
2. Go to **"History"** tab
3. See all executions, response codes, and timing

## 🐛 Troubleshooting

### "Unauthorized" Error (HTTP 401)
- Your `REMINDER_CRON_KEY` on Render doesn't match the `key` in the URL
- Double-check both values are exactly the same (no extra spaces)

### "Server not configured" Error (HTTP 500)
- `REMINDER_CRON_KEY` is not set on Render
- Go to Render → Environment and add it

### No Emails Being Sent (HTTP 200 but no emails)
1. Check SMTP settings on Render:
   - `ENVIRONMENT=production`
   - `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS=True`
   - `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`
2. Check member emails are set:
   - `ALLAN_EMAIL`, `BLESSING_EMAIL`, `CYNTHIA_EMAIL`, `SULTAN_EMAIL`
3. Check Render logs for SMTP errors

### Cronjob Shows Failed Execution
- Check the response code in cron-job.org history
- If 502/503: Your Render app might be sleeping (cold start)
  - Solution: Increase timeout in cron-job.org to 60 seconds
  - Or use a free uptime monitor (like UptimeRobot) to keep your app awake

### Cold Start Issues (Render Free Tier)
Render free tier apps sleep after 15 minutes of inactivity. Solutions:

**Option A: Increase Timeout**
- In cron-job.org, set **Request timeout** to 60 seconds
- First request wakes the app (takes ~30 seconds), then runs

**Option B: Keep App Awake**
- Use UptimeRobot (free) to ping your homepage every 5 minutes
- This prevents cold starts entirely

## 📊 Monitoring Best Practices

1. **Enable Email Notifications:**
   - In cron-job.org, add your email to get alerts on failures

2. **Check Weekly:**
   - Review cron-job.org execution history
   - Check `/reminder-logs/` in your app for patterns

3. **Set Up a Status Page:**
   - Consider a simple dashboard showing last successful run

## 🔒 Security Notes

- ✅ Never share your `REMINDER_CRON_KEY` token
- ✅ Don't commit it to Git (it's in environment variables only)
- ✅ Use a strong, random token (UUID or 32+ character random string)
- ✅ If token is compromised, generate a new one and update both Render and cron-job.org

## 💰 Cost Breakdown

- **Cron-Job.org:** Free (unlimited jobs)
- **Render Web Service:** Free tier (750 hours/month)
- **Render PostgreSQL:** Free tier (1GB storage)
- **Total:** $0/month 🎉

## 🚀 Alternative: Upgrade to Render Paid Plan

If you prefer not to use an external scheduler:

1. Upgrade to Render's **Starter Plan** ($7/month)
2. Add native Cron Jobs:
   - Schedule: `0 20 * * *` (8 PM)
   - Command: `cd finance_alert && python manage.py send_daily_reminders`
3. Benefit: No cold starts, runs directly on your server

## ✨ What Happens at 8 PM and 9 PM

1. Cron-job.org sends GET request to your endpoint
2. Your app validates the secret token
3. Django runs `send_daily_reminders` management command
4. Command fetches latest Google Sheets data
5. Sends personalized email to each member:
   - Current balance
   - Group summary
   - Status (deficit or good standing)
6. Logs each send (success/failure) to database
7. Returns success response to cron-job.org

---

## 📝 Quick Checklist

Before going live:
- [ ] Token generated and saved securely
- [ ] `REMINDER_CRON_KEY` added to Render environment
- [ ] Service redeployed on Render
- [ ] Both cron jobs created (8 PM and 9 PM)
- [ ] Timezone set correctly (Africa/Nairobi)
- [ ] Test execution successful
- [ ] Checked Render logs
- [ ] Confirmed emails received
- [ ] Email notifications enabled in cron-job.org

**You're all set!** 🎊 Your reminders will now send automatically every day at 8 PM and 9 PM.

---

**Need Help?**
- Cron-job.org Docs: https://cron-job.org/en/documentation/
- Your app logs: Render Dashboard → Your service → Logs
- Your reminder history: `https://notifier-dpvz.onrender.com/reminder-logs/`
