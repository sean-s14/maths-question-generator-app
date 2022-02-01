from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import check_password

# Mine
from .forms import (
    CustomUserCreationForm, 
    CustomUserLoginForm, 
    CustomUserEditForm,
    CustomUserDeleteForm,
)
from .send_email import send_email

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
            
            html_content = render_to_string('custom_auth/email/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
            })

            subject = 'Confirmation e-mail for Maths Question Generator'
            
            send_email(request, email, subject, html_content)
                
            message_content = render_to_string('custom_auth/email/resend_confirmation.html', {
                'email': email,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
            })

            messages.info(request, message_content)
            return redirect('custom_auth:login')
        else:
            print('Form is NOT valid...')
    else:
        form = CustomUserCreationForm()

    context = {'form': form, 'active': 'signup'}
    return render(request, 'custom_auth/signup.html', context)


def resend_confirmation(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        email = user.email
        
        current_site = get_current_site(request)
        html_content = render_to_string('custom_auth/email/activate_account.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token,
        })
            
        subject = 'Re-send confirmation email'  # Probably not necessary
        send_email(request, email, subject, html_content)

        html_content = render_to_string('custom_auth/email/resend_confirmation.html', {
            'email': email,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token,
        })
        messages.info(request, html_content)
    else:
        messages.error(request, 'Activation link is invalid or User does not exist.')

    return redirect('custom_auth:login')


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
                    # print('User is active. Something went wrong.')
                    pass
                else:  # User is not active

                    email = user.email
                    token = account_activation_token.make_token(user)
                    
                    current_site = get_current_site(request)
                    html_content = render_to_string('custom_auth/email/login_fail_resend_confirmation.html', {
                        'email': email,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': token,
                    })
                    messages.error(request, html_content)
                    return redirect('custom_auth:login')

                # print('User:', user, user.is_active)
                # print('User is none...')
        else:
            # print('Form is not valid...')
            pass

    else:
        form = CustomUserLoginForm()


    context = {'form': form, 'active': 'login'}
    return render(request, 'custom_auth/login.html', context)


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('generator:home')


@login_required
def account_view(request):
    user = None
    user = request.user

    form_delete = CustomUserDeleteForm()
    context = {'active': 'account','user': user, 'form_delete': form_delete}
    return render(request, 'custom_auth/account_view.html', context)


@login_required
def account_edit(request):
    user = request.user
    
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST or None, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your account details have beend updated.')
            return redirect('custom_auth:account_view')
        else:
            messages.error('Details invalid!')
            return redirect('custom_auth:account_edit')
    else:
        form = CustomUserEditForm(instance=user)

    context = {'form': form}
    return render(request, 'custom_auth/account_edit.html', context)


@login_required
def account_delete(request):
    user = request.user
    username = user.username
    if request.method == 'POST':
        form = CustomUserDeleteForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            encoded_password = user.password
            passed = check_password(password, encoded_password)
            if passed:
                user.delete()
                messages.success(request, f'Your account "{username}" has been deleted')
                return redirect('generator:home')

    messages.error(request, f'Could not delete account "{username}"')
    return redirect(request, 'custom_auth:account_view')

