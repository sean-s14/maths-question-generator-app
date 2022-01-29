from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test

# Mine
from .forms import CustomUserCreationForm, CustomUserLoginForm

# Sendgrid
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token

UserModel = get_user_model()


@user_passes_test(lambda user: user.is_anonymous, login_url='/', redirect_field_name=None)
def signup_view(request):

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            token = account_activation_token.make_token(user)
            email = form.cleaned_data.get('email')

            current_site = get_current_site(request)
            html_content = render_to_string('custom_auth/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
            })

            message = Mail(
                from_email=settings.DEFAULT_FROM_EMAIL,
                to_emails=email,
                subject='Confirmation e-mail for Maths Question Generator',
                html_content=html_content
            )

            try:
                sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                response = sg.send(message)
            except Exception as e:
                print(e)
                
            messages.info(request, f'A confirmation email has been sent to {email}. Please confirm before trying to log in to your account.')
            return redirect('custom_auth:login')
        else:
            print('Form is NOT valid...')
    else:
        form = CustomUserCreationForm()

    context = {'form': form, 'active': 'signup'}
    return render(request, 'custom_auth/signup.html', context)


def activate(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])

        messages.success(request, 'Email has been verified!')
    else:
        messages.error(request, 'Activation link is invalid')

    return redirect('generator:home')


@user_passes_test(lambda user: user.is_anonymous, login_url='/', redirect_field_name=None)
def login_view(request):

    if request.method == 'POST':
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = None
            try:
                email = validate_email(username)
            except ValidationError as e:
                print("Bad Email:", e)

            password = form.cleaned_data.get('password')

            user = authenticate(email=email, username=username, password=password)
            if user is not None:
                login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
                username = request.user
                messages.success(request, f'Logged in as {username}')
                return redirect('generator:home')
            else:
                # Check if user is active. If not then redirect to login page with message.
                user = None
                try:
                    user = UserModel.objects.get(username=username)
                except UserModel.DoesNotExist as e:
                    print('user does not exist...')
                
                if user.is_active:
                    print('User is active. Something went wrong.')
                else:  # User is not active
                    messages.error(request,'You must verify your email address before logging in to your account')
                    return redirect('custom_auth:login')

                print('User:', user, user.is_active)
                print('User is none...')
        else:
            print('Form is not valid...')

    else:
        form = CustomUserLoginForm()


    context = {'form': form, 'active': 'login'}
    return render(request, 'custom_auth/login.html', context)


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('generator:home')