from django.conf import settings
from django.db import models

class AuditLog(models.Model):
    class Action(models.TextChoices):
        CREATE = "CREATE", "Criou"
        UPDATE = "UPDATE", "Atualizou"
        DELETE = "DELETE", "Excluiu"
        APPROVE = "APPROVE", "Aprovou"
        REJECT = "REJECT", "Rejeitou"
        EXPORT = "EXPORT", "Exportou"
        IMPORT = "IMPORT", "Importou"
        CLOSE = "CLOSE", "Fechou período"
        REOPEN = "REOPEN", "Reabriu período"
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="audit_logs")
    action = models.CharField(max_length=20, choices=Action.choices)
    object_type = models.CharField(max_length=100)
    object_id = models.CharField(max_length=64, blank=True)
    object_repr = models.CharField(max_length=255)
    details = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    class Meta:
        ordering = ["-created_at"]
    def __str__(self):
        return f"{self.get_action_display()} {self.object_repr}"
