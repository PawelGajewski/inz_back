from django.db import models
from datetime import datetime


class User(models.Model):
    name = models.TextField()
    surname = models.TextField()
    email = models.TextField()
    password = models.CharField(max_length=120)
    is_admin = models.BooleanField(default=False)


class Car(models.Model):
    userID = models.TextField(default=0)
    brand = models.TextField()
    model = models.TextField()
    version = models.TextField(default="")
    color = models.TextField()
    VIN = models.TextField()
    production_date = models.DateField()
    engine_capacity = models.IntegerField()
    fuel_type = models.TextField()
    mileage = models.IntegerField()
    OC_date = models.DateField(default="1970-01-01", blank=True)
    car_review_date = models.DateField(default="1970-01-01", blank=True)
    image = models.TextField(default='https://www.clipartwiki.com/iclipmax/wohRmi/')


class Service(models.Model):
    carID = models.TextField()
    userID = models.TextField()
    start_date = models.DateField(default='1970-01-01')
    end_date = models.DateField(default='1970-01-01')
    is_accepted = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    cli_date = models.DateField(default='1970-01-01')
    cli_info = models.TextField(default="Brak info!")
    cli_desc = models.TextField(default="Brak opisu!")


class Invoice(models.Model):
    serviceID = models.ForeignKey(Service, on_delete=models.CASCADE, default='0')
    job_name = models.TextField(default='0')
    job_amount = models.FloatField(default='0')
    job_prize = models.FloatField(default='0')
    carID = models.IntegerField(default='0')
