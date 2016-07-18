from accounts.models import AcUser
from django.contrib.auth.hashers import check_password

class MyAuth:

    def authenticate(self, email="", password=""):
        try:
            user = AcUser.objects.get(email=email)
            if check_password(password, user.password):
                return user
            else:
                return None
        except AcUser.DoesNotExist:
            # No user was found, return None - triggers default login failed
            return None

    # Required for your backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
        try:
            return AcUser.objects.get(pk=user_id)
        except AcUser.DoesNotExist:
            return None
