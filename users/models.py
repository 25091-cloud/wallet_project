from django.db import models

class user (models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    NNI = models.CharField(max_length=100)
    nb_telephone = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.prenom} {self.name}"