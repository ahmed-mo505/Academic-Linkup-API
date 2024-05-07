# Once you've defined the EmailBackend class and configured Django to use it,
# Django will authenticate users based on their email address
# when you call the authenticate function during the login process.


from django.contrib.auth import get_user_model

class EmailBackend:
    def authenticate(self, request, email=None, password=None):
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
