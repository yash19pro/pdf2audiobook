from django import forms
from .models import Books, Editorial

class BooksForm(forms.ModelForm):
	class Meta:
		model = Books
		fields = ('title', 'file', )

class EditorialForm(forms.ModelForm):
	class Meta:
		model = Editorial
		fields = ('title', 'file', )