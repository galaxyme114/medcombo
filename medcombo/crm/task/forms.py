from django import forms
from .models import Task, CallTask

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        call = forms.ModelChoiceField(queryset=CallTask.objects.filter(language_id=4), required='true')
        fields = (
            'opportunity', 
            'responsible',
            'deadline',
            'priority',
            'notes',
            'call'
        )
        widgets = {
            'deadline': forms.TextInput(attrs={'type':'date', 'class':'form-control','required':'true'}),
        }
