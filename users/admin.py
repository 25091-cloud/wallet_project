from django.contrib import admin
from .models import user


@admin.register(user)
class UserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'name', 'prenom', 'nb_telephone', 'NNI', 'type_user', 'is_active', 'is_staff']
    search_fields = ['name', 'prenom', 'nb_telephone', 'NNI']