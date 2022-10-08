from django.db import models

# Create your models here.

class Perk(models.Model):
    name = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

class Person(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    image = models.CharField(max_length=200, null=True)
    pin = models.CharField(max_length=4, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    perks = models.ManyToManyField(Perk, blank=True)



