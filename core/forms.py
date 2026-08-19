from decimal import Decimal, InvalidOperation
from pathlib import Path
from django import forms
from django.core.exceptions import ValidationError

ALLOWED_DOCUMENT_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}
MAX_DOCUMENT_SIZE = 10 * 1024 * 1024

class BRLDecimalField(forms.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_digits", 14)
        kwargs.setdefault("decimal_places", 2)
        super().__init__(*args, **kwargs)
    def to_python(self, value):
        if value in self.empty_values:
            return None
        if isinstance(value, str):
            normalized = value.strip().replace("R$", "").replace(" ", "").replace("\u00a0", "")
            if "," in normalized:
                normalized = normalized.replace(".", "").replace(",", ".")
            try:
                value = Decimal(normalized)
            except InvalidOperation as exc:
                raise ValidationError("Informe um valor válido.") from exc
        return super().to_python(value)

def validate_document_upload(upload):
    if not upload:
        return upload
    extension = Path(upload.name).suffix.lower()
    if extension not in ALLOWED_DOCUMENT_EXTENSIONS:
        raise ValidationError("Envie um arquivo PDF, JPG, JPEG ou PNG.")
    if upload.size > MAX_DOCUMENT_SIZE:
        raise ValidationError("O arquivo deve ter no máximo 10 MB.")
    position = upload.tell()
    signature = upload.read(12)
    upload.seek(position)
    signatures = {".pdf": (b"%PDF-",), ".jpg": (b"\xff\xd8\xff",), ".jpeg": (b"\xff\xd8\xff",), ".png": (b"\x89PNG\r\n\x1a\n",)}
    if not any(signature.startswith(item) for item in signatures[extension]):
        raise ValidationError("O conteúdo do arquivo não corresponde ao formato informado.")
    return upload
