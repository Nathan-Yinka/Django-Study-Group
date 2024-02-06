# backends.py
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            # Check if the username is a valid username or email
            user = user_model.objects.get(email=username)
        except user_model.DoesNotExist:
            # If user is not found by email, try with username
            try:
                user = user_model.objects.get(username=username)
            except user_model.DoesNotExist:
                return None
        
        # Check if the user's password is correct
        if user.check_password(password):
            return user
        return None
