
from django.contrib.auth.models import User
import os 
from django.db import migrations


def create_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    if not User.objects.filter(username='cacaouseradmin').exists():
        User.objects.create_superuser(
            username='cacaouseradmin',
            email='jairgavilanezcell@gmail.com',
            password=os.environ.get('DJANGO_ADMIN_PASSWORD', 'cacao2024app')
        )



class Migration(migrations.Migration):

    dependencies = [
        ('cacaoApp', '0025_alter_fertilizer_benefits_and_more'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
