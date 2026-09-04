from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager): # the manager for the user model
    def create_user(self, nb_telephone, password=None, **extra_fields): # **extra_fields to adding in the user model ( name , prenom , NNI , type_user ) 
        if not nb_telephone:
            raise ValueError('Le numéro de téléphone est obligatoire')
        user = self.model(nb_telephone=nb_telephone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_superuser(self, nb_telephone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(nb_telephone, password, **extra_fields)


class user(AbstractBaseUser, PermissionsMixin): # abstractBaseUser: for authentication ( login ) , PermissionsMixin: for permissions ( is_staff , is_superuser )
    TYPE_CHOICES = [
        ('client', 'Client'),
        ('agence', 'Agence'),
        ('admin', 'Admin'),
    ]
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    NNI = models.CharField(max_length=100, unique=True)
    nb_telephone = models.CharField(max_length=100, unique=True )
    type_user = models.CharField(max_length=10, choices=TYPE_CHOICES , default='client')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # access to admin site

    objects = UserManager() # 

    USERNAME_FIELD = 'nb_telephone' # for authentication ( login )
    REQUIRED_FIELDS = ['name', 'prenom'] # for creating superuser

    def __str__(self):
        return f"{self.prenom} {self.name}"