from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q, Sum

class FinancialAccount(models.Model):
    class Kind(models.TextChoices):
        CASH = "CASH", "Caixa físico"
        CHECKING = "CHECKING", "Conta corrente"
        SAVINGS = "SAVINGS", "Poupança"
        INVESTMENT = "INVESTMENT", "Aplicação"
        OTHER = "OTHER", "Outro"
    name = models.CharField("Nome", max_length=120)
    institution = models.CharField("Instituição", max_length=120, blank=True)
    kind = models.CharField("Tipo", max_length=20, choices=Kind.choices, default=Kind.CHECKING)
    opening_balance = models.DecimalField("Saldo inicial", max_digits=14, decimal_places=2, default=0)
    active = models.BooleanField("Ativa", default=True)
    notes = models.TextField("Observações", blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["name"]
    @property
    def balance(self):
        totals = self.transactions.aggregate(credits=Sum("amount", filter=Q(direction=AccountTransaction.Direction.CREDIT)), debits=Sum("amount", filter=Q(direction=AccountTransaction.Direction.DEBIT)))
        return self.opening_balance + (totals["credits"] or Decimal("0")) - (totals["debits"] or Decimal("0"))
    def __str__(self):
        return self.name

class AccountTransaction(models.Model):
    class Direction(models.TextChoices):
        CREDIT = "CREDIT", "Entrada"
        DEBIT = "DEBIT", "Saída"
    account = models.ForeignKey(FinancialAccount, on_delete=models.PROTECT, related_name="transactions")
    date = models.DateField("Data")
    direction = models.CharField("Tipo", max_length=10, choices=Direction.choices)
    amount = models.DecimalField("Valor", max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    description = models.CharField("Descrição", max_length=220)
    reference = models.CharField("Referência", max_length=100, blank=True)
    revenue = models.ForeignKey("revenues.Revenue", on_delete=models.SET_NULL, null=True, blank=True, related_name="account_transactions")
    expense = models.ForeignKey("expenses.Expense", on_delete=models.SET_NULL, null=True, blank=True, related_name="account_transactions")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-date", "-created_at"]
        indexes = [models.Index(fields=["account", "date"])]
    def __str__(self):
        return f"{self.get_direction_display()} - {self.description}"
