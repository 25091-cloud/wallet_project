from django.db import models
from django.db.models import Q


class wallet(models.Model):
    wallet_id = models.AutoField(primary_key=True)
    solde = models.DecimalField(max_digits=10, decimal_places=2 , default=0)
    user = models.OneToOneField(
    'users.user',
    on_delete=models.CASCADE,
    related_name='wallet',
    db_column='user_id'
)


    def __str__(self):
        return f"Wallet {self.wallet_id} for user {self.user.name} {self.user.prenom} he has : {self.solde}"