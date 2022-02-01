from django.urls import path, re_path
from .views import (
    login_view,
    logout_view,
    signup_view,
    resend_confirmation,
    activate,
    account_view,
    account_edit,
    account_delete
)

app_name = 'custom_auth'
urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('account/', account_view, name='account_view'),
    path('account/edit/', account_edit, name='account_edit'),
    path('account/delete/', account_delete, name='account_delete'),
    re_path(r'^re-send-confirmation/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$',
        resend_confirmation, name='resend_confirmation'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$',
        activate, name='activate'),
]