from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
import django.core.validators as v

GENDER_CHOICES = [('M','M'), ('F','F')]

class User(AbstractUser):
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)

    @property
    def object_owner(self):
        return self


class Location(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)


class Visit(models.Model):
    user = models.ForeignKey(User, related_name='visits', on_delete=models.CASCADE)
    location = models.ForeignKey(Location, related_name='visits', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    ratio = models.IntegerField(validators=[v.MinValueValidator(0), v.MaxValueValidator(10)])

    @property
    def object_owner(self):
        return self.user
