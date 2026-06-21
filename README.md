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

## Project Structure

```
music-dashboard/
├── accounts/              # Authentication app (login, register, logout, profile)
├── music_app/              # Core app (songs, CRUD, search, dashboard, charts, insights)
│   ├── templates/music_app/
│   └── migrations/
├── music_dashboard/        # Project settings and root URLs
├── templates/
│   ├── base.html            # Shared layout, navbar, theme
│   └── registration/login.html
├── db.sqlite3
├── manage.py
└── requirements.txt
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Nimra951/music-dashboard.git
cd music-dashboard
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If you hit an execution policy error on Windows:

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create a superuser (optional, for admin access)

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## Usage

| Page | URL |
|---|---|
| Home | `/` |
| Login | `/accounts/login/` |
| Register | `/accounts/register/` |
| Profile | `/accounts/profile/` |
| Add Song | `/add/` |
| Search | `/search/` |
| Dashboard | `/dashboard/` |
| Charts | `/charts/` |
| Insights | `/insights/` |
| Export CSV | `/export/csv/` |
| Export PDF | `/export/pdf/` |

## Adding Data

Use the Django admin panel to add Artists and Genres before adding songs, since songs reference them via dropdowns:

```bash
python manage.py createsuperuser
```

Then visit `/admin/` and add Artists and Genres first, followed by Songs.

## Team

| Member | Responsibility |
|---|---|
| Member 1 | Authentication, database, CRUD |
| Member 2 | Search, filter, dashboard |
| Member 3 | Charts, auto-insights, PDF/CSV reports |

## Notes

- Energy values are decimals between 0.0 and 1.0 (e.g. 0.8 for high energy).
- The PDF report includes a summary, genre distribution table, top 10 songs, and auto-generated insights.