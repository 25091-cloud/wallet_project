from rest_framework import serializers
from .models import transaction
from wallet.models import wallet


class TransactionSerializer(serializers.ModelSerializer):

    type_trans = serializers.SerializerMethodField()

    telephone_expediteur = serializers.SerializerMethodField()
    telephone_destinataire = serializers.SerializerMethodField()

    class Meta:
        model = transaction
        fields = [
            'trans_id',
            'montant',
            'date_trans',
            'type_trans',
            'statut_trans',
            'telephone_expediteur',
            'telephone_destinataire',
        ]

        read_only_fields = fields

    def get_type_trans(self, obj):

        request = self.context.get('request')

        if not request or not request.user:
            return obj.type_trans

        current_user = request.user

        # Dépôt
        if obj.type_trans == "depot":
            return "depot"

        # Retrait
        if obj.type_trans == "retrait":
            return "retrait"

        # Transfert
        if obj.type_trans == "transfert":

            # Celui qui envoie
            if (
                obj.wallet_expediteur
                and obj.wallet_expediteur.user == current_user
            ):
                return "envoi"

            # Celui qui reçoit
            elif (
                obj.wallet_destinataire
                and obj.wallet_destinataire.user == current_user
            ):
                return "recoit"

        return obj.type_trans

    def get_telephone_expediteur(self, obj):

        if not obj.wallet_expediteur:
            return None

        return obj.wallet_expediteur.user.nb_telephone

    def get_telephone_destinataire(self, obj):

        if not obj.wallet_destinataire:
            return None

        return obj.wallet_destinataire.user.nb_telephone