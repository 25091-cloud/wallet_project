from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, nb_telephone, password=None, **extra_fields):
        if not nb_telephone:
            raise ValueError(
                "Le numéro de téléphone est obligatoire"
            )

        user_instance = self.model(
            nb_telephone=nb_telephone,
            **extra_fields
        )

        user_instance.set_password(password)
        user_instance.save(using=self._db)

        return user_instance

    def create_superuser(self, nb_telephone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("type_user", "admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Le superuser doit avoir is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Le superuser doit avoir is_superuser=True"
            )

        return self.create_user(
            nb_telephone=nb_telephone,
            password=password,
            **extra_fields
        )


class user(AbstractBaseUser, PermissionsMixin):

    TYPE_CHOICES = [
        ("client", "Client"),
        ("agence", "Agence"),
        ("admin", "Admin"),
    ]

    user_id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=100)

    prenom = models.CharField(max_length=100)

    NNI = models.CharField(
        max_length=100,
        unique=True,
    )

    nb_telephone = models.CharField(
        max_length=20,
        unique=True,
    )

    type_user = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default="client",
    )

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "nb_telephone"

    REQUIRED_FIELDS = [
        "name",
        "prenom",
        "NNI",
    ]

    def __str__(self):
        return f"{self.prenom} {self.name}"
