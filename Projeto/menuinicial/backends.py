from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class CPFBackend(BaseBackend):
    def authenticate(self, request, cpf=None, password=None):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(cpf=cpf)
            if user.check_password(password):
                return user
        except user_model.DoesNotExist:
            return None
        return None
