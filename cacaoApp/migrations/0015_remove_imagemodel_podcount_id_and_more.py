# Generated by Django 4.2.13 on 2024-05-21 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cacaoApp', '0014_alter_imagemodel_mazorcastate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagemodel',
            name='podCount_id',
        ),
        migrations.AlterField(
            model_name='imagemodel',
            name='mazorcaState',
            field=models.CharField(max_length=500),
        ),
        migrations.DeleteModel(
            name='PodCount',
        ),
    ]
