from django import forms
from .models import Post

class PostForm(forms.ModelForm):

	class Meta:
		model= Post

		fields=[
			'title',
			'description',
			'date',
			'image',
			'user',
			'company',
		]

		labels = {
			'title': 'Asunto',
			'description': 'Descripción',
			'date': 'Fecha',
			'image': 'Imagen',
			'user': 'Usuario',
			'company': 'Empresa',
		}

		widget={
			'title': forms.TextInput(attrs={'class':'form-control'}),
			'description': forms.TextInput(attrs={'class':'form-control'}),
			'date': forms.TextInput(attrs={'class':'form-control'}),
			'image': forms.TextInput(attrs={'class':'form-control'}),
			'user': forms.TextInput(attrs={'class':'form-control'}),
			'company': forms.TextInput(attrs={'class':'form-control'}),
		}