from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUser, FertilizersForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from .models import ImageModel, PodCount, Fertilizer
from .forms import ImageUploadForm, ImageEditForm
from django.views.decorators.csrf import csrf_exempt
from PIL import Image, ImageDraw, ImageFont
import pathlib
import pandas
import numpy as np
import cv2
from django.http import HttpResponseForbidden, JsonResponse
from django.conf import settings
import json
import os
from django.core.files import File
from django.utils.translation import activate
import serial
import random
import time
from django.db.models import Sum 
from pathlib import Path
from urllib.error import HTTPError
from inference_sdk import InferenceHTTPClient
import tempfile
# import urllib.request

# Create your views here.


CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="LK1RiipbOUDaJotyMCuS"
)

# Puerto Serial




# # Gestion de Usuarios
@login_required
def homeView(request):
    users = User.objects.all()
    numberUsers = len(users)
    user_pod_counts = []
    current_user = request.user
    id_user = current_user.id
    print(f'Current User: {current_user}, ID: {current_user.id}') 
    

    for userdata in users:
        images = ImageModel.objects.filter(user_id=userdata)
        total_healthy = sum(image.numHealthy for image in images)
        total_monilia = sum(image.numMonilia for image in images)
        total_pythophora = sum(image.numPythophora for image in images)
        total_pods = total_healthy + total_monilia + total_pythophora
        user_pod_counts.append({
            'id': userdata.id,
            'username': userdata.username,
            'is_superuser': userdata.is_superuser,
            'total_pods': total_pods
        })


    podCounts = PodCount.objects.all()
    print([pod.healthyPod for pod in podCounts])
    totalHealthy = sum(pod.healthyPod for pod in podCounts)    
    totalMonilia = sum(pod.moniliaPod for pod in podCounts)
    totalPythophora = sum(pod.pythophoraPod for pod in podCounts)
    totalMaz = totalMonilia + totalPythophora + totalHealthy
    print(totalMaz)
    print(totalMaz)
    return render(request, 'index.html', {
        # 'usersapp': users, 
        'numberusers': numberUsers,
        'pythoDetects': totalPythophora,
        'moniliaDetects': totalMonilia,
        'healthyDetects': totalHealthy,
        'totalMaz': totalMaz,
        'current_user': current_user,  
        'user_id': id_user,
        'usersapp': user_pod_counts,
    })




def loginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username= username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenido {username}')
                return redirect('home-view')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')


    form = AuthenticationForm()   

    form.fields['username'].label = 'Nombre de usuario'
    form.fields['password'].label = 'Contraseña'
    return render(request, 'login.html', {"form":form})


def createUser(request):
    activate('es')
    if request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login-view')
    else:
        form = CreateUser()

    return render(request, 'createUser.html', {'form': form})


@login_required
def deleteUser(request, user_id):
    if request.method == 'POST':
        if request.user.is_superuser:
            usuario = get_object_or_404(User, pk=user_id)
            usuario.delete()
            return redirect('home-view')
        else: 
            return render('error.html')
    else:
        pass



def userProfile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    # user = request.user  
    analizedImage = ImageModel.objects.filter(user_id=user)
    total_healthy = sum(img.numHealthy for img in analizedImage)
    total_monilia = sum(img.numMonilia for img in analizedImage)
    total_pythophora = sum(img.numPythophora for img in analizedImage)

    is_owner = (request.user == user)
    print(is_owner)

    

    
    return render(request, 'userProfile.html', {
        'user': user,
        'analizedImage': analizedImage,
        'total_healthy': total_healthy,
        'total_monilia': total_monilia,
        'total_pythophora': total_pythophora,
        'is_owner': is_owner
    })


def logoutApp(request):
    logout(request)
    return redirect('login-view')







def fertilizers(request):
    user = request.user
    fertilizerPosts = Fertilizer.objects.all()

    return render(request, 'fertilizers.html',{
        'user': user,
        'posts': fertilizerPosts,
    })


def postFertilizer(request, id):
    post = get_object_or_404(Fertilizer, id=id)
    user = request.user

    return render(request, 'postFertilizer.html', {
        'post': post,
        'user': user
        
    })


def addFertilizers(request):
    activate('es')
    if request.method == 'POST':
        form = FertilizersForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = request.user
            post.save()
            return redirect('fertilizers')
        
    else:
        form = FertilizersForm()
        return render(request, 'addFertilizers.html',{
            'form': form
        })



def editAddFertilizer(request, id):
    post = get_object_or_404(Fertilizer, id=id)
    if request.user != post.user_id:
        # Puedes redirigir a alguna página o mostrar un mensaje de error
        return render(request, 'error.html', {'message': 'No tienes permisos para editar esta barbería.'})
    
    if request.method == 'POST':
        form = FertilizersForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = request.user
            post.save()
            return redirect('fertilizers')  
        
    else:
        form = FertilizersForm(instance=post)
        return render(request, 'editFertilizer.html',{
            'form': form
        })

    
def deleteFertilizer(request, id):
    form = get_object_or_404(Fertilizer, id=id)
    if request.user == form.user_id:
        form.delete()
        return redirect('fertilizers')
    else:
        return HttpResponseForbidden('No Tienes permisos para eliminar este Post')



        
class UploadImage(CreateView):
    model = ImageModel 
    template_name = 'addCocoaPhoto.html'
    fields = ["image"]

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = ImageUploadForm(request.POST, request.FILES)
            if form.is_valid():
                mazorcaimage = form.save(commit=False)
                mazorcaimage.user_id = request.user

                try:
                    imageByIa, mazorcaP, mazorcaM, mazorcaS, detectState = detectCacaoState(mazorcaimage.image)
                except HTTPError as e:
                    if e.code == 403:
                        print("Rate limit exceeded. Waiting before retrying...")
                        time.sleep(200)  # Esperar 200 segundos antes de reintentar
                        return detectCacaoState(mazorcaimage.image)
                    else:
                        raise

                mazorcaimage.numPythophora = mazorcaP
                mazorcaimage.numMonilia = mazorcaM
                mazorcaimage.numHealthy = mazorcaS

                podCount = PodCount.objects.create()

                # Filtrado de Mazorcas
                if mazorcaP >= 1:
                    mazorcaimage.mazorcaState += f'{mazorcaP} M. con Pythophora\n'
                    podCount.pythophoraPod += mazorcaP

                if mazorcaM >= 1:
                    mazorcaimage.mazorcaState += f'{mazorcaM} M. con Monilia\n'
                    podCount.moniliaPod += mazorcaM

                if mazorcaS >= 1:
                    mazorcaimage.mazorcaState += f'{mazorcaS} M. Saludable\n'
                    podCount.healthyPod += mazorcaS

                podCount.save()
                mazorcaimage.podCount_id = podCount

                # Verificar si `imageByIa` es una lista o una imagen única
                if isinstance(imageByIa, list):
                    # Si es una lista, selecciona la primera imagen (ajusta según tus necesidades)
                    first_image = imageByIa[0]
                    processed_image_path = os.path.join(settings.DETECTION_MEDIA_ROOT, 'mydetect.png')
                    first_image.save(processed_image_path)
                else:
                    # Si es una sola imagen, guarda directamente
                    processed_image_path = os.path.join(settings.DETECTION_MEDIA_ROOT, 'mydetect.png')
                    imageByIa.save(processed_image_path)

                processed_image = File(open(processed_image_path, 'rb'))
                mazorcaimage.imagesDetected.save('mydetect.png', processed_image, save=False)

                # Asignar la nueva imagen procesada al campo de imagen del modelo
                mazorcaimage.image.name = 'mydetect.png'
                
                # Guardar la instancia de mazorcaimage
                mazorcaimage.save()
                user_now = request.user.id
                return redirect('user-profile', user_id=user_now)
        else:       
            form = ImageUploadForm()
        return render(request, 'addCocoaPhoto.html', {'form': form})



class EditUploadImage(UpdateView):
    model = ImageModel
    template_name = 'editCocoaPhoto.html'
    form_class = ImageEditForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, request.FILES, instance=self.object)
        if form.is_valid():
            mazorcaimage = form.save(commit=False)
            mazorcaimage.user_id = request.user
            podCount = mazorcaimage.podCount_id

            # Actualizar los valores con los nuevos datos manuales
            podCount.healthyPod = mazorcaimage.numHealthy
            podCount.moniliaPod = mazorcaimage.numMonilia
            podCount.pythophoraPod = mazorcaimage.numPythophora

            podCount.save()
         
            mazorcaimage.save()
            return redirect('user-profile', user_id=request.user.id)
        return render(request, self.template_name, {'form': form})

    def get_object(self, queryset=None):
        # Asegúrate de obtener el objeto correcto para editar
        return get_object_or_404(ImageModel, pk=self.kwargs.get('pk'))




def deleteRegisterC(request, user_id):
    imgToDelete = get_object_or_404(ImageModel, pk=user_id)
    
    # Verificar que el usuario tiene permiso para eliminar la imagen
    if request.user == imgToDelete.user_id:
        # Primero, eliminar el archivo de imagen del sistema de archivos
        if imgToDelete.image:
            try:
                cacao_image_path = os.path.join(settings.MEDIA_ROOT, imgToDelete.image.name)
                detected_image_path = os.path.join(settings.DETECTION_MEDIA_ROOT, imgToDelete.imagesDetected.name)

                # Eliminar la imagen de cacaoimages
                if os.path.isfile(cacao_image_path):
                    try:
                        os.remove(cacao_image_path)
                        print(f'Eliminada la imagen de cacaoimages: {cacao_image_path}')
                    except Exception as e:
                        print(f'Error al eliminar la imagen de cacaoimages: {e}')

                # Eliminar la imagen de cacaodetected
                if os.path.isfile(detected_image_path):
                    try:
                        os.remove(detected_image_path)
                        print(f'Eliminada la imagen de cacaodetected: {detected_image_path}')
                    except Exception as e:
                        print(f'Error al eliminar la imagen de cacaodetected: {e}')
            except Exception as e:
                print(f'Error al eliminar la imagen: {e}')

        # Actualizar el conteo de pods antes de eliminar la imagen
        podCount = imgToDelete.podCount_id
        if podCount:
            podCount.healthyPod -= imgToDelete.numHealthy
            podCount.moniliaPod -= imgToDelete.numMonilia
            podCount.pythophoraPod -= imgToDelete.numPythophora
            podCount.save()

        # Eliminar el registro de la base de datos
        imgToDelete.delete()
        return redirect('user-profile', user_id=request.user.id)

    else:
        return HttpResponseForbidden('No tienes permiso de editar estos datos')

def showError(request):
    return render(request, 'error.html')




def detectCacaoState(img_path):
    img = Image.open(img_path)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    draw = ImageDraw.Draw(img)  # Move this line after the conversion

    # Create a temporary file for storing the image in JPEG format
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
        temp_jpg_path = temp_file.name
        img.save(temp_jpg_path, format="JPEG", quality=85)

    result = CLIENT.infer(temp_jpg_path, model_id="cocoa-disease-zl3cl/1")
    print(result)

    numMazorcaP = 0
    numMazorcaM = 0
    numMazorcaS = 0
    noDetections = True

    mazorcas = []

    font = ImageFont.load_default()
    for prediction in result['predictions']:
        x0 = prediction['x'] - prediction['width'] / 2
        y0 = prediction['y'] - prediction['height'] / 2
        x1 = prediction['x'] + prediction['width'] / 2
        y1 = prediction['y'] + prediction['height'] / 2
        confi = prediction['confidence']
        cla = prediction['class_id']

        # Añadir cada mazorca con los datos necesarios
        mazorcas.append({
            'x0': x0,
            'y0': y0,
            'x1': x1,
            'y1': y1,
            'confianza': confi,
            'clase': cla
        })

        # Dibujar el rectángulo en la imagen
        draw.rectangle([x0, y0, x1, y1], outline="red", width=3)

        # Contar según la clase detectada si la confianza es mayor a 0.5
        if confi > 0.50:
            noDetections = False
            label = ""
            if cla == 0:
                numMazorcaS += 1
                label = "Saludable"
                print('Mazorca Saludable')
            elif cla == 1:
                numMazorcaM += 1
                label = "Con Monilia"
                print('Mazorca con Monilia')
            elif cla == 2:
                numMazorcaP += 1
                label = "Con Phytophthora"
                print('Mazorca con Phytophthora')

            # Dibujar el cuadro de detección
            draw.rectangle([x0, y0, x1, y1], outline="red", width=2)
            # Añadir el texto con el nombre de la detección
            draw.text((x0, y0), label, fill="red", font=font)

    # Retornar la imagen procesada y los datos
    return img, numMazorcaP, numMazorcaM, numMazorcaS, noDetections