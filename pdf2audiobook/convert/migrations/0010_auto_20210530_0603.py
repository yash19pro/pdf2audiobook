# Generated by Django 3.1.7 on 2021-05-30 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convert', '0009_auto_20210529_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='editorial',
            name='file',
            field=models.FileField(upload_to='editorials'),
        ),
    ]
