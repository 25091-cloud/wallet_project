from django.contrib import admin

from .models import wallet


@admin.register(wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ["wallet_id", "user", "solde"]
    search_fields = ["user__nb_telephone"]
