# Generated by Django 3.1.7 on 2021-04-25 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('convert', '0004_auto_20210425_0717'),
    ]

    operations = [
        migrations.CreateModel(
            name='AudioBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('audio_file', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Chapters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chap_no', models.PositiveIntegerField()),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='convert.books')),
            ],
        ),
        migrations.DeleteModel(
            name='Audiobooks',
        ),
        migrations.AddField(
            model_name='audiobook',
            name='audio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='convert.chapters'),
        ),
    ]
