from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from knox.models import AuthToken
from knox.settings import CONSTANTS, knox_settings
from knox import crypto



class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=13, blank=True)
    image = models.ImageField(upload_to="profile", blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]



class UserAgent(models.Model):
    family = models.CharField(max_length=250, null=True)
    brand = models.CharField(max_length=250, null=True)
    model = models.CharField(max_length=250, null=True)

    def __str__(self):
        res = tuple((self.family, self.brand, self.model))
        return str(res)

class CustomeAuthTokenManager(models.Manager):
    def create(self, user, user_agent, expiry=knox_settings.TOKEN_TTL):
        token = crypto.create_token_string()
        digest = crypto.hash_token(token)
        if expiry is not None:
            expiry = timezone.now() + expiry

        instance = super(CustomeAuthTokenManager, self).create(
            token_key=token[:CONSTANTS.TOKEN_KEY_LENGTH], digest=digest,
            user=user, expiry=expiry, user_agent=user_agent)

        return instance, token
        

    # def filter(self, user, *args, **kwargs):
    #     return AuthToken.objects.filter(user=user)

    # def all(self):
    #     return AuthToken.objects.all()

class CustomeAuthToken(AuthToken):
    objects = CustomeAuthTokenManager()

    user_agent = models.OneToOneField(UserAgent, on_delete=models.CASCADE)
