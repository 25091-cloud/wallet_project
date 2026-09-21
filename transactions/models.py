from django.db import models

class transaction(models.Model):
    trans_id = models.AutoField(primary_key=True)

    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_trans = models.DateTimeField(auto_now_add=True)
    choix_type = [
        ('transfert','Transfert'),
        ('depot','Depot'),
        ('retrait', 'Retrait'),
    ]
    choix_statut = [
        ('en attente','En attente'),
        ('effectué','Effectué'),
        ('annulé','Annulé')]

    type_trans = models.CharField(max_length=10, choices=choix_type)
    statut_trans = models.CharField(max_length=15, choices=choix_statut, default='en attente')
    wallet_expediteur = models.ForeignKey('wallet.wallet', on_delete=models.SET_NULL, null=True, related_name='transactions_expediteur', db_column='wallet_expediteur_id')
    wallet_destinataire = models.ForeignKey('wallet.wallet', on_delete=models.SET_NULL, null=True, related_name='transactions_destinataire', db_column='wallet_destinataire_id')    
    deposent = models.ForeignKey('wallet.wallet', on_delete=models.SET_NULL, null=True, blank = True ,  related_name='transactions_deposit', db_column='deposent_id')


    class Meta:
        ordering = ["-date_trans"]

    def __str__(self):
        return f"Transaction {self.trans_id}: {self.type_trans} of {self.montant} on {self.date_trans} with status {self.statut_trans}"



