from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
import django
import django.contrib.auth as a
import django.core.validators as v

GENDER_CHOICES = [('M','M'), ('F','F')]


class User(AbstractUser):
    # username = models.CharField(max_length=100, unique=True)
    # email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)

    # REQUIRED_FIELDS = []


class Location(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)


class Visit(models.Model):
    user_id = models.ForeignKey(User, related_name='visits', on_delete=models.CASCADE)
    location_id = models.ForeignKey(Location, related_name='visits', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    ratio = models.IntegerField(validators=[v.MinValueValidator(0), v.MaxValueValidator(10)])
