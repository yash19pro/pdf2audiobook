# Generated by Django 3.1.7 on 2021-05-29 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convert', '0006_auto_20210529_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='index',
            field=models.CharField(default='0: ', max_length=100),
        ),
    ]
