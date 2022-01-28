from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomUserCreationForm, CustomUserLoginForm


UserModel = get_user_model()


@user_passes_test(lambda user: user.is_anonymous, login_url='/', redirect_field_name=None)
def signup_view(request):

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.is_active = False
            instance.save()
            return redirect('custom_auth:login')
        else:
            print('Form is NOT valid...')
    else:
        form = CustomUserCreationForm()

    context = {'form': form, 'active': 'signup'}
    return render(request, 'custom_auth/signup.html', context)

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
                login(request, user)
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
                    messages.error(request,'You must verify your email address before logging in')
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