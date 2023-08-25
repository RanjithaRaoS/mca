from django import forms
from .models import Exercise, Training
from django.forms import inlineformset_factory

class AddExercisesForm(forms.Form):
    exercise_name = forms.CharField(label='Exercise Name', max_length=100)
    weight_kg = forms.FloatField(label='Weight (kg)')
    weight_per = forms.ChoiceField(choices=[('total', 'Total'), ('per hand', 'Per Hand')])
    series = forms.IntegerField(label='Series')
    reps = forms.CharField(label='Reps', max_length=100)




class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ['name', 'started', 'ended']
        widgets = {
            'started': forms.TextInput(attrs={'type': 'date'}),
            'ended': forms.TextInput(attrs={'type': 'date'}),
        }

    started = forms.DateField(label='Start Date', required=False)  # Set required=False
    ended = forms.DateField(label='End Date', required=False)  # Set required=False
