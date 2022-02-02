from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

# User = get_user_model()

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'.")


class CustomUser(AbstractUser):
    pass


class Group(models.Model):
    group_name = models.CharField(max_length=128)

    def __str__(self):
        return self.group_name


class Contact(models.Model):
    group = models.ForeignKey(Group, related_name='contacts', on_delete=models.CASCADE)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(validators=[phone_regex],
                                    max_length=11,
                                    blank=True)
    address = models.TextField(max_length=256,
                               default='',
                               blank=True)

    def __str__(self):
        return self.user
