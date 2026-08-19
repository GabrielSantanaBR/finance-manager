from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class FixedExpense(models.Model):
    class PaymentMethod(models.TextChoices):
        PIX = "PIX", "PIX"
        CASH = "DINHEIRO", "Dinheiro"
        DEBIT = "DEBITO", "Débito"
        CREDIT = "CREDITO", "Crédito"
        TRANSFER = "TRANSFERENCIA", "Transferência"
    ministry = models.ForeignKey("ministries.Ministry", on_delete=models.PROTECT, related_name="fixed_expenses", verbose_name="Departamento")
    name = models.CharField("Nome", max_length=150)
    description = models.TextField("Descrição", blank=True, default="")
    value = models.DecimalField("Valor", max_digits=14, decimal_places=2)
    due_day = models.PositiveSmallIntegerField("Dia do vencimento", validators=[MinValueValidator(1), MaxValueValidator(31)])
    payment_method = models.CharField("Forma de pagamento", max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.PIX)
    supplier = models.CharField("Favorecido", max_length=150, blank=True, default="")
    budget_code = models.CharField("Centro de custo", max_length=50, blank=True, default="")
    active = models.BooleanField("Ativo", default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="fixed_expenses_created")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["due_day", "name"]
    def __str__(self):
        return self.name

class FixedExpensePayment(models.Model):
    fixed_expense = models.ForeignKey(FixedExpense, on_delete=models.PROTECT, related_name="payments")
    reference_month = models.DateField("Mês de referência", help_text="Use o primeiro dia do mês.")
    paid_on = models.DateField("Pago em")
    amount = models.DecimalField("Valor pago", max_digits=14, decimal_places=2)
    expense = models.OneToOneField("expenses.Expense", on_delete=models.PROTECT, related_name="fixed_payment")
    paid_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-reference_month", "fixed_expense__due_day"]
        constraints = [models.UniqueConstraint(fields=["fixed_expense", "reference_month"], name="unique_fixed_expense_payment_month")]
    def __str__(self):
        return f"{self.fixed_expense} - {self.reference_month:%m/%Y}"
