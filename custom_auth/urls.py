from django.urls import path, re_path
from .views import (
    login_view,
    logout_view,
    signup_view,
    resend_confirmation,
    activate,
    account_view,
    account_edit,
    account_delete,
    premium_view,

    create_checkout_session,
    customer_portal,
    webhook_received,
    payment_success,
    payment_cancel,
    cancel_subscription,
)

app_name = 'custom_auth'

urlpatterns = [
    path('create-checkout-session/', create_checkout_session, name='create_checkout_session'),
    path('create-portal-session/', customer_portal, name='customer_portal'),
    path('webhook/', webhook_received, name='webhook_received'),
    path('payment-success/', payment_success, name='payment_success'),
    path('payment-cancel/', payment_cancel, name='payment_cancel'),
    path('cancel-subscription/', cancel_subscription, name='cancel_subscription'),

    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('account/', account_view, name='account_view'),
    path('account/edit/', account_edit, name='account_edit'),
    path('account/delete/', account_delete, name='account_delete'),
    path('premium/', premium_view, name='premium_view'),
    re_path(r'^re-send-confirmation/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$',
        resend_confirmation, name='resend_confirmation'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$',
        activate, name='activate'),
]