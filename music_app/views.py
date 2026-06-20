from django.shortcuts import render, redirect, get_object_or_404  # type: ignore
from .models import Song
from .forms import SongForm


def home(request):
    songs = Song.objects.all()
    return render(request, 'music_app/home.html', {'songs': songs})


def profile(request):
    return render(request, 'music_app/profile.html')


def add_song(request):
    if request.method == "POST":
        form = SongForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SongForm()

    return render(request, 'music_app/add_song.html', {'form': form})


def edit_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    if request.method == "POST":
        form = SongForm(request.POST, instance=song)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SongForm(instance=song)

    return render(request, 'music_app/edit_song.html', {'form': form, 'song': song})


def delete_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    if request.method == "POST":
        song.delete()
        return redirect('home')

    return render(request, 'music_app/delete_song.html', {'song': song})