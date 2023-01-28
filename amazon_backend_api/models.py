from django.db import models
from amazon_backend_api.manager import AmazonuserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class Amazonuser(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(_('full name'), max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AmazonuserManager()

    def __str__(self):
        return self.email
