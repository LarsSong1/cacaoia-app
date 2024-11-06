from django.db import models
from django.contrib.auth.models import User
import os
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.


class PodCount(models.Model):
    healthyPod = models.IntegerField(default=0)
    moniliaPod = models.IntegerField(default=0)
    pythophoraPod = models.IntegerField(default=0)




class ImageModel(models.Model):
    image = models.ImageField(upload_to='cacaoimages/')
    imagesDetected = models.ImageField(upload_to='cacaodetected/',null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True,  null=True, blank=True)
    mazorcaState = models.CharField(max_length=500, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    podCount_id = models.ForeignKey(PodCount, on_delete=models.CASCADE, null=True, blank=True)
    numHealthy = models.IntegerField(default=0)  # Número de mazorcas saludables
    numMonilia = models.IntegerField(default=0)  # Número de mazorcas con Monilia
    numPythophora = models.IntegerField(default=0)

    def __str__(self):
        return self.mazorcaState





class Fertilizer(models.Model):
    image = models.ImageField(upload_to='plants/')
    title = models.CharField(max_length=100)
    scienceName = models.CharField(max_length=100, blank=True, null=True)
    description = RichTextUploadingField(max_length=8000)
    linkFertilizer = models.CharField(max_length=300, default='https://www.amazon.com/')
    recomendation = models.CharField(max_length=100)
    benefits = RichTextUploadingField(max_length=8000)
    date = models.DateTimeField(default=timezone.now)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title




