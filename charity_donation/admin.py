from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Category, CustomUser, Donation, Institution

# UserAdmin - allows to manage Users in Django admin panel (defines how User instances are displayed in admin panel)
admin.site.register(CustomUser, UserAdmin)  # register CustomUser as UserAdmin field
admin.site.register(Category)
admin.site.register(Institution)


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_taken')
