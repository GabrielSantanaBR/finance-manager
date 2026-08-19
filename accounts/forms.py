from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User

class StyledAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control", "placeholder": "Seu usuário", "autofocus": True})
        self.fields["password"].widget.attrs.update({"class": "form-control", "placeholder": "Sua senha"})

class ManagedUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email", "role", "ministry")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["ministry"].label = "Departamento"
        for field in self.fields.values(): field.widget.attrs.setdefault("class", "form-control")
        self.fields["role"].widget.attrs["class"] = "form-select"
        self.fields["ministry"].widget.attrs["class"] = "form-select"
