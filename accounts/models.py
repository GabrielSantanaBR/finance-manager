from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Administrador financeiro"
        LEADER = "LEADER", "Responsável de departamento"

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.LEADER)
    # Nome técnico legado mantido para compatibilidade com o banco existente.
    # Na versão genérica, "ministry" representa um departamento/centro de responsabilidade.
    ministry = models.ForeignKey("ministries.Ministry", on_delete=models.SET_NULL, null=True, blank=True, related_name="users")

    @property
    def is_master_admin(self):
        return self.is_superuser

    @property
    def is_finance_admin(self):
        return self.is_superuser or self.role == self.Roles.ADMIN

    def clean(self):
        super().clean()
        if self.role == self.Roles.LEADER and not self.ministry_id:
            raise ValidationError({"ministry": "Um responsável deve estar vinculado a um departamento."})

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.Roles.ADMIN
        super().save(*args, **kwargs)
