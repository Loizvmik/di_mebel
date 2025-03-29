from django import forms
from .models import VacancyPerson, Vacancy

class VacancyPersonForm(forms.ModelForm):
    class Meta:
        model = VacancyPerson
        vacancyId = Vacancy

        fields = ['name', 'description', 'phone']
