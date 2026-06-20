from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Avg, Max, Min
from django.core.paginator import Paginator
from .models import Song, Genre, Artist
from .forms import SongForm


# ---- MEMBER 1 — CRUD ----

def home(request):
    songs = Song.objects.all()
    return render(request, 'music_app/home.html', {'songs': songs})


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


# ---- MEMBER 2 — Search + Filter + Dashboard ----

def search(request):
    songs = Song.objects.all()

    query = request.GET.get('q', '')
    genre = request.GET.get('genre', '')
    year = request.GET.get('year', '')
    energy = request.GET.get('energy', '')
    sort = request.GET.get('sort', 'title')

    if query:
        songs = songs.filter(title__icontains=query) | songs.filter(artist__name__icontains=query)
    if genre:
        songs = songs.filter(genre__name=genre)
    if year:
        songs = songs.filter(year=year)
    if energy == 'high':
        songs = songs.filter(energy__gte=0.7)
    elif energy == 'medium':
        songs = songs.filter(energy__gte=0.4, energy__lt=0.7)
    elif energy == 'low':
        songs = songs.filter(energy__lt=0.4)

    songs = songs.order_by(sort)

    paginator = Paginator(songs, 10)
    page = request.GET.get('page')
    songs = paginator.get_page(page)

    genres = Genre.objects.all()
    return render(request, 'music_app/search.html', {
        'songs': songs, 'genres': genres,
        'query': query, 'selected_genre': genre,
        'selected_year': year, 'selected_energy': energy,
        'selected_sort': sort,
    })


def dashboard(request):
    total_songs = Song.objects.count()
    avg_popularity = Song.objects.aggregate(Avg('popularity'))['popularity__avg'] or 0
    top_songs = Song.objects.order_by('-popularity')[:10]
    top_genres = Genre.objects.annotate(count=Count('song')).order_by('-count')[:5]

    return render(request, 'music_app/dashboard.html', {
        'total_songs': total_songs,
        'avg_popularity': round(avg_popularity, 1),
        'top_songs': top_songs,
        'top_genres': top_genres,
    })