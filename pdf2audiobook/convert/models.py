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

class Chapters(models.Model):
	chapter = models.ForeignKey(Books, on_delete=models.CASCADE)
	chap_no = models.PositiveIntegerField()

class AudioBook(models.Model):
	audio = models.ForeignKey(Chapters, on_delete=models.CASCADE)
	image = models.ImageField()
	audio_file = models.FileField()

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
