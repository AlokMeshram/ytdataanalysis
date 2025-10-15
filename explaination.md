# Project Explaination: YouTube Analytics Dashboard

This document is a presentation-ready explanation of the entire project. Use it for your submission and viva. It includes an executive summary, architecture, data flow, code walkthrough, how to run, libraries, likely viva questions, and a short demo script.

---

## 1) Executive summary (what it does)
- A Flask web app that turns a CSV of global YouTube channel stats into an interactive dashboard.
- The CSV is cleaned and loaded into a local SQLite database, then visualized in the browser:
  - Pie chart: Top 5 countries by total views
  - Bar chart: Top 10 channels by subscribers
  - Country selector + table: Top 5 channels for the selected country
- Handles messy CSV variations (different column names and number formats like 2.3M, 120K).

## 2) Why this is useful (problem it solves)
- Avoids manual spreadsheet filtering and charting every time.
- Makes exploration fast, visual, and reproducible from the same dataset.
- Provides quick insights like “Which countries have the most views?” or “Top channels in India.”

## 3) How to run (Windows PowerShell)
Prerequisites: Python 3.7+ (tested with Python 3.12), pip

1. Create a virtual environment and install requirements
   - python -m venv .venv
   - .\.venv\Scripts\Activate.ps1
   - pip install -r requirements.txt

2. Load the CSV into SQLite (creates youtube.db)
   - python data_loader.py

3. Start the web app and open the dashboard
   - python app.py
   - Visit: http://127.0.0.1:5000/

## 4) High-level architecture
- Data source: CSV file (Global YouTube Statistics.csv)
- ETL: data_loader.py → cleans data and writes to SQLite
- Backend: Flask (app.py) + SQLAlchemy + Pandas
- Frontend: HTML + Jinja templates + Chart.js + Pico.css
- Routes:
  - / → Home page
  - /dashboard → Charts + country dropdown + country’s top-5 channels table

Text diagram
CSV → (data_loader.py) → SQLite (youtube.db) → (app.py) → Templates (Chart.js + Pico.css) → Browser

## 5) End‑to‑end data flow
1. Place Global YouTube Statistics.csv in the project root.
2. Run data_loader.py:
   - Reads the CSV with tolerant parsing.
   - Normalizes column names to snake_case lower.
   - Maps common variants to canonical names: channel_name, subscribers, views, country.
   - Parses numbers: 1,234 → 1234; 2.3M → 2300000; 120K → 120000; 1.5B → 1500000000.
   - Writes a single table youtube_stats into youtube.db (SQLite).
3. Run app.py:
   - Reads youtube_stats into a Pandas DataFrame.
   - Coerces numeric columns and drops invalid rows.
   - Computes:
     - Top 10 channels globally by subscribers (for the bar chart)
     - Top 5 countries by total views (for the pie chart)
     - Country list (unique sorted) for the dropdown
     - Top 5 channels by subscribers for the selected country
   - Renders dashboard.html with all arrays/rows embedded safely via Jinja.

## 6) Components and file roles
- app.py — Flask server, prepares data for charts/table and renders templates.
- data_loader.py — Cleans CSV and writes youtube_stats into youtube.db (SQLite).
- templates/index.html — Home with a link to Dashboard (forced light theme).
- templates/dashboard.html —
  - Pie chart (Top 5 countries by views)
  - Bar chart (Top 10 channels by subscribers)
  - Country dropdown (auto‑submits via GET param ?country=)
  - Table: Top 5 channels for the selected country
  - Styling: white table background and dark text for clear visibility
- requirements.txt — Python dependencies (Flask, Pandas, SQLAlchemy)
- youtube.db — SQLite file created by the loader
- Global YouTube Statistics.csv — Input dataset
- README.md — GitHub-friendly documentation
- understand.md — Plain-English overview (shorter brief)
- explaination.md — This detailed explanation for your presentation

## 7) Backend logic highlights (app.py)
- Connects to youtube.db using SQLAlchemy.
- Reads table youtube_stats using Pandas read_sql.
- Normalizes/renames columns in case input was inconsistent.
- Creates arrays:
  - channel_labels, channel_subscribers → for the top‑10 bar chart
  - country_labels, country_values → for the top‑5 pie chart (sum of views by country)
- Country filter logic:
  - Extracts sorted unique countries from the DF
  - selected_country = request.args.get('country') or default to first country
  - Filters DF, sorts by subscribers desc, takes head(5) for the table
- Renders Jinja template with tojson for safe JavaScript data embedding.

## 8) Frontend logic highlights (dashboard.html)
- Light theme enforced; white tables and dark text for clarity.
- Charts rendered via Chart.js (pie + bar), responsive with axes formatting.
- Country dropdown in a form (onchange submit) to reload /dashboard?country=... with new data.
- Table shows Channel Name, Subscribers, Views, Country with formatted numbers.

## 9) Data model (SQLite)
Single table: youtube_stats
- channel_name: TEXT
- subscribers: REAL/INTEGER (parsed from strings)
- views: REAL/INTEGER (parsed from strings)
- country: TEXT

## 10) Error handling and edge cases
- Missing CSV → loader raises FileNotFoundError.
- Empty/invalid CSV → creates an empty DataFrame with expected schema.
- Column mismatch → normalization + rename_map covers common variants.
- Non‑numeric values → coerced to NA and handled safely.
- Missing table or no data → charts/tables render empty but without crashing.

## 11) Complexity and performance
- Let n = number of CSV rows
- Normalization & parsing: O(n)
- Top‑k selection by subscribers: O(n log n) (k is small constant: 5 or 10)
- Groupby by country: O(n), then nlargest(5)
- Works comfortably for typical CSV sizes (thousands to low millions).

## 12) Libraries and versions
Python (backend & data)
- Flask 3.0.3 — web framework (routes, templates)
- Pandas 2.2.2 — CSV reading/cleaning, data transforms
- SQLAlchemy 2.0.35 — DB engine for SQLite connection
- SQLite — local file database (via SQLAlchemy)

Frontend
- Chart.js 4.x — pie & bar charts
- Pico.css 2.x — lightweight, modern CSS defaults
- HTML + JavaScript + Jinja2 — templating from Flask

Environment
- Python 3.12 (works with 3.7+)

## 13) Demo script (3–5 minutes)
1) Objective — “This app turns a YouTube CSV into an interactive dashboard.”
2) Data flow — “data_loader.py cleans & loads to SQLite; app.py reads & visualizes.”
3) Live demo —
   - Open http://127.0.0.1:5000/ → Dashboard.
   - Show pie: Top 5 countries by views.
   - Show bar: Top 10 channels by subscribers.
   - Use country dropdown → table updates to Top 5 channels for that country.
4) Internals — column normalization, numeric parsing (K/M/B), graceful empty states.
5) Close — benefits, limitations, and possible improvements.

## 14) Likely viva questions with answers
- Why Flask + SQLite?
  - Lightweight stack; SQLite requires no server and is perfect for local analytics dashboards.
- How do you handle inconsistent CSV columns?
  - Normalize to snake_case and map common variants to canonical names.
- How do you parse values like 2.3M or 120K?
  - A parser converts K/M/B suffixes to numbers (x1e3, x1e6, x1e9).
- What if the CSV is empty or missing columns?
  - We create an empty DataFrame with expected schema; UI still renders safely.
- Complexity?
  - Groupby O(n); sort O(n log n); k is a small constant.
- Security concerns?
  - No user‑generated DB writes; templating escapes output; only simple GET filter param.
- How to scale?
  - Move to Postgres, add APIs, cache aggregates, add pagination and auth.

## 15) Limitations and future work
- Static CSV; not real‑time.
- No authentication/authorization (local app focus).
- Potential enhancements:
  - CSV upload UI
  - Export filtered results (CSV/Excel)
  - More charts (growth trends, ratios)
  - Pagination/search for very large datasets
  - Unit tests for loader and routes

## 16) One‑liner (for slides)
“From a raw CSV to insights in your browser: this Flask app cleans YouTube channel data, stores it in SQLite, and renders interactive charts and a country-wise top‑5 table.”

## 17) Quick commands (reference)
- Create venv: python -m venv .venv
- Activate: .\.venv\Scripts\Activate.ps1
- Install: pip install -r requirements.txt
- Load CSV → DB: python data_loader.py
- Run app: python app.py → http://127.0.0.1:5000/

## 18) Where to customize
- Data file name: change the call at the bottom of data_loader.py
- Charts & metrics: edit /dashboard logic in app.py and templates/dashboard.html
- Styling: tweak CSS in templates/dashboard.html (currently forced light theme & white tables)

---
If you need a slide deck version, I can generate a concise 6–7 slide outline with speaker notes based on this document.
