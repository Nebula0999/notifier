"""
WSGI config for finance_alert project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys

try:
    from django.core.wsgi import get_wsgi_application  # type: ignore[import]
except Exception:
    # Django is not available in this environment (e.g., editor linting); provide a stub that
    # raises a clear error if someone tries to run the WSGI app without Django installed.
    def get_wsgi_application():
        raise RuntimeError("Django is not installed; install Django to run the WSGI application.")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_alert.settings')

# Fail-fast: If Django takes too long to initialize, warn and proceed anyway
# (better than worker timeout). This helps diagnose blocking imports or DB queries.
import signal

'''def timeout_handler(signum, frame):
    print("WARNING: Django initialization taking >25s, possible blocking call.", file=sys.stderr)
    # Don't raise; let it proceed so we can at least see error logs

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(25)  # 25 seconds grace for cold start

try:
    application = get_wsgi_application()
finally:
    signal.alarm(0)  # Disable alarm after successful init'''
application = get_wsgi_application()
