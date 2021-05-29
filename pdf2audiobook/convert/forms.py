from django import forms
from .models import Books, Editorial

class BooksForm(forms.ModelForm):
	class Meta:
		model = Books
		fields = ('title', 'file', 'index')

class EditorialForm(forms.ModelForm):
	class Meta:
		model = Editorial
		fields = ('title', 'file', )