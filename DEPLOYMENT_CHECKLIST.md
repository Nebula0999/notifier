# Pre-Deployment Checklist

Use this checklist before deploying to Render.

## ✅ Repository Preparation

- [x] All code committed to GitHub
- [x] `.env` file in `.gitignore` (not committed)
- [x] `requirements.txt` created with all dependencies
- [x] `build.sh` script created for Render
- [x] `render.yaml` configuration file created
- [x] `.python-version` file specifies Python 3.13.3
- [x] Production settings configured in `settings.py`

## ✅ Django Configuration

- [x] `DEBUG=False` for production
- [x] `ALLOWED_HOSTS` configured via environment variable
- [x] Database supports `DATABASE_URL` (Render format)
- [x] Static files configured with WhiteNoise
- [x] Security headers enabled for production
- [x] CSRF and session cookies secured for HTTPS
- [x] Email backend configured for production

## 📋 Information You'll Need

Before deploying, gather these credentials:

### Google Sheets API
- [ ] Service account JSON file
- [ ] Extract each field: PROJECT_ID, PRIVATE_KEY, CLIENT_EMAIL, etc.
- [ ] Share your Google Sheet with service account email

### Email (SMTP) - Optional but recommended
- [ ] SMTP host (e.g., smtp.gmail.com)
- [ ] SMTP port (usually 587)
- [ ] Email username
- [ ] Email app password (not regular password!)
- [ ] Default FROM email address

### Member Emails
- [ ] Sultan's email
- [ ] Blessing's email
- [ ] Cynthia's email
- [ ] Allan's email

## 🚀 Deployment Steps

### 1. Create Render Account
- [ ] Sign up at [render.com](https://render.com)
- [ ] Connect GitHub account
- [ ] Authorize Render to access repositories

### 2. Deploy via Blueprint
- [ ] Click "New +" → "Blueprint"
- [ ] Select repository: `Nebula0999/notifier`
- [ ] Click "Apply"
- [ ] Wait for initial deployment

### 3. Configure Environment Variables
Go to Web Service → Environment and add:

- [ ] `ALLOWED_HOSTS` = your-app-name.onrender.com
- [ ] `TYPE` = service_account
- [ ] `PROJECT_ID` = (from Google)
- [ ] `PRIVATE_KEY_ID` = (from Google)
- [ ] `PRIVATE_KEY` = (from Google - keep \n characters)
- [ ] `CLIENT_EMAIL` = (from Google)
- [ ] `CLIENT_ID` = (from Google)
- [ ] `CLIENT_X509_CERT_URL` = (from Google)
- [ ] `EMAIL_HOST` = smtp.gmail.com (or your provider)
- [ ] `EMAIL_HOST_USER` = your email
- [ ] `EMAIL_HOST_PASSWORD` = app password
- [ ] `DEFAULT_FROM_EMAIL` = noreply@yourdomain.com
- [ ] `SULTAN_EMAIL` = sultan's email
- [ ] `BLESSING_EMAIL` = blessing's email
- [ ] `CYNTHIA_EMAIL` = cynthia's email
- [ ] `ALLAN_EMAIL` = allan's email

### 4. Post-Deployment
- [ ] Visit your app URL
- [ ] Create superuser via Render Shell
- [ ] Login to admin panel
- [ ] Update Django Site domain to match Render URL
- [ ] Test data wall (Google Sheets integration)
- [ ] Test user registration/login
- [ ] Test reminder logs page

### 5. Test Reminders (Optional)
Via Render Shell:
```bash
cd finance_alert
python manage.py send_daily_reminders --dry-run
python manage.py send_daily_reminders --only Allan --override-email "your@email.com"
```

## 🐛 Troubleshooting

If deployment fails:

1. **Check Build Logs**
   - Render Dashboard → Service → Logs
   - Look for Python/pip errors
   
2. **Check Runtime Logs**
   - Look for Django errors
   - Check database connection
   - Verify environment variables

3. **Common Issues:**
   - Missing environment variable → Add in Render
   - Static files not loading → Run collectstatic manually
   - Database errors → Check migrations ran
   - Google Sheets access denied → Share sheet with service account

## 📝 Post-Deployment Notes

### App URL
Your app will be at: `https://[your-service-name].onrender.com`

### Free Tier Limitations
- Spins down after 15 minutes inactivity
- First request takes ~30 seconds (cold start)
- 750 hours/month free
- No cron jobs (scheduled reminders won't work automatically)

### Scheduled Reminders
To enable daily reminders on free tier:
1. Use external cron service like [cron-job.org](https://cron-job.org)
2. Upgrade to paid Render plan ($7/month for cron)
3. Use GitHub Actions with scheduled workflow

## ✨ Success Indicators

Your deployment is successful when:
- [ ] Homepage loads without errors
- [ ] Admin panel accessible
- [ ] Data wall shows Google Sheets data
- [ ] User registration works
- [ ] Email verification works (if SMTP configured)
- [ ] Reminder logs page displays
- [ ] No errors in Render logs

## 📚 Documentation

- Full deployment guide: `RENDER_DEPLOYMENT.md`
- Render docs: [render.com/docs](https://render.com/docs)
- Django deployment: [docs.djangoproject.com](https://docs.djangoproject.com/en/5.1/howto/deployment/)

---

**Ready to deploy?** Follow `RENDER_DEPLOYMENT.md` for detailed step-by-step instructions!
