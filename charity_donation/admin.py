from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Category, CustomUser, Donation, Institution

# UserAdmin - provided by Django look for User model in admin panel
admin.site.register(CustomUser, UserAdmin)  # CustomUser uses UserAdmin look in admin panel
admin.site.register(Category)
admin.site.register(Institution)


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
