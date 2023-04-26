from django.contrib import admin
from .models import User, CustomeAuthToken


class CustomeUserAdmin(admin.ModelAdmin):
    model = User
    fieldsets = (
        (None, {"fields": ("username", "email", "password", "first_name","last_name", "phone_number", "image")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )

admin.site.register(User, CustomeUserAdmin)
admin.site.register(CustomeAuthToken)