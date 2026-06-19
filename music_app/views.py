from django.shortcuts import render, redirect, get_object_or_404
from .models import Song


def home(request):
    songs = Song.objects.all()
    return render(request, 'music_app/home.html', {'songs': songs})


def add_song(request):
    if request.method == "POST":
        title = request.POST.get('title')
        artist = request.POST.get('artist')
        genre = request.POST.get('genre')

        Song.objects.create(title=title, artist=artist, genre=genre)
        return redirect('home')

    return render(request, 'music_app/add_song.html')


def edit_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)

    if request.method == "POST":
        song.title = request.POST.get('title')
        song.artist = request.POST.get('artist')
        song.genre = request.POST.get('genre')
        song.save()
        return redirect('home')

    return render(request, 'music_app/edit_song.html', {'song': song})


def delete_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    song.delete()
    return redirect('home')