from django.contrib import admin

from .models import Category, Donation, Institution


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    pass


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    pass
