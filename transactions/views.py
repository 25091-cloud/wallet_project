from django.db.models import Q

from rest_framework import permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import transaction
from .serializers import TransactionSerializer


class TransactionPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


class TransactionListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        wallet_instance = request.user.wallet

        transactions = transaction.objects.filter(
            Q(wallet_expediteur=wallet_instance)
            | Q(wallet_destinataire=wallet_instance)
            | Q(deposent=wallet_instance)
        ).distinct()

        type_filter = request.query_params.get("type")
        if type_filter:
            transactions = transactions.filter(
                type_trans=type_filter
            )

        date_filter = request.query_params.get("date")
        if date_filter:
            transactions = transactions.filter(
                date_trans__date=date_filter
            )

        date_from = request.query_params.get("date_from")
        if date_from:
            transactions = transactions.filter(
                date_trans__date__gte=date_from
            )

        date_to = request.query_params.get("date_to")
        if date_to:
            transactions = transactions.filter(
                date_trans__date__lte=date_to
            )

        transactions = transactions.order_by("-date_trans")

        paginator = TransactionPagination()
        page = paginator.paginate_queryset(
            transactions,
            request,
            view=self,
        )

        serializer = TransactionSerializer(
            page,
            many=True,
            context={
                "wallet_instance": wallet_instance,
            },
        )

        return paginator.get_paginated_response(serializer.data)
