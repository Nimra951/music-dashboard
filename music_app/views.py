from django.http import HttpResponse
import csv
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
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

def charts(request):
    songs = Song.objects.all()

    genre_counts = Genre.objects.annotate(count=Count('song')).values('name', 'count')
    genre_labels = [g['name'] for g in genre_counts]
    genre_data = [g['count'] for g in genre_counts]

    high = songs.filter(energy__gte=0.7).count()
    medium = songs.filter(energy__gte=0.4, energy__lt=0.7).count()
    low = songs.filter(energy__lt=0.4).count()

    year_data = (
        songs.values('year')
        .annotate(avg_pop=Avg('popularity'))
        .order_by('year')
    )
    year_labels = [str(y['year']) for y in year_data]
    year_popularity = [round(y['avg_pop'], 1) if y['avg_pop'] else 0 for y in year_data]

    scatter_data = [
        {'x': s.energy, 'y': s.popularity} for s in songs if s.energy is not None and s.popularity is not None
    ]

    bins = {'2015-2017': 0, '2018-2020': 0, '2021-2023': 0, '2024+': 0}
    for s in songs:
        if s.year:
            if s.year <= 2017:
                bins['2015-2017'] += 1
            elif s.year <= 2020:
                bins['2018-2020'] += 1
            elif s.year <= 2023:
                bins['2021-2023'] += 1
            else:
                bins['2024+'] += 1

    context = {
        'genre_labels': json.dumps(genre_labels),
        'genre_data': json.dumps(genre_data),
        'energy_labels': json.dumps(['High', 'Medium', 'Low']),
        'energy_data': json.dumps([high, medium, low]),
        'year_labels': json.dumps(year_labels),
        'year_popularity': json.dumps(year_popularity),
        'scatter_data': json.dumps(scatter_data),
        'bin_labels': json.dumps(list(bins.keys())),
        'bin_data': json.dumps(list(bins.values())),
    }
    return render(request, 'music_app/charts.html', context)


def insights(request):
    songs = Song.objects.all()
    total = songs.count()

    insights_list = []

    if total > 0:
        top_genre = Genre.objects.annotate(count=Count('song')).order_by('-count').first()
        if top_genre:
            pct = round((top_genre.count / total) * 100, 1)
            insights_list.append(f"{top_genre.name} is the most common genre, representing {pct}% of all songs.")

        avg_pop = songs.aggregate(Avg('popularity'))['popularity__avg']
        if avg_pop:
            insights_list.append(f"The average song popularity is {round(avg_pop, 1)} out of 100.")

        peak_year = (
            songs.values('year')
            .annotate(count=Count('id'))
            .order_by('-count')
            .first()
        )
        if peak_year:
            insights_list.append(f"Music releases peaked in {peak_year['year']} with {peak_year['count']} songs.")

        high_energy_avg = songs.filter(energy__gte=0.7).aggregate(Avg('popularity'))['popularity__avg']
        low_energy_avg = songs.filter(energy__lt=0.4).aggregate(Avg('popularity'))['popularity__avg']
        if high_energy_avg and low_energy_avg and low_energy_avg > 0:
            ratio = round(high_energy_avg / low_energy_avg, 1)
            insights_list.append(f"High energy songs are {ratio}x more popular on average than low energy songs.")

        top_artist = Artist.objects.annotate(count=Count('song')).order_by('-count').first()
        if top_artist:
            insights_list.append(f"{top_artist.name} has the most songs in the dataset ({top_artist.count} songs).")
    else:
        insights_list.append("No data available yet. Add some songs to see insights.")

    return render(request, 'music_app/insights.html', {'insights': insights_list})


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="songs_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Title', 'Artist', 'Genre', 'Year', 'Popularity', 'Energy'])

    songs = Song.objects.all()
    for song in songs:
        writer.writerow([
            song.title,
            song.artist.name,
            song.genre.name,
            song.year,
            song.popularity,
            song.energy,
        ])

    return response


def export_pdf(request):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=20, spaceAfter=20)
    elements.append(Paragraph("Music Analytics Dashboard - Report", title_style))
    elements.append(Spacer(1, 12))

    songs = Song.objects.all()
    total = songs.count()
    avg_pop = songs.aggregate(Avg('popularity'))['popularity__avg'] or 0

    elements.append(Paragraph("Summary", styles['Heading2']))
    summary_data = [
        ['Total Songs', str(total)],
        ['Total Artists', str(Artist.objects.count())],
        ['Total Genres', str(Genre.objects.count())],
        ['Average Popularity', str(round(avg_pop, 1))],
    ]
    summary_table = Table(summary_data, colWidths=[200, 200])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#1DB954')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Genre Distribution", styles['Heading2']))
    genre_counts = Genre.objects.annotate(count=Count('song')).values('name', 'count').order_by('-count')
    genre_data = [['Genre', 'Number of Songs']] + [[g['name'], str(g['count'])] for g in genre_counts]
    genre_table = Table(genre_data, colWidths=[250, 150])
    genre_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#333333')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
    ]))
    elements.append(genre_table)
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Top 10 Songs by Popularity", styles['Heading2']))
    top_songs = songs.order_by('-popularity')[:10]
    song_data = [['Title', 'Artist', 'Genre', 'Popularity']]
    for s in top_songs:
        song_data.append([s.title, s.artist.name, s.genre.name, str(s.popularity)])
    song_table = Table(song_data, colWidths=[150, 130, 100, 80])
    song_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1DB954')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
    ]))
    elements.append(song_table)
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Auto-Generated Insights", styles['Heading2']))
    top_genre = Genre.objects.annotate(count=Count('song')).order_by('-count').first()
    if top_genre and total > 0:
        pct = round((top_genre.count / total) * 100, 1)
        elements.append(Paragraph(f"• {top_genre.name} is the most common genre ({pct}% of songs).", styles['Normal']))
    elements.append(Paragraph(f"• Average song popularity is {round(avg_pop, 1)}.", styles['Normal']))

    doc.build(elements)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="music_report.pdf"'
    return response