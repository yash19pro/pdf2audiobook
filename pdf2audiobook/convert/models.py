from django.db import models

# Create your models here.
class Books(models.Model):
	title = models.CharField(max_length=100)
	file = models.FileField(upload_to='books/')

	def __str__(self):
		return self.title

	def delete(self, *args, **kwargs):
		self.file.delete()
		super().delete(*args, **kwargs)

class Audiobooks(models.Model):
	title = models.ForeignKey(Books, on_delete=models.CASCADE)
	audiobook = models.FileField(upload_to="audiobook_books/")

	def __str__(self):
		return self.title

class Editorial(models.Model):
	title = models.CharField(max_length=100)
	file = models.FileField(upload_to='editorials/')

	def __str__(self):
		return self.title

	def delete(self, *args, **kwargs):
		self.file.delete()
		super().delete(*args, **kwargs)

class Editorial_Audiobooks(models.Model):
	title = models.ForeignKey(Editorial, on_delete=models.CASCADE)
	audiobook = models.FileField(upload_to="audiobook_editorials/")

	def __str__(self):
		return self.title
