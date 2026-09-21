from django.contrib import admin

from .models import user


@admin.register(user)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "user_id",
        "nb_telephone",
        "name",
        "prenom",
        "type_user",
        "is_active",
        "is_staff",
    ]

    search_fields = [
        "nb_telephone",
        "name",
        "prenom",
        "NNI",
    ]

    list_filter = [
        "type_user",
        "is_active",
        "is_staff",
    ]
