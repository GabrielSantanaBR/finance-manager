from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class Ministry(models.Model):
    name = models.CharField("Nome", max_length=100, unique=True)
    description = models.TextField("Descrição", blank=True)
    active = models.BooleanField("Ativo", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["name"]
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
    def __str__(self):
        return self.name

class MinistryBudget(models.Model):
    ministry = models.ForeignKey(Ministry, on_delete=models.CASCADE, related_name="budgets", verbose_name="Departamento")
    year = models.PositiveIntegerField("Ano")
    month = models.PositiveSmallIntegerField("Mês", validators=[MinValueValidator(1), MaxValueValidator(12)])
    amount = models.DecimalField("Orçamento", max_digits=14, decimal_places=2)
    notes = models.TextField("Observações", blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["-year", "-month", "ministry__name"]
        verbose_name = "Orçamento de departamento"
        verbose_name_plural = "Orçamentos de departamentos"
        constraints = [models.UniqueConstraint(fields=["ministry", "year", "month"], name="unique_ministry_month_budget")]
    def __str__(self):
        return f"{self.ministry} - {self.month:02d}/{self.year}"
