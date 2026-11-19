from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, Record


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    department = forms.CharField(max_length=100)
    designation = forms.CharField(max_length=100, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=True)
        Profile.objects.create(
            user=user,
            department=self.cleaned_data['department'],
            designation=self.cleaned_data['designation'],
        )
        return user


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['record_type', 'title', 'year', 'details', 'proof']
        widgets = {'details': forms.Textarea(attrs={'rows': 3})}
