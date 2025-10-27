from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Professor

class ProfessorForm(UserCreationForm):
    matricula = forms.CharField(max_length=20)
    departamento = forms.CharField(max_length=100)
    telefone = forms.CharField(max_length=15, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Professor.objects.create(
                user=user,
                matricula=self.cleaned_data['matricula'],
                departamento=self.cleaned_data['departamento'],
                telefone=self.cleaned_data['telefone']
            )
        return user