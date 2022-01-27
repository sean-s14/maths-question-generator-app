from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserLoginForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test


@user_passes_test(lambda user: user.is_anonymous, login_url='/', redirect_field_name=None)
def signup_view(request):

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('generator:home')
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
                return redirect('generator:home')
            else:
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

    return redirect('generator:home')