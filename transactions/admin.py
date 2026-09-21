from django.contrib import admin

from .models import transaction


@admin.register(transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "trans_id",
        "montant",
        "type_trans",
        "statut_trans",
        "date_trans",
    ]

    list_filter = [
        "type_trans",
        "statut_trans",
        "date_trans",
    ]

    ordering = ["-date_trans"]
