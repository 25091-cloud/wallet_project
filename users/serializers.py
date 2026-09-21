from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import user
from wallet.models import wallet
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class userSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True, validators=[validate_password])
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )
    class Meta:
        model = user
        fields = [
            'name',
            'prenom',
            'NNI',
            'nb_telephone',
            'password',
            
        ]

    def create(self, validated_data):
        user_instance = user.objects.create_user(
            nb_telephone=validated_data['nb_telephone'],
            password=validated_data['password'],
            name=validated_data['name'],
            prenom=validated_data['prenom'],
            NNI=validated_data['NNI'],
            type_user="client"
        )
        wallet.objects.create(user=user_instance)
        return user_instance


class LoginSerializer(TokenObtainPairSerializer):
    username_field = 'nb_telephone'


class ProfileSerializer(serializers.ModelSerializer):
    solde = serializers.SerializerMethodField()

    class Meta:
        model = user
        fields = ['user_id', 'name', 'prenom', 'NNI', 'nb_telephone', 'type_user', 'solde']
        read_only_fields = ['user_id', 'NNI', 'nb_telephone', 'type_user']

    def get_solde(self, obj):
        wallet_instance = getattr(obj, 'wallet', None)
        if wallet_instance is None :
            return None
        return wallet_instance.solde

