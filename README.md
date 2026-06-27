
# Music Analytics Dashboard

A Django-based web application for exploring, analyzing, and visualizing a Spotify-style music dataset. Built as a final project for Software Construction and Development (SCD).

## Features

- **Authentication** — Register, login, logout, and profile pages
- **CRUD Operations** — Add, edit, delete, and view songs
- **Search & Filter** — Search by song/artist, filter by genre, year, and energy level, with sorting
- **Dashboard** — Summary cards, top 10 songs, top 5 genres
- **Charts** — Bar, pie, line, scatter, and histogram visualizations (Chart.js)
- **Auto-Generated Insights** — Plain-language summary statistics
- **Reports** — Export data as CSV or a detailed PDF report

## Tech Stack

- **Backend:** Django
- **Database:** SQLite
- **Frontend:** Bootstrap 5, Chart.js
- **PDF Generation:** ReportLab
- **Data Processing:** Pandas

## Dataset

- **Source:** [Spotify Tracks Dataset — Kaggle](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset)
- **Imported:** 337 songs across 10 balanced genres
- **Genres:** acoustic, rock, hip-hop, jazz, classical, electronic, r-n-b, indie, country, latin

## Project Structure

```
music-dashboard/
├── accounts/                        # Authentication app
├── music_app/                       # Core app
│   ├── management/
│   │   └── commands/
│   │       └── import_songs.py      # Kaggle CSV import command
│   ├── templates/music_app/
│   └── migrations/
├── music_dashboard/                 # Project settings and root URLs
├── templates/
│   ├── base.html
│   └── registration/login.html
├── dataset.csv
├── manage.py
└── requirements.txt
```

## Setup Instructions

### 1. Clone the repository
```
git clone https://github.com/Nimra951/music-dashboard.git
cd music-dashboard
```

### 2. Create and activate virtual environment
```
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Apply migrations
```
python manage.py migrate
```

### 5. Import the Kaggle dataset

Download `dataset.csv` from Kaggle and place it in the project root, then run:
```
python manage.py import_songs
```

### 6. Run the server
```
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`

## Pages

| Page | URL |
|---|---|
| Home | `/` |
| Login | `/accounts/login/` |
| Register | `/accounts/register/` |
| Add Song | `/add/` |
| Search | `/search/` |
| Dashboard | `/dashboard/` |
| Charts | `/charts/` |
| Insights | `/insights/` |
| Export CSV | `/export/csv/` |
| Export PDF | `/export/pdf/` |

## Team

| Member | Responsibility |
|---|---|
| Member 1 | Authentication, database, CRUD |
| Member 2 | Search, filter, dashboard |
| Member 3 | Charts, auto-insights, PDF/CSV reports |

## Notes

- Energy values are decimals between 0.0 and 1.0
- Genres balanced at ~50 songs each for fair chart visualization
- Dataset imported via custom Django management command
