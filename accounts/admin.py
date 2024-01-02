# from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = [
        "username",
        "email",
        "is_staff",
    ]
    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {
                "fields": "username",
            },
        )
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("username", "email")})
    )


# admin.site.register(User, CustomUserAdmin)
