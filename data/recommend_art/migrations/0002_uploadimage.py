# Generated by Django 3.2.12 on 2022-09-30 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommend_art', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testfield', models.CharField(max_length=200)),
                ('photo', models.FileField(upload_to='')),
            ],
        ),
    ]