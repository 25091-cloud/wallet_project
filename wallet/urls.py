from django.urls import path

from .views import (
    WalletDataView,
    DepositView,
    WithdrawView,
    TransferView,
)


urlpatterns = [
    path("", WalletDataView.as_view(), name="wallet-data"),
    path("deposit/", DepositView.as_view(), name="deposit"),
    path("withdraw/", WithdrawView.as_view(), name="withdraw"),
    path("transfer/", TransferView.as_view(), name="transfer"),
]
