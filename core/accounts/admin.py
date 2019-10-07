from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Define admin model for custom User model with email field.
    """

    list_display = (
        "email",
        "first_name",
        "last_name",
        "university",
        "degree_commencement_year",
        "is_staff",
    )
    list_filter = (
        "is_staff",
        "university",
        "degree_commencement_year",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                ),
            }
        ),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "university",
                    "degree_commencement_year",
                ),
            }
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            }
        ),
        (
            "Important dates",
            {
                "fields": (
                    "date_joined",
                ),
            }
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": (
                    "wide",
                ),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                ),
            }
        ),
    )
    readonly_fields = (
        "date_joined",
    )
    search_fields = (
        "email",
        "first_name",
        "last_name"
    )
    ordering = (
        "email",
    )
    filter_horizontal = ()


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
