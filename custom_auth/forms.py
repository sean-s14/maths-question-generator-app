from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, Form
from django import forms
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email',)

        # TODO: Change placeholders

        labels = {
            "password2": _("Confirm Password")
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["placeholder"] = "username"
        self.fields["username"].widget.attrs["class"] = "input"
        self.fields["email"].widget.attrs["placeholder"] = "email"
        self.fields["email"].widget.attrs["class"] = "input"
        self.fields["password1"].widget.attrs["placeholder"] = "password"
        self.fields["password1"].widget.attrs["class"] = "input"
        self.fields["password2"].widget.attrs["placeholder"] = "password again"
        self.fields["password2"].widget.attrs["class"] = "input"

        
class CustomUserLoginForm(Form):

    username = forms.CharField(
        label=_('Email/Username'),
        max_length=150, 
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'email or username', 'class': 'input'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'password', 'class': 'input'}), 
        required=True
    )

