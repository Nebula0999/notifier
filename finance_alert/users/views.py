from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail

from .forms import SignUpForm, LoginForm

User = get_user_model()


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # send activation email
            subject = 'Activate your account'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            domain = Site.objects.get_current().domain
            activation_link = f"https://{domain}/users/activate/{uid}/{token}/"
            message = render_to_string('users/activation_email.txt', {
                'user': user,
                'domain': domain,
                'activation_link': activation_link,
            })
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            return render(request, 'users/activation_sent.html', {'email': user.email})
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'users/activation_complete.html')
    else:
        return render(request, 'users/activation_invalid.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('users:profile')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('users:login')


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    return render(request, 'users/profile.html')


def resend_activation_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            user = None
        if user and not user.is_active:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            domain = Site.objects.get_current().domain
            activation_link = f"https://{domain}/users/activate/{uid}/{token}/"
            subject = 'Activate your account'
            message = render_to_string('users/activation_email.txt', {
                'user': user,
                'domain': domain,
                'activation_link': activation_link,
            })
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        return render(request, 'users/activation_sent.html', {'email': email})
    return render(request, 'users/resend_activation.html')
from django.shortcuts import render

# Create your views here.
