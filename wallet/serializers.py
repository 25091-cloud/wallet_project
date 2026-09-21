from rest_framework import serializers
from .models import wallet

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = wallet
        fields = ['wallet_id','solde']
        read_only_fields = fields   



class WalletDepositSerializer(serializers.Serializer):
    montant = serializers.DecimalField(max_digits=10,
    decimal_places=2,
    min_value=0.01)

class WalletWithdrawSerializer(serializers.Serializer):
    montant = serializers.DecimalField(max_digits=10,
    decimal_places=2,
    min_value=0.01)



class WalletTransferSerializer(serializers.Serializer):
    montant = serializers.DecimalField(max_digits=10,
    decimal_places=2,
    min_value=0.01)
    nb_telephone_destinataire = serializers.CharField(max_length=15)
    