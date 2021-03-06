from django.db import models

# Create your models here.

class Books(models.Model):
	title = models.CharField(max_length=100)
	file = models.FileField(upload_to='books')
	index = models.CharField(max_length=100, default="editorial")

	def __str__(self):
		return self.title

	def delete(self, *args, **kwargs):
		self.file.delete()
		super().delete(*args, **kwargs)
