from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Institution(models.Model):
    FOUNDATION = 1
    NGO = 2
    LOCAL = 3

    TYPE_CHOICES = (
        (FOUNDATION, "fundacja"),
        (NGO, "organizacja pozarządowa"),
        (LOCAL, "zbiórka lokalna"),
    )

    name = models.CharField(max_length=128)
    description = models.TextField()
    type = models.IntegerField(choices=TYPE_CHOICES, default=FOUNDATION)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return "{} \"{}\" ".format(self.get_type_display(), self.name).capitalize()


class Donation(models.Model):
    quantity = models.IntegerField()
    address = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=64)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, default=None)

    @property
    def name(self):
        """User-friendly display of Donation instance name"""
        return "Donation to: {}".format(self.institution)

    def __str__(self):
        return self.name
