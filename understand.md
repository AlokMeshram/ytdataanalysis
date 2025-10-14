# Understand: YouTube Analytics Dashboard

A friendly, plain‑English overview of what this project does, how it works, and which libraries it uses.

## What this project is

A small web app that shows insights from a CSV of global YouTube channel stats. It:
- Loads the CSV into a local SQLite database
- Lets you view a dashboard with charts (top countries by views, top channels by subscribers)
- Lets you pick a country and see the top 5 channels in that country in a clean table

In short: it turns a CSV into an interactive dashboard you can open in your browser.

## Why this is useful
- No manual Excel filtering needed—just run once and explore
- Handles slightly messy CSV columns (different names, different cases)
- Gives quick, visual answers to questions like “Which countries have the most views?” or “Who are the top channels in India?”

## How the data flows
1. You put `Global YouTube Statistics.csv` in the project folder.
2. You run `python data_loader.py` which:
   - Reads the CSV safely (even with minor format quirks)
   - Normalizes column names (e.g., "Channel Name" → `channel_name`)
   - Converts values like `1.2M` into real numbers
   - Stores the data in a local `youtube.db` SQLite database
3. You start the web app with `python app.py` which:
   - Reads the data from `youtube.db`
   - Builds chart data for the dashboard
   - Serves web pages you can open at http://127.0.0.1:5000/

## What each file does
- `app.py`: The web server (Flask). It prepares the data for charts and tables and renders the webpages.
- `data_loader.py`: Loads and cleans the CSV, then saves it into the SQLite database.
- `Global YouTube Statistics.csv`: Your dataset.
- `youtube.db`: The SQLite database created from the CSV.
- `templates/index.html`: Home page with a button to open the dashboard.
- `templates/dashboard.html`: Dashboard with charts and tables.
- `requirements.txt`: List of Python packages to install.
- `README.md`: Project documentation and setup steps.
- `understand.md`: This file.

## Features at a glance
- Interactive charts:
  - Pie: Top 5 countries by total views
  - Bar: Top 10 channels by subscribers
- Country picker + table: Top 5 channels for any country in the data
- Robust column mapping and number parsing (e.g., `1,234`, `2.5M`, `120K`)
- Graceful handling of missing columns or empty data

## Libraries used

### Python (backend + data)
- Flask (3.x): Minimal web framework to serve pages and routes
- SQLAlchemy (2.x): Connects to the SQLite database (`youtube.db`)
- Pandas (2.x): Reads and cleans the CSV, prepares data for charts/tables
- SQLite (via SQLAlchemy): Lightweight database stored as a single file

### Frontend (browser)
- Chart.js (4.x): Draws the pie and bar charts on the dashboard
- Pico.css (2.x): Small, clean CSS framework for nice default styles
- Vanilla HTML + JavaScript: The dashboard pages and chart code

### Dev/runtime environment
- Python 3.12 (or 3.7+): Runs the app and data loader

## Typical usage
1. Install dependencies: `pip install -r requirements.txt`
2. Load data: `python data_loader.py`
3. Run the app: `python app.py`
4. Open: `http://127.0.0.1:5000/` → click "Go to Dashboard"
5. Use the country dropdown to view top 5 channels for each country

## Notes and tips
- If the CSV has slightly different column names, the loader maps common variants to: `channel_name`, `subscribers`, `views`, `country`.
- If you want to use a different CSV name, change the call at the bottom of `data_loader.py`.
- The database is recreated each time you run the loader (it replaces existing data).

## Where to customize
- Want a different default chart or more metrics? Edit `app.py` (the `/dashboard` route) and `templates/dashboard.html`.
- Want to change styles? Edit the CSS in `templates/dashboard.html` or swap Pico.css for another framework.

---
If you need this summarized further or translated, tell me how you’d like it presented (bullet points, infographic style, etc.).
