from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('add/', views.add_song, name='add_song'),
    path('edit/<int:song_id>/', views.edit_song, name='edit_song'),
    path('delete/<int:song_id>/', views.delete_song, name='delete_song'),
]