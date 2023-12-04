import datetime

from django.db import models
from django.utils import timezone


class Size(models.Model):
    value = models.IntegerField()
    label = models.CharField(max_length=30)
    pricePerDay = models.DecimalField(max_digits=8, decimal_places=2)
    serialNumber = models.CharField(max_length=80)

    def __str__(self):
        return self.label


class Article(models.Model):
    name = models.CharField(max_length=70)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.CharField(null=True, max_length=500)
    sizes = models.ManyToManyField(Size)
    description = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    category_name = models.CharField(max_length=30)

    def __str__(self):
        return self.category_name


class Booked(models.Model):
    startDate = models.DateField(null=True)
    endDate = models.DateField(null=True)
    bookingDate = models.DateField(default=datetime.date.today())
    firstName = models.CharField(max_length=50, null=True)
    lastName = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    phoneNumber = models.CharField(max_length=20, null=True)
    size = models.ForeignKey('Size', on_delete=models.CASCADE, related_name='object', default=0)
    street = models.CharField(max_length=70, null=True)
    local = models.CharField(max_length=70, null=True)
    note = models.TextField(null=True, max_length=300)

    def __str__(self):
        return self.startDate
