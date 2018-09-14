from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    """
        Extended AbstractUser model
    """
    bio = models.TextField(_(u'Biography'), max_length=500, blank=True)
    ip = models.GenericIPAddressField(_(u'Last login IP'), null=True)
