# Generated by Django 4.2.13 on 2024-05-21 01:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cacaoApp', '0016_alter_imagemodel_mazorcastate'),
    ]

    operations = [
        migrations.CreateModel(
            name='PodCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('healthyPod', models.IntegerField(default=0)),
                ('moniliaPod', models.IntegerField(default=0)),
                ('pythophoraPod', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='imagemodel',
            name='numHealthy',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='imagemodel',
            name='numMonilia',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='imagemodel',
            name='numPythophora',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='imagemodel',
            name='podCount_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cacaoApp.podcount'),
        ),
    ]
