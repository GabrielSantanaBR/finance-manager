from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from core.forms import validate_document_upload

class Revenue(models.Model):
    class Category(models.TextChoices):
        SALES = "TITHE", "Vendas"
        SERVICES = "OFFERING", "Serviços"
        SUBSCRIPTION = "FUNERAL_PLAN", "Planos e assinaturas"
        EVENT = "EVENT", "Eventos"
        CONTRIBUTION = "DONATION", "Aportes e contribuições"
        REIMBURSEMENT = "REIMBURSEMENT", "Reembolso"
        OTHER = "OTHER", "Outro"
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Rascunho"
        PENDING = "PENDING", "Pendente"
        REVIEWED = "REVIEWED", "Revisada"
        APPROVED = "APPROVED", "Aprovada"
        REJECTED = "REJECTED", "Rejeitada"
        POSTED = "POSTED", "Lançada"
    ministry = models.ForeignKey("ministries.Ministry", on_delete=models.PROTECT, null=True, blank=True, related_name="revenues", verbose_name="Departamento")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="revenues_created")
    received_date = models.DateField("Data do recebimento", null=True, blank=True)
    category = models.CharField(max_length=30, choices=Category.choices, default=Category.OTHER)
    offering_type = models.CharField("Subcategoria", max_length=40, blank=True, default="")
    is_reimbursement = models.BooleanField("Reembolso", default=False)
    tithe_count = models.PositiveIntegerField("Quantidade de itens", default=0)
    value = models.DecimalField("Valor", max_digits=14, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    observation = models.TextField("Observação", blank=True, default="")
    receipt = models.FileField(upload_to="revenues/%Y/%m/", blank=True, null=True, validators=[validate_document_upload])
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.POSTED, db_index=True)
    approval_note = models.TextField("Observação da aprovação", blank=True, default="")
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="revenues_reviewed")
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="revenues_approved")
    approved_at = models.DateTimeField(null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["-received_date", "-created_at"]
        indexes = [models.Index(fields=["status", "received_date"])]
    def clean(self):
        if self.status not in {self.Status.DRAFT, self.Status.REJECTED}:
            errors = {}
            if not self.received_date: errors["received_date"] = "Informe a data do recebimento."
            if self.value is None or self.value <= 0: errors["value"] = "Informe um valor maior que zero."
            if self.category == self.Category.OTHER and not (self.observation or "").strip(): errors["observation"] = "Informe o nome desta receita."
            if errors: raise ValidationError(errors)
        self.is_reimbursement = self.category == self.Category.REIMBURSEMENT
    def save(self, *args, **kwargs):
        self.is_reimbursement = self.category == self.Category.REIMBURSEMENT
        super().save(*args, **kwargs)
    @property
    def accounting_category_display(self):
        if self.category == self.Category.OTHER and (self.observation or "").strip(): return self.observation.strip()
        return self.get_category_display()
    def __str__(self): return f"{self.accounting_category_display} - R$ {(self.value or 0):.2f}"
