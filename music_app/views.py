from django.shortcuts import render
from .models import Song

def home(request):
    songs = Song.objects.all()
    return render(request, 'music_app/home.html', {'songs': songs})
def profile(request):
    return render(request, 'music_app/profile.html')
from django.shortcuts import redirect
from .forms import SongForm

def add_song(request):
    if request.method == "POST":
        form = SongForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SongForm()

    return render(request, 'music_app/add_song.html', {'form': form})