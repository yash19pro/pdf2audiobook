from django import forms
from .models import Books

class BooksForm(forms.ModelForm):
	class Meta:
		model = Books
		fields = ('title', 'file', )