from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Email field changed to 'unique' for authentication by email."""
    email = models.EmailField(unique=True)


class Category(models.Model):
    """Donation categories, e.g. toys, clothes."""
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Institution(models.Model):
    """Institutions to which donations are made."""

    # Institution types
    FOUNDATION = 1
    NGO = 2  # Non-governmental organisation
    LOCAL = 3  # Local charity groups and events

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
        """Display Institution model instance as 'type' + 'name'."""
        return "{} \"{}\" ".format(self.get_type_display(), self.name).capitalize()


class Donation(models.Model):
    """"
    Donation model contains info about user donations (institution, donation categories, amount of donated stuff)
    and pick-up data for courier (address from which donations will be picked up and date/time info).
    """
    quantity = models.IntegerField()  # Number of bags donated by user in one donation.
    address = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=64)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField(Category)
    is_taken = models.BooleanField(default=False)  # Allows user to mark if donation was taken by courier.
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, default=None)

    @property
    def name(self):
        """User-friendly display of Donation model instance name."""
        return "Donation to: {}".format(self.institution)

    def __str__(self):
        return self.name
