from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('id',"first_name","last_name",'username',"email", "is_staff", "is_active",'is_superuser',"created_at","updated_at")
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("first_name","last_name",'username',"email")}),
        ("Permissions", {"fields": ("is_staff", "is_active",'is_superuser', "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "first_name","last_name",'username',"email","password1","password2", "is_staff",
                "is_active",'is_superuser', "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

