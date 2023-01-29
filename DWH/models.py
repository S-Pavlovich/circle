from datetime import datetime
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.utils import timezone


# Create your models here.


class User(models.Model):
    nickname = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_start_circle = models.DateField(null=True, blank=True)
    telegram_id = models.IntegerField(max_length=20, null=True, blank=True, default=0000000)
    timezone = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=80, null=True, blank=True)
    time_to_notificate = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.nickname

    def __int__(self):
        return self.telegram_id


class Event(models.Model):
    date_of_event = models.DateField()
    name = models.CharField(max_length=100, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1),
                                                                    MaxValueValidator(10)])
    additional_comment = models.TextField(max_length=300, validators=[MinLengthValidator(1)], null=True, blank=True)
    User = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
