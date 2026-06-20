from django.shortcuts import render, redirect, get_object_or_404
from .models import Song
from .forms import SongForm
<<<<<<< HEAD
=======

>>>>>>> dad60f72e01301b22d79db321470b700c0a7c119

def home(request):
    songs = Song.objects.all()
    return render(request, 'music_app/home.html', {'songs': songs})

<<<<<<< HEAD
def profile(request):
    return render(request, 'music_app/profile.html')
=======

def profile(request):
    return render(request, 'music_app/profile.html')

>>>>>>> dad60f72e01301b22d79db321470b700c0a7c119

def add_song(request):
    if request.method == "POST":
        form = SongForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SongForm()

    return render(request, 'music_app/add_song.html', {'form': form})

<<<<<<< HEAD
def edit_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)

=======

def edit_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
>>>>>>> dad60f72e01301b22d79db321470b700c0a7c119
    if request.method == "POST":
        form = SongForm(request.POST, instance=song)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SongForm(instance=song)

<<<<<<< HEAD
    return render(request, 'music_app/edit_song.html', {'form': form})

def delete_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)

=======
    return render(request, 'music_app/edit_song.html', {'form': form, 'song': song})


def delete_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
>>>>>>> dad60f72e01301b22d79db321470b700c0a7c119
    if request.method == "POST":
        song.delete()
        return redirect('home')

    return render(request, 'music_app/delete_song.html', {'song': song})