from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username", "email", "first_name", "last_name",
        "role", "department", "employee_id", "is_active", "is_staff",
    )
    list_filter = ("role", "department", "is_active", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name", "employee_id")
    list_editable = ("role", "is_active")
    fieldsets = UserAdmin.fieldsets + (
        ("Fortius Profile", {"fields": ("role", "employee_id", "department", "phone")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Fortius Profile", {"fields": ("role", "employee_id", "department", "phone")}),
    )
