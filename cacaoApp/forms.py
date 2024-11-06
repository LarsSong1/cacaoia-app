from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ImageModel, Fertilizer 
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CreateUser(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(CreateUser, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Nombre de usuario'
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        help_texts = {
            'username': _('Solo se aceptan letras o estos caracteres @/./+/-/_ '),
            'password2': _('Vuelve a ingresar la misma contraseña'),
            'password1': _('Tu contraseña no debe ser similar a tu usuario.\n'
                           'Debe contener al menos 8 caracteres\n'
                           'No uses contraseñas habituales\n'
                           'No debe ser solo numeros'),
        }



class ImageUploadForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super(ImageUploadForm, self).__init__(*args, **kwargs)
    #     self.fields['mazorcaState'].label = 'Estado de Mazorca'


    class Meta:
        model = ImageModel  
        fields = ['image', 'mazorcaState']  



class ImageEditForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ['mazorcaState', 'numHealthy', 'numMonilia', 'numPythophora']




class FertilizersForm(forms.ModelForm):

    description = forms.CharField(widget=CKEditorUploadingWidget())
    benefits = forms.CharField(widget=CKEditorUploadingWidget())

    def __init__(self, *args, **kwargs):
        super(FertilizersForm, self).__init__(*args, **kwargs)
        self.fields['image'].label = 'Imagen'
        self.fields['title'].label = 'Titulo Post'
        self.fields['description'].label = 'Descripción Post'
        self.fields['recomendation'].label = 'Fertilizante Recomendado'
        self.fields['linkFertilizer'].label = 'Pagina de Venta Fertilizante'
        self.fields['scienceName'].label = 'Nombre Cientifico'
        self.fields['benefits'].label = 'Importancia del Fertilizante'


    class Meta:
        model = Fertilizer
        fields = ['title', 'scienceName',  'description', 'image', 'benefits', 'recomendation', 'linkFertilizer']