from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Avg, Max, Min
from django.core.paginator import Paginator
from .models import Song, Genre, Artist

# Member 1 functions
def home(request):
    songs = Song.objects.all()
    return render(request, 'music_app/home.html', {'songs': songs})

def profile(request):
    return render(request, 'music_app/profile.html')

def add_song(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        artist_name = request.POST.get('artist')
        genre_name = request.POST.get('genre')

        artist, _ = Artist.objects.get_or_create(name=artist_name)
        genre, _ = Genre.objects.get_or_create(name=genre_name)

        Song.objects.create(title=title, artist=artist, genre=genre)
        return redirect('home')

    return render(request, 'music_app/add_song.html')

def edit_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    return render(request, 'music_app/edit_song.html', {'song': song})

def delete_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    song.delete()
    return redirect('home')

# ---- MEMBER 2 WORK STARTS HERE ----

# Search + Filter + Sort
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

# Dashboard
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