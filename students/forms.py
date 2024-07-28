from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Fees_detail

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class fees_details_form(forms.ModelForm):
    class Meta:
        model = Fees_detail
        fields = [
            "type_of_fees", "semester_number","reference_id",
            "paid_date", "fees_amount", "fees_receipt"]
        widgets = {
            'paid_date': forms.SelectDateWidget,
        }
        