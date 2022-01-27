from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


UserModel = get_user_model()

class CustomModelBackend(ModelBackend):
    """
    Authenticates against settings.AUTH_USER_MODEL.
    """

    def authenticate(self, request, email=None, username=None, password=None, **kwargs):
            
        if ( username is None and email is None ) or password is None:
            return

        try:
            if email is None:
                user = UserModel._default_manager.get(username=username)
            else:
                user = UserModel._default_manager.get(email=email)

        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user