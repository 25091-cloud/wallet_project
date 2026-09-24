from django.db.models import Q

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import transaction
from .serializers import TransactionSerializer


class TransactionListView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        wallet_instance = request.user.wallet

        transactions = transaction.objects.filter(
            Q(wallet_expediteur=wallet_instance)
            | Q(wallet_destinataire=wallet_instance)
            | Q(deposent=wallet_instance)
        ).distinct()

        # Filter by type
        type_filter = request.query_params.get("type")

        if type_filter:
            transactions = transactions.filter(
                type_trans=type_filter
            )

        # Filter by exact date
        date_filter = request.query_params.get("date")

        if date_filter:
            transactions = transactions.filter(
                date_trans__date=date_filter
            )

        # Filter from date
        date_from = request.query_params.get("date_from")

        if date_from:
            transactions = transactions.filter(
                date_trans__date__gte=date_from
            )

        # Filter until date
        date_to = request.query_params.get("date_to")

        if date_to:
            transactions = transactions.filter(
                date_trans__date__lte=date_to
            )

        # Newest transactions first
        transactions = transactions.order_by("-date_trans")

        serializer = TransactionSerializer(
            transactions,
            many=True,
            context={
                "request": request,
                "wallet_instance": wallet_instance,
            }
        )

        return Response(serializer.data)