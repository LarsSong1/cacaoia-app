# Generated by Django 4.2.13 on 2024-05-27 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cacaoApp', '0019_fertilizer_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='fertilizer',
            name='scienceName',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
