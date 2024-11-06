
from django.urls import path
from .views import homeView, loginView, createUser, userProfile, logoutApp, showError, deleteUser, fertilizers, UploadImage, deleteRegisterC, EditUploadImage, addFertilizers, postFertilizer, editAddFertilizer, deleteFertilizer


urlpatterns = [
    path('', loginView, name='login-view'),
    path('dashboard', homeView, name='home-view'),
    path('create-user/', createUser, name='create-user'),
    path('user-profile/<int:user_id>/', userProfile, name='user-profile'),
    path('logout-app', logoutApp, name='logout'), 
    path('error/', showError, name='error'),
    path('user/<int:user_id>/', deleteUser, name='delete-user'),
    path('fertilizers/', fertilizers, name="fertilizers"),
    path('post-fertilizer/<int:id>/', postFertilizer, name="post-fertilizer"),
    path('edit-fertilizer/<int:id>/', editAddFertilizer, name="edit-fertilizer"),
    path('add-fertilizers/', addFertilizers, name='add-fertilizers'),
    path('delete-fertilizers/<int:id>/', deleteFertilizer, name='delete-fertilizer'),
    path('upload-image/', UploadImage.as_view(), name='upload-image'),
    path('delete-image/<int:user_id>/', deleteRegisterC, name='delete-image'),
    path('edit-upload-image/<int:pk>/', EditUploadImage.as_view(), name='edit-upload-image'),
   
   
]
