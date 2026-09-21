from django.db import transaction as db_transaction

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from transactions.models import transaction
from users.models import user
from .models import wallet
from .serializers import (
    WalletSerializer,
    WalletDepositSerializer,
    WalletWithdrawSerializer,
    WalletTransferSerializer,
)


class WalletDataView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        wallet_instance, created = wallet.objects.get_or_create(
            user=request.user
        )

        serializer = WalletSerializer(wallet_instance)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class DepositView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = WalletDepositSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        montant = serializer.validated_data["montant"]

        with db_transaction.atomic():
            wallet_instance = wallet.objects.select_for_update().get(
                user=request.user
            )

            wallet_instance.solde += montant
            wallet_instance.save(update_fields=["solde"])

            transaction.objects.create(
                statut_trans="effectué",
                deposent=wallet_instance,
                montant=montant,
                type_trans="depot",
            )

        return Response(
            {
                "message": "Dépôt effectué avec succès.",
                "solde": wallet_instance.solde,
            },
            status=status.HTTP_200_OK,
        )


class WithdrawView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = WalletWithdrawSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        montant = serializer.validated_data["montant"]

        with db_transaction.atomic():
            wallet_instance = wallet.objects.select_for_update().get(
                user=request.user
            )

            if wallet_instance.solde < montant:
                return Response(
                    {
                        "error": (
                            "Solde insuffisant pour effectuer "
                            "le retrait."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            wallet_instance.solde -= montant
            wallet_instance.save(update_fields=["solde"])

            transaction.objects.create(
                statut_trans="effectué",
                deposent=wallet_instance,
                montant=montant,
                type_trans="retrait",
            )

        return Response(
            {
                "message": "Retrait effectué avec succès.",
                "solde": wallet_instance.solde,
            },
            status=status.HTTP_200_OK,
        )


class TransferView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = WalletTransferSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        montant = serializer.validated_data["montant"]
        telephone_destinataire = serializer.validated_data[
            "nb_telephone_destinataire"
        ]

        try:
            destinataire = user.objects.get(
                nb_telephone=telephone_destinataire
            )
        except user.DoesNotExist:
            return Response(
                {"error": "Le destinataire n'existe pas."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if destinataire == request.user:
            return Response(
                {
                    "error": (
                        "Vous ne pouvez pas transférer de l'argent "
                        "à vous-même."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        with db_transaction.atomic():
            wallet_expediteur = wallet.objects.select_for_update().get(
                user=request.user
            )

            wallet_destinataire, created = (
                wallet.objects.select_for_update().get_or_create(
                    user=destinataire
                )
            )

            if wallet_expediteur.solde < montant:
                return Response(
                    {"error": "Solde insuffisant."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            wallet_expediteur.solde -= montant
            wallet_destinataire.solde += montant

            wallet_expediteur.save(update_fields=["solde"])
            wallet_destinataire.save(update_fields=["solde"])

            transaction.objects.create(
                montant=montant,
                type_trans="transfert",
                statut_trans="effectué",
                wallet_expediteur=wallet_expediteur,
                wallet_destinataire=wallet_destinataire,
            )

        return Response(
            {
                "message": "Transfert effectué avec succès.",
                "solde": wallet_expediteur.solde,
            },
            status=status.HTTP_200_OK,
        )
