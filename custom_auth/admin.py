from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# admin.site.register(CustomUser, UserAdmin)

class CustomUserAdmin(UserAdmin):
    list_filter = ('is_staff', 'is_active')
    list_display = ('username', 'email', 'is_active', 'is_staff')

admin.site.register(CustomUser, CustomUserAdmin)