from django import forms
from .models import JobApplication
from django.contrib.auth.models import User


class CandidateRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    help_texts = {
            'username': '',
            'password': '',
        }
    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password")
        p2 = cleaned_data.get("confirm_password")

        if p1 != p2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data



class ApplicationForm(forms.ModelForm):

    class Meta:
        model = JobApplication
        fields = ['name', 'email', 'phone', 'resume']
        widgets = {
            'resume': forms.FileInput(),
        }
