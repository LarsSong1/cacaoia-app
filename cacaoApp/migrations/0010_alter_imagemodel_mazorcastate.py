# Generated by Django 4.2.13 on 2024-05-20 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cacaoApp', '0009_imagemodel_imagesdetected'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagemodel',
            name='mazorcaState',
            field=models.CharField(blank=True, max_length=40),
        ),
    ]
