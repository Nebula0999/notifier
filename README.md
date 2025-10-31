# Finance Alert - Notifier System

A Django-based notification system that fetches financial data from Google Sheets and sends alerts to users. Features include complete user authentication with email verification, password reset, and a responsive Bootstrap UI.

## 🚀 Features

### User Authentication System
- **User Registration** with email verification
  - Custom user model extending Django's AbstractUser
  - Token-based email activation
  - Resend activation email functionality
  
- **Login System**
  - Support for login with email OR username
  - Custom authentication backend
  - Password reset flow with email
  - "Forgot password" functionality
  
- **Security Features**
  - Email verification required before account activation
  - Secure password hashing
  - CSRF protection
  - Django's built-in password validators

### Google Sheets Integration
- Service account authentication with Google Sheets API
- Real-time data fetching from Google Sheets
- Display financial data in a responsive grid layout
- Image proxy for secure image loading from Google sources

### Email System
- Development: Console backend for testing
- Production: SMTP backend configuration ready
- Uses Django Sites framework for proper domain handling in emails
- Configurable via environment variables

### UI/UX
- Bootstrap 5 responsive design
- Mobile-friendly navigation
- Flash messages for user feedback
- Consistent layout across all pages
- Card-based form layouts

## 📋 Prerequisites

- Python 3.10+
- PostgreSQL database
- Google Cloud service account with Sheets API enabled
- SMTP server credentials (for production email)

## 🛠️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/Nebula0999/notifier.git
cd notifier/finance_alert
```

### 2. Create virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the `finance_alert` directory with:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ENVIRONMENT=development

# Database (PostgreSQL)
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Google Sheets API (Service Account)
TYPE=service_account
PROJECT_ID=your-project-id
PRIVATE_KEY_ID=your-private-key-id
PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
CLIENT_EMAIL=your-service-account@project.iam.gserviceaccount.com
CLIENT_ID=your-client-id
AUTH_URI=https://accounts.google.com/o/oauth2/auth
TOKEN_URI=https://oauth2.googleapis.com/token
AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/...
UNIVERSE_DOMAIN=googleapis.com

# Email Configuration (for production)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Sites Framework
SITE_ID=1
```

### 5. Database Setup
```bash
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Configure Django Site
1. Start the development server: `python manage.py runserver`
2. Go to http://127.0.0.1:8000/admin/
3. Navigate to Sites → Select "example.com" (ID=1)
4. Update:
   - Domain: `localhost:8000` (dev) or `yourdomain.com` (prod)
   - Display name: `Finance Alert`

### 8. Google Sheets Setup
1. Create a Google Cloud project
2. Enable Google Sheets API
3. Create a service account and download JSON credentials
4. Share your Google Sheet with the service account email (viewer or editor access)
5. Copy credentials to your `.env` file

## 🚦 Running the Application

### Development Server
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/

### Key URLs
- **Home/Data Wall**: http://127.0.0.1:8000/
- **Sign Up**: http://127.0.0.1:8000/users/signup/
- **Login**: http://127.0.0.1:8000/users/login/
- **Profile**: http://127.0.0.1:8000/users/profile/
- **Password Reset**: http://127.0.0.1:8000/users/password-reset/
- **Resend Activation**: http://127.0.0.1:8000/users/resend-activation/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 📁 Project Structure

```
finance_alert/
├── finance_alert/          # Project settings
│   ├── settings.py        # Main configuration
│   ├── urls.py           # Root URL routing
│   └── wsgi.py           # WSGI configuration
├── users/                 # User authentication app
│   ├── backends.py       # Custom auth backend (email/username)
│   ├── forms.py          # Registration and login forms
│   ├── models.py         # Custom User model
│   ├── views.py          # Auth views
│   ├── urls.py           # User URL patterns
│   └── templates/users/  # User-related templates
├── notifier/              # Main app for notifications
│   ├── services.py       # Google Sheets integration
│   ├── views.py          # Data display views
│   └── templates/        # Notifier templates
├── templates/layout/      # Base templates
│   └── base.html         # Bootstrap base layout
├── .env                   # Environment variables (not in git)
├── manage.py             # Django management script
└── requirements.txt      # Python dependencies
```

## 🔧 Key Technical Details

### Custom User Model
- Extends `AbstractUser` with additional `phone_number` field
- Set via `AUTH_USER_MODEL = 'users.User'`

### Authentication Backend
- Custom `EmailOrUsernameModelBackend` in `users/backends.py`
- Allows login with either email or username
- Case-insensitive matching

### Email Verification Flow
1. User registers → account created but `is_active=False`
2. Activation email sent with token link
3. User clicks link → account activated and auto-logged in
4. Token uses Django's `default_token_generator` (secure, one-time use)

### Google Sheets Integration
- Lazy client initialization (avoids circular imports)
- Service account authentication via `gspread`
- Handles escaped newlines in private keys from env vars
- Caches gspread client for performance

### Image Proxy
- Server-side proxy at `/proxy-image/` 
- Solves CORS and authentication issues with external images
- Adds caching headers

## 🔐 Security Best Practices Implemented

- ✅ CSRF protection enabled
- ✅ Passwords hashed with Django's default hasher
- ✅ Email verification before account activation
- ✅ Service account credentials in environment variables (never committed)
- ✅ Sites framework for proper domain handling
- ✅ Token-based password reset
- ✅ SQL injection protection (Django ORM)
- ✅ XSS protection (Django template auto-escaping)

## 📧 Email Configuration

### Development
Emails print to console by default when `ENVIRONMENT != 'development'`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### Production
Set `ENVIRONMENT=development` in `.env` and configure SMTP:
- Gmail: Use app-specific password
- SendGrid, Mailgun, AWS SES: Configure per provider docs

## 🐛 Troubleshooting

### "relation django_site does not exist"
Run: `python manage.py migrate sites`

### Activation emails not sending
- Check EMAIL_BACKEND in settings
- Verify SMTP credentials
- Check console output in development

### Google Sheets access denied
- Verify service account email has access to the sheet
- Check credentials in `.env`
- Ensure PRIVATE_KEY newlines are properly escaped

### Images not loading
- Check proxy URL is accessible
- Verify Google Sheet image URLs are public or accessible
- Check browser console for errors

## 🚀 Deployment to Render

This project is ready for deployment to Render's free tier!

### Quick Deploy

1. **Push to GitHub:**
```bash
git add .
git commit -m "Deploy to Render"
git push
```

2. **Deploy on Render:**
   - Go to [render.com](https://render.com) and sign up
   - Click "New +" → "Blueprint"
   - Connect repository: `Nebula0999/notifier`
   - Click "Apply" - Render will use `render.yaml`

3. **Configure Environment Variables:**
   - Add Google Sheets credentials
   - Add email SMTP settings
   - Update `ALLOWED_HOSTS` with your Render URL

4. **Update Django Site:**
   - Visit `/admin/` and update Site domain

**Full deployment guide:** See `RENDER_DEPLOYMENT.md`

### Production Features

✅ Gunicorn WSGI server
✅ WhiteNoise for static files
✅ PostgreSQL database (Render-provided)
✅ SSL/HTTPS enabled by default
✅ Security headers configured
✅ Environment-based settings
✅ Auto-migrations on deploy
✅ Static files auto-collected

### Files for Deployment

- `requirements.txt` - Python dependencies
- `build.sh` - Render build script
- `render.yaml` - Render configuration
- `.python-version` - Python version specification
- `.env.example` - Environment variable template

## 📚 Tech Stack

- **Backend**: Django 5.1+
- **Database**: PostgreSQL
- **Authentication**: Django Auth + Custom Backend
- **Frontend**: Bootstrap 5, HTML5
- **APIs**: Google Sheets API (via gspread)
- **Email**: Django Email + SMTP
- **Python Libraries**: 
  - gspread
  - google-auth
  - django-environ
  - python-dotenv
  - psycopg2

## ⏰ Automated Daily Reminders

The system includes automated scheduled reminders at 8 PM and 9 PM daily.

### Setup (Windows Task Scheduler)

**Quick Setup:**
```powershell
cd "C:\Users\Allan N\OneDrive\Desktop\python_introduction\notifier"
Register-ScheduledTask -Xml (Get-Content task_8pm.xml | Out-String) -TaskName "Daily Reminders 8PM"
Register-ScheduledTask -Xml (Get-Content task_9pm.xml | Out-String) -TaskName "Daily Reminders 9PM"
```

**Manual Testing:**
```bash
python manage.py send_daily_reminders --dry-run
python manage.py send_daily_reminders --only Allan --override-email "test@example.com"
```

**View Reminder Logs:**
- Web UI: `http://localhost:8000/reminder-logs/`
- Django Admin: Admin panel → Reminder Logs
- File: `reminder_execution.log`

### Features
- ✅ Sends personalized balance summaries to each member
- ✅ Logs every send attempt (success/failure) to database
- ✅ No email addresses stored (data protection)
- ✅ Group summary included in each email
- ✅ Configurable member emails via environment variables
- ✅ Automatic retry if network available

For detailed scheduler setup, see `SCHEDULER_SETUP.md`

## 🔄 Future Enhancements

- [ ] SMS notifications via Twilio
- [ ] Slack integration for alerts
- [ ] Dashboard with financial data charts
- [ ] User notification preferences
- [ ] Alert rules and thresholds configuration UI
- [ ] Multi-tenant support
- [ ] API endpoints (Django REST Framework)
- [ ] Real-time updates with WebSockets
- [ ] Docker containerization

## 👨‍💻 Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Shell Access
```bash
python manage.py shell
```

## 📄 License

This project is private and proprietary.

## 🙋 Support

For issues or questions, contact the development team or create an issue in the repository.

---

**Last Updated**: October 31, 2025
