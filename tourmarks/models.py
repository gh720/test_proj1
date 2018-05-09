from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
import django
import django.contrib.auth as a
import django.core.validators as v
GENDER_CHOICES = ['M', 'F']


class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(choices=GENDER_CHOICES, blank=True, required=False)
    birth_date = models.DateField(required=False)
    country = models.CharField(max_length=200, required=False)

    # REQUIRED_FIELDS = []


class Location:
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)


class Visit:
    user_id = models.ForeignKey(User, related_name='visits')
    location_id = models.ForeignKey(Location, related_name='visits')
    date = models.DateTimeField(auto_now_add=True)
    ratio = models.IntegerField(validators=[ v.MinValueValidator(0), v.MaxValueValidator(10)])