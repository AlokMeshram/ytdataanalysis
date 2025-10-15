# YouTube Analytics Dashboard

A small Flask app that visualizes global YouTube statistics stored in a local SQLite database.

## Quick start

1. Create and activate a virtual environment (Windows PowerShell):

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Load data into the SQLite database (expects `Global YouTube Statistics.csv` in the project root):

```
python data_loader.py
```

4. Run the app:

```
python app.py
```

Open http://127.0.0.1:5000/ and click "Go to Dashboard".

## Notes
- If the CSV has different column names, the loader will normalize them and try to map to `channel_name`, `subscribers`, `views`, and `country`.
- If the database/table is missing, the dashboard will render empty charts and table gracefully.
