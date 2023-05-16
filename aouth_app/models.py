from django.db import models
from django.utils import timezone
from oauthlib.common import generate_token


class OAuthToken(models.Model):
    token = models.CharField(max_length=255)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return self.expires_at <= timezone.now()

    def generate_token(self):
        self.token = generate_token()
        self.expires_at = timezone.now() + timezone.timedelta(minutes=3)
        self.save()

    @classmethod
    def get_valid_token(cls):
        token = cls.objects.first()
        if not token or token.is_expired():
            token = cls()
            token.generate_token()
        return token.token
    

class UserDetails(models.Model):
    f_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    email_id = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.f_name

