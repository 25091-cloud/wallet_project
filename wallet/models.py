from django.db import models


class wallet(models.Model):
    wallet_id = models.AutoField(primary_key=True)
    solde = models.DecimalField(max_digits=10, decimal_places=2 , default=0)
    user = models.ForeignKey('users.user', on_delete=models.CASCADE, related_name='wallets' , db_column='user_id')