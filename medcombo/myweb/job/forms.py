from django import forms
from cities_light.models import Country
from cities_light.models import City
from .models import Job, Contract, Workday, Resume
from dal import autocomplete
from django.forms import ModelChoiceField
from dal import forward


class JobForm(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required='true')
    type_contract = forms.ModelChoiceField(queryset=Contract.objects.filter(language_id=4), required='true')
    work_day = forms.ModelChoiceField(queryset=Workday.objects.filter(language_id=4), required='true')
    CHOICES = (('0', '0'),('1', '1'),('100', '100'),('500', '500'),('1000', '1000'),('5000', '5000'),('10000', '10000'),('50000', '50000'), ('100000', '100000'),)
    salary_minimum = forms.ChoiceField(choices=CHOICES)
    salary_maximum = forms.ChoiceField(choices=CHOICES)

    class Meta:
        model = Job
        fields = ('user', 'name', 'places','city', 'country', 'assignment', 'requirements', 'advantages', 'show', 'salary_minimum', 'salary_maximum')
        widgets = {
            'city': autocomplete.ModelSelect2(url='city-autocomplete-job', forward=['country']),
            'assignment': forms.Textarea(attrs={'style':'resize: none;', 'rows':'5', 'required':'required'}),
            'requirements': forms.Textarea(attrs={'style':'resize: none;', 'rows':'5', 'required':'required'}),
            'advantages': forms.Textarea(attrs={'style':'resize: none;', 'rows':'5', 'required':'required'}),
            'show': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }

class JobForm_en(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required='true')
    type_contract = forms.ModelChoiceField(queryset=Contract.objects.filter(language_id=3), required='true')
    work_day = forms.ModelChoiceField(queryset=Workday.objects.filter(language_id=3), required='true')
    CHOICES = (('0', '0'),('1', '1'),('100', '100'),('500', '500'),('1000', '1000'),('5000', '5000'),('10000', '10000'),('50000', '50000'), ('100000', '100000'),)
    salary_minimum = forms.ChoiceField(choices=CHOICES)
    salary_maximum = forms.ChoiceField(choices=CHOICES)

    class Meta:
        model = Job
        fields = ('user', 'name', 'places','city', 'country', 'assignment', 'requirements', 'advantages', 'show', 'salary_minimum', 'salary_maximum')
        widgets = {
            'city': autocomplete.ModelSelect2(url='city-autocomplete-job', forward=['country']),
            'assignment': forms.Textarea(attrs={'style':'resize: none;', 'rows':'5', 'required':'required'}),
            'requirements': forms.Textarea(attrs={'style':'resize: none;', 'rows':'5', 'required':'required'}),
            'advantages': forms.Textarea(attrs={'style':'resize: none;', 'rows':'5', 'required':'required'}),
            'show': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }

class JobForm_ja(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required='true')
    type_contract = forms.ModelChoiceField(queryset=Contract.objects.filter(language_id= 9), required='true')
    work_day = forms.ModelChoiceField(queryset=Workday.objects.filter(language_id=9), required='true')
    CHOICES = (('0', '0'),('1', '1'),('100', '100'),('500', '500'),('1000', '1000'),('5000', '5000'),('10000', '10000'),('50000', '50000'), ('100000', '100000'),)
    salary_minimum = forms.ChoiceField(choices=CHOICES)
    salary_maximum = forms.ChoiceField(choices=CHOICES)

    class Meta:
        model = Job
        fields = ('user', 'name', 'places','city', 'country', 'assignment', 'requirements', 'advantages', 'type_contract', 'work_day', 'show', 'salary_minimum', 'salary_maximum')
        widgets = {
            'city': autocomplete.ModelSelect2(url='city-autocomplete-job', forward=['country']),
            'assignment': forms.Textarea(attrs={'style':'resize: none;', 'rows':'5', 'required':'required'}),
            'requirements': forms.Textarea(attrs={'style':'resize: none;', 'rows':'5', 'required':'required'}),
            'advantages': forms.Textarea(attrs={'style':'resize: none;', 'rows':'5', 'required':'required'}),
            'show': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }

class JobForm_it(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required='true')
    type_contract = forms.ModelChoiceField(queryset=Contract.objects.filter(language_id= 6), required='true')
    work_day = forms.ModelChoiceField(queryset=Workday.objects.filter(language_id=6), required='true')
    CHOICES = (('0', '0'),('1', '1'),('100', '100'),('500', '500'),('1000', '1000'),('5000', '5000'),('10000', '10000'),('50000', '50000'), ('100000', '100000'),)
    salary_minimum = forms.ChoiceField(choices=CHOICES)
    salary_maximum = forms.ChoiceField(choices=CHOICES)

    class Meta:
        model = Job
        fields = ('user', 'name', 'places','city', 'country', 'assignment', 'requirements', 'advantages', 'type_contract', 'work_day', 'show', 'salary_minimum', 'salary_maximum')
        widgets = {
            'city': autocomplete.ModelSelect2(url='city-autocomplete-job', forward=['country']),
            'assignment': forms.Textarea(attrs={'style':'resize: none;', 'rows':'5', 'required':'required'}),
            'requirements': forms.Textarea(attrs={'style':'resize: none;', 'rows':'5', 'required':'required'}),
            'advantages': forms.Textarea(attrs={'style':'resize: none;', 'rows':'5', 'required':'required'}),
            'show': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }

class JobForm_pt(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required='true')
    type_contract = forms.ModelChoiceField(queryset=Contract.objects.filter(language_id= 7), required='true')
    work_day = forms.ModelChoiceField(queryset=Workday.objects.filter(language_id=7), required='true')
    CHOICES = (('0', '0'),('1', '1'),('100', '100'),('500', '500'),('1000', '1000'),('5000', '5000'),('10000', '10000'),('50000', '50000'), ('100000', '100000'),)
    salary_minimum = forms.ChoiceField(choices=CHOICES)
    salary_maximum = forms.ChoiceField(choices=CHOICES)

    class Meta:
        model = Job
        fields = ('user', 'name', 'places','city', 'country', 'assignment', 'requirements', 'advantages', 'type_contract', 'work_day', 'show', 'salary_minimum', 'salary_maximum')
        widgets = {
            'city': autocomplete.ModelSelect2(url='city-autocomplete-job', forward=['country']),
            'assignment': forms.Textarea(attrs={'style':'resize: none;', 'rows':'5', 'required':'required'}),
            'requirements': forms.Textarea(attrs={'style':'resize: none;', 'rows':'5', 'required':'required'}),
            'advantages': forms.Textarea(attrs={'style':'resize: none;', 'rows':'5', 'required':'required'}),
            'show': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }

class JobForm_de(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required='true')
    type_contract = forms.ModelChoiceField(queryset=Contract.objects.filter(language_id= 2), required='true')
    work_day = forms.ModelChoiceField(queryset=Workday.objects.filter(language_id=2), required='true')
    CHOICES = (('0', '0'),('1', '1'),('100', '100'),('500', '500'),('1000', '1000'),('5000', '5000'),('10000', '10000'),('50000', '50000'), ('100000', '100000'),)
    salary_minimum = forms.ChoiceField(choices=CHOICES)
    salary_maximum = forms.ChoiceField(choices=CHOICES)

    class Meta:
        model = Job
        fields = ('user', 'name', 'places','city', 'country', 'assignment', 'requirements', 'advantages', 'type_contract', 'work_day', 'show', 'salary_minimum', 'salary_maximum')
        widgets = {
            'city': autocomplete.ModelSelect2(url='city-autocomplete-job', forward=['country']),
            'assignment': forms.Textarea(attrs={'style':'resize: none;', 'rows':'5', 'required':'required'}),
            'requirements': forms.Textarea(attrs={'style':'resize: none;', 'rows':'5', 'required':'required'}),
            'advantages': forms.Textarea(attrs={'style':'resize: none;', 'rows':'5', 'required':'required'}),
            'show': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }

class JobForm_fr(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required='true')
    type_contract = forms.ModelChoiceField(queryset=Contract.objects.filter(language_id= 5), required='true')
    work_day = forms.ModelChoiceField(queryset=Workday.objects.filter(language_id=5), required='true')
    CHOICES = (('0', '0'),('1', '1'),('100', '100'),('500', '500'),('1000', '1000'),('5000', '5000'),('10000', '10000'),('50000', '50000'), ('100000', '100000'),)
    salary_minimum = forms.ChoiceField(choices=CHOICES)
    salary_maximum = forms.ChoiceField(choices=CHOICES)

    class Meta:
        model = Job
        fields = ('user', 'name', 'places','city', 'country', 'assignment', 'requirements', 'advantages', 'type_contract', 'work_day', 'show', 'salary_minimum', 'salary_maximum')
        widgets = {
            'city': autocomplete.ModelSelect2(url='city-autocomplete-job', forward=['country']),
            'assignment': forms.Textarea(attrs={'style':'resize: none;', 'rows':'5', 'required':'required'}),
            'requirements': forms.Textarea(attrs={'style':'resize: none;', 'rows':'5', 'required':'required'}),
            'advantages': forms.Textarea(attrs={'style':'resize: none;', 'rows':'5', 'required':'required'}),
            'show': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }

class JobForm_zh(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required='true')
    type_contract = forms.ModelChoiceField(queryset=Contract.objects.filter(language_id= 8), required='true')
    work_day = forms.ModelChoiceField(queryset=Workday.objects.filter(language_id=8), required='true')
    CHOICES = (('0', '0'),('1', '1'),('100', '100'),('500', '500'),('1000', '1000'),('5000', '5000'),('10000', '10000'),('50000', '50000'), ('100000', '100000'),)
    salary_minimum = forms.ChoiceField(choices=CHOICES)
    salary_maximum = forms.ChoiceField(choices=CHOICES)

    class Meta:
        model = Job
        fields = ('user', 'name', 'places','city', 'country', 'assignment', 'requirements', 'advantages', 'type_contract', 'work_day', 'show', 'salary_minimum', 'salary_maximum')
        widgets = {
            'city': autocomplete.ModelSelect2(url='city-autocomplete-job', forward=['country']),
            'assignment': forms.Textarea(attrs={'style':'resize: none;', 'rows':'5', 'required':'required'}),
            'requirements': forms.Textarea(attrs={'style':'resize: none;', 'rows':'5', 'required':'required'}),
            'advantages': forms.Textarea(attrs={'style':'resize: none;', 'rows':'5', 'required':'required'}),
            'show': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }

class JobForm_zhh(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required='true')
    type_contract = forms.ModelChoiceField(queryset=Contract.objects.filter(language_id= 1), required='true')
    work_day = forms.ModelChoiceField(queryset=Workday.objects.filter(language_id=1), required='true')
    CHOICES = (('0', '0'),('1', '1'),('100', '100'),('500', '500'),('1000', '1000'),('5000', '5000'),('10000', '10000'),('50000', '50000'), ('100000', '100000'),)
    salary_minimum = forms.ChoiceField(choices=CHOICES)
    salary_maximum = forms.ChoiceField(choices=CHOICES)

    class Meta:
        model = Job
        fields = ('user', 'name', 'places','city', 'country', 'assignment', 'requirements', 'advantages', 'type_contract', 'work_day', 'show', 'salary_minimum', 'salary_maximum')
        widgets = {
            'city': autocomplete.ModelSelect2(url='city-autocomplete-job', forward=['country']),
            'assignment': forms.Textarea(attrs={'style':'resize: none;', 'rows':'5', 'required':'required'}),
            'requirements': forms.Textarea(attrs={'style':'resize: none;', 'rows':'5', 'required':'required'}),
            'advantages': forms.Textarea(attrs={'style':'resize: none;', 'rows':'5', 'required':'required'}),
            'show': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }

class ResumeForm(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required='true')

    class Meta:
        model = Resume
        fields = ('participant', 'offer', 'age', 'phone', 'city', 'country', 'experience', 'education', 'languages', 'computer', 'another', 'pdf')
        widgets = {
            'city': autocomplete.ModelSelect2(url='city-autocomplete-job', forward=['country']),
            'experience': forms.Textarea(attrs={'style':'resize: none;', 'class': 'form-control', 'rows':'5','required':'true'}),
            'education': forms.Textarea(attrs={'style':'resize: none;', 'class': 'form-control', 'rows':'5','required':'true'}),
            'languages': forms.Textarea(attrs={'style':'resize: none;', 'class': 'form-control', 'rows':'5'}),
            'computer': forms.Textarea(attrs={'style':'resize: none;', 'class': 'form-control', 'rows':'5'}),
            'another': forms.Textarea(attrs={'style':'resize: none;', 'class': 'form-control','rows':'5'}),
            'age': forms.NumberInput(attrs={'class': 'form-control','min':18,'max':100,'required':'true'}),
        }

class JobFilterForm(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required='true')
    type_contract = forms.ModelChoiceField(queryset=Contract.objects.all(), required='true')
    work_day = forms.ModelChoiceField(queryset=Workday.objects.all(), required='true')
    CHOICES = (('0', '0'),('1', '1'),('100', '100'),('500', '500'),('1000', '1000'),('5000', '5000'),('10000', '10000'),('50000', '50000'), ('100000', '100000'),)
    salary_minimum = forms.ChoiceField(choices=CHOICES)
    salary_maximum = forms.ChoiceField(choices=CHOICES)

    class Meta:
        model = Job
        fields = ('user', 'name', 'places','city', 'country', 'assignment', 'requirements', 'advantages', 'show', 'salary_minimum', 'salary_maximum')
        widgets = {
            'city': autocomplete.ModelSelect2(url='city-autocomplete-job', forward=['country']),
            'assignment': forms.Textarea(attrs={'style':'resize: none;', 'rows':'5'}),
            'requirements': forms.Textarea(attrs={'style':'resize: none;', 'rows':'5'}),
            'advantages': forms.Textarea(attrs={'style':'resize: none;', 'rows':'5'}),
            'show': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }