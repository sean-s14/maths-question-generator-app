from django.http import HttpResponse, JsonResponse
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



# Stripe
import stripe
stripe.api_key = settings.STRIPE_SK_KEY


@login_required(login_url='custom_auth:signup')
def premium_view(request):
    context = {}

    print('Is User Premium?', request.user.is_premium)

    try:
        # Get customer with user email if one exists
        customer = stripe.Customer.list(email=request.user.email).data[0].id
        print(customer)

        # Check if user has subscription
        subscription = stripe.Subscription.list(customer=customer).data[0]
        print(subscription.id)
        print(subscription)

        # Check if subscription will be renewed
        will_renew = subscription.get('cancel_at_period_end')
        if will_renew is not None:
            print('Will Renew:', will_renew)
            context = {'will_renew': will_renew}

    except Exception as e:
        print(e)


    # Get Prices and display them to user
    prices = stripe.Price.list(lookup_keys=['monthly_sub', 'yearly_sub'])
    
    prices = [
        {
            "id": price.id,
            "lookup_key": price.lookup_key,
            "amount": int(price.unit_amount)/100,
            "interval": price.recurring.interval,
        } for price in prices.data
    ]

    context = {**context, 'active': 'premium', 'prices': prices}
    return render(request, 'custom_auth/premium.html', context)


# YOUR_DOMAIN = 'https://maths-quizzer.herokuapp.com/'
YOUR_DOMAIN = settings.ENV_DOMAIN

def payment_cancel(request):
    return redirect('custom_auth:premium_view')
    # return render(request, 'custom_auth/cancel.html', {})

def payment_success(request):
    session_id = request.GET.get('session_id', None)

    try:
        user = UserModel.objects.get(session_id=session_id)
        messages.success(request, 'Congratulations, you are a Premium User!')
    except Exception as e:
        print(e)
        messages.error(request, 'Subscription failed!')

    # return render(request, 'custom_auth/success.html', {'session_id': session_id})
    return redirect('generator:home')

from datetime import datetime
def cancel_subscription(request):

    user_email = request.user.email

    # Retrieve latest Subscription object from Stripe with user's email
    customer = stripe.Customer.list(email=user_email).data[0].id
    subscription = stripe.Subscription.list(customer=customer).data[0]

    # Cancel subscription at period end
    subscription_cancellation = stripe.Subscription.modify(
        subscription.id,
        cancel_at_period_end=True
    )

    messages.success(request, 'Your subscription has been cancelled. An email has been sent to your account with more details.')
    return redirect('generator:home')


@login_required(login_url='custom_auth:signup')
@user_passes_test(lambda user: user.is_premium == False, login_url='custom_auth:account_view')
def create_checkout_session(request):
    if request.method == 'POST':
        try:
            # Get Price chosen from the form
            price_input = request.POST.get('premium_plan')
            price = stripe.Price.retrieve(price_input)
            # print(price)

            # Get customer with current user's email if one exists 
            email = request.user.email
            customer = None
            try:
                customer = stripe.Customer.list(email=email).data[0]  # This is the newest by default 
            except Exception as e:
                print('Error:', e)

            print('\nCustomer:', customer, '\n')

            # Parameters for Stripe Session object
            success_url = YOUR_DOMAIN + 'auth/payment-success/?session_id={CHECKOUT_SESSION_ID}'
            cancel_url = YOUR_DOMAIN + 'auth/premium/'
            mode = 'subscription'
            line_items = [
                    {
                        'price': price.id,
                        'quantity': 1,
                    },
                ]

            # If there is NO customer in the stripe database, use customer_email to populate email field.
            # If there IS a customer in the stripe database, populate use customer to populate all fields. 
            if customer is None:
                checkout_session = stripe.checkout.Session.create(
                    success_url=success_url,
                    cancel_url=cancel_url,
                    mode=mode,
                    line_items=line_items,
                    customer_email=email,
                )
            else:
                checkout_session = stripe.checkout.Session.create(
                    success_url=success_url,
                    cancel_url=cancel_url,
                    mode=mode,
                    line_items=line_items,
                    customer=customer,
                )

            # Save session_id after creating session. Session_id can be used to modify billing information.
            try:
                user = UserModel.objects.get(email=request.user.email)
                user.session_id = checkout_session.id
                user.save()
            except Exception as e:
                print(e)

            return redirect(checkout_session.url)
        except Exception as e:
            print(e)
            return HttpResponse("Server error (updated)")


def customer_portal(request):
    # For demonstration purposes, we're using the Checkout session to retrieve the customer ID.
    # Typically this is stored alongside the authenticated user in your database.
    if request.method == 'POST':
        checkout_session_id = request.POST.get('session_id')

        print('Checkout Session ID:', checkout_session_id)
        checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)

        # This is the URL to which the customer will be redirected after they are
        # done managing their billing with the portal.
        return_url = YOUR_DOMAIN

        portalSession = stripe.billing_portal.Session.create(
            customer=checkout_session.customer,
            return_url=return_url,
        )

        print('\nPortal Session Return URL:', portalSession.return_url)
        print('\nPortal Session URL:', portalSession.url, '\n')

        return redirect(portalSession.url)


import json
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def webhook_received(request):

    if request.method == 'POST':
        py_request_data = json.loads(request.body).get('data', None)

        webhook_secret = settings.STRIPE_WEBHOOK_SK
        if webhook_secret:
            # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
            signature = request.headers.get('stripe-signature')

            # Create event
            try:
                event = stripe.Webhook.construct_event(
                    payload=request.body, 
                    sig_header=signature, 
                    secret=webhook_secret
                )
                data = event['data']
            except stripe.error.SignatureVerificationError as e:
                print(e)
                return HttpResponse('Error')
            except Exception as e:
                print(e)
                return HttpResponse('Error')
            
            # Get the type of webhook event sent - used to check the status of PaymentIntents.
            event_type = event['type']
        else:
            data = py_request_data['data']
            event_type = py_request_data['type']

        data_object = data['object']

        print('event ' + event_type ,'\n')

        if event_type == 'checkout.session.completed':
            print('🔔 Payment succeeded!')

        elif event_type == 'customer.subscription.created':
            print('Subscription created -', event.id)

        elif event_type == 'customer.subscription.updated':
            print('Subscription updated -', event.id)
            print('Event Object: ', data_object)

            # Send email when user cancels subscription
            if data_object['cancel_at_period_end'] == True:
                print('Subscription canceled -', event.id)
                customer_id = data_object.get('customer', None)
                if customer_id is not None:
                    customer = stripe.Customer.retrieve(customer_id)
                    try:
                        user = UserModel.objects.get(email=customer.email)

                        # Notify user of subscription cancellation by email
                        current_period_end = data_object.get('current_period_end')
                        current_period_end = datetime.fromtimestamp(current_period_end)

                        html_content = render_to_string('custom_auth/email/subscription_cancellation.html', {
                            'username': user.username,
                            'date': current_period_end
                        })
                            
                        subject = 'Subscription Cancellation'
                        send_email(request, user.email, subject, html_content)
                    
                    except Exception as e:
                        print(e)
                else:
                    print('Could not get customer\'s ID ')


        elif event_type == 'customer.subscription.deleted':
            print('Subscription deleted -', event.id)
            # Get user email from data_object and change user's is_premium field to False
            # customer_email = data_object.get('customer_email', None)
            customer_id = data_object.get('customer')
            customer = stripe.Customer.retrieve(customer_id)
            customer_email = customer.get('email')
            print('Event Object:', data_object)
            print(customer_email)
            if customer_email is not None:
                try:
                    user = UserModel.objects.get(email=customer_email)
                    user.is_premium = False
                    user.save()
                    # TODO: Send email

                except UserModel.DoesNotExist as e:
                    print(e)
            else:
                print('Could not get customer\'s email\n')

        elif event_type == 'invoice.payment_succeeded':
            print('Invoice Payment Succeeded -', event.id)
            # Get user email from data_object and change user's is_premium field to True
            customer_email = data_object.get('customer_email', None)
            print('Event Object:', data_object)
            print('Customer Email:', customer_email)
            if customer_email is not None:
                try:
                    user = UserModel.objects.get(email=customer_email)
                    user.is_premium = True
                    print(user.is_premium)
                    user.save()
                    user = UserModel.objects.get(email=customer_email)
                    print(user.is_premium)
                    # TODO: Send email

                except UserModel.DoesNotExist as e:
                    print(e)
            else:
                print('Could not get customer\'s email\n')
        
        elif event_type == 'invoice.payment_failed':
            print('Payment failed!')

        

        return JsonResponse({'status': 'success'})