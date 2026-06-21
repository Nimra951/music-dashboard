from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_song, name='add_song'),
    path('edit/<int:song_id>/', views.edit_song, name='edit_song'),
    path('delete/<int:song_id>/', views.delete_song, name='delete_song'),
    path('search/', views.search, name='search'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('charts/', views.charts, name='charts'),
    path('insights/', views.insights, name='insights'),
    path('export/csv/', views.export_csv, name='export_csv'),
    path('export/pdf/', views.export_pdf, name='export_pdf'),
]