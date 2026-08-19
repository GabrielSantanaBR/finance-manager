from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from core.forms import validate_document_upload

class Expense(models.Model):
    class Scope(models.TextChoices):
        MINISTRY = "MINISTRY", "Departamento"
        TREASURY = "TREASURY", "Administração central"
    class TreasuryCategory(models.TextChoices):
        OPERATIONS = "CHURCH", "Operações"
        MARKETING = "EVANGELISM", "Marketing e divulgação"
        SOCIAL = "SOCIAL_ACTION", "Projetos sociais"
        REIMBURSEMENT = "REIMBURSEMENT", "Reembolso"
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Rascunho"
        PENDING = "PENDING", "Pendente"
        REVIEWED = "REVIEWED", "Revisada"
        APPROVED = "APPROVED", "Aprovada"
        REJECTED = "REJECTED", "Rejeitada"
    class Category(models.TextChoices):
        PROFESSIONAL = "PREBENDA", "Serviços profissionais"
        FOOD = "FOOD", "Alimentação"
        TRANSPORT = "TRANSPORT", "Transporte"
        EVENT = "EVENT", "Evento"
        MAINTENANCE = "MAINTENANCE", "Manutenção"
        CLEANING = "CLEANING", "Limpeza"
        OFFICE = "OFFICE", "Material de escritório"
        MARKETING = "EVANGELISM", "Marketing e divulgação"
        CONSTRUCTION = "CONSTRUCTION", "Obras e infraestrutura"
        SOCIAL = "DONATION", "Projetos sociais"
        REIMBURSEMENT = "REIMBURSEMENT", "Reembolso"
        OTHER = "OTHER", "Outros"
    class PaymentMethod(models.TextChoices):
        PIX = "PIX", "PIX"
        CASH = "DINHEIRO", "Dinheiro"
        DEBIT = "DEBITO", "Cartão de débito"
        CREDIT = "CREDITO", "Cartão de crédito"
        TRANSFER = "TRANSFERENCIA", "Transferência"
    ministry = models.ForeignKey("ministries.Ministry", on_delete=models.PROTECT, null=True, blank=True, related_name="expenses", verbose_name="Departamento")
    scope = models.CharField(max_length=20, choices=Scope.choices, default=Scope.MINISTRY, db_index=True)
    treasury_category = models.CharField(max_length=30, choices=TreasuryCategory.choices, blank=True, default="", verbose_name="Categoria administrativa")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="expenses_created")
    purchase_date = models.DateField("Data da compra", null=True, blank=True)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.OTHER)
    supplier = models.CharField("Fornecedor", max_length=150, blank=True, default="")
    paid_to = models.CharField("Favorecido", max_length=150, blank=True, default="")
    requested_by = models.CharField("Solicitante", max_length=150, blank=True, default="")
    budget_code = models.CharField("Centro de custo", max_length=50, blank=True, default="")
    quantity = models.DecimalField("Quantidade", max_digits=10, decimal_places=2, default=1, validators=[MinValueValidator(0)])
    unit = models.CharField("Unidade", max_length=30, default="un")
    payment_method = models.CharField("Forma de pagamento", max_length=30, choices=PaymentMethod.choices, default=PaymentMethod.PIX)
    invoice_number = models.CharField("Número da nota fiscal", max_length=50, blank=True, default="")
    purpose = models.CharField("Finalidade", max_length=200, blank=True, default="")
    description = models.TextField("Observações", blank=True)
    value = models.DecimalField("Valor", max_digits=14, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    receipt = models.FileField(upload_to="receipts/%Y/%m/", blank=True, null=True, validators=[validate_document_upload])
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)
    approval_note = models.TextField("Observação da aprovação", blank=True, default="")
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="expenses_reviewed")
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="expenses_approved")
    approved_at = models.DateTimeField(null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["-purchase_date", "-created_at"]
        indexes = [models.Index(fields=["status", "purchase_date"]), models.Index(fields=["ministry", "purchase_date"])]
    def clean(self):
        if self.status != self.Status.DRAFT and self.scope == self.Scope.TREASURY and not self.treasury_category:
            raise ValidationError({"treasury_category": "Informe a categoria da despesa administrativa."})
        if self.scope == self.Scope.MINISTRY:
            self.treasury_category = ""
            if self.status != self.Status.DRAFT and not self.ministry_id:
                raise ValidationError({"ministry": "O usuário precisa estar vinculado a um departamento."})
        else:
            self.ministry = None
        if self.status != self.Status.DRAFT:
            errors = {}
            if self.category == self.Category.OTHER and not (self.description or "").strip(): errors["description"] = "Informe o nome desta despesa."
            if not self.purchase_date: errors["purchase_date"] = "Informe a data da compra."
            if self.value is None or self.value <= 0: errors["value"] = "Informe um valor maior que zero."
            if errors: raise ValidationError(errors)
    @property
    def accounting_category_display(self):
        if self.category == self.Category.OTHER and (self.description or "").strip(): return self.description.strip()
        return self.get_category_display()
    def can_view(self, user):
        return user.is_finance_admin or (self.scope == self.Scope.MINISTRY and user.ministry_id == self.ministry_id)
    def can_edit(self, user):
        if user.is_finance_admin: return True
        return self.created_by_id == user.id and self.status in {self.Status.DRAFT, self.Status.PENDING, self.Status.REJECTED}
    def __str__(self):
        origin = self.ministry or self.get_treasury_category_display() or "Administração central"
        return f"{origin} - R$ {(self.value or 0):.2f}"

class ExpenseItem(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name="expense_items")
    description = models.CharField("Descrição", max_length=200)
    quantity = models.DecimalField("Quantidade", max_digits=10, decimal_places=2, default=1, validators=[MinValueValidator(0)])
    unit = models.CharField("Unidade", max_length=20, default="un")
    unit_price = models.DecimalField("Valor unitário", max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    @property
    def total(self): return self.quantity * self.unit_price
    def __str__(self): return self.description
