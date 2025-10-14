from flask import Flask, render_template, request
from sqlalchemy import create_engine, inspect, text
import pandas as pd
from pathlib import Path

app = Flask(__name__)

# Connect to SQLite DB
DB_PATH = Path(__file__).with_name('youtube.db')
engine = create_engine(f'sqlite:///{DB_PATH.as_posix()}')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    # Ensure table exists
    inspector = inspect(engine)
    if 'youtube_stats' not in inspector.get_table_names():
        # No data available
        return render_template(
            'dashboard.html',
            top_channels=[],
            country_labels=[],
            country_values=[],
            channel_labels=[],
            channel_subscribers=[],
            countries=[],
            selected_country='',
            country_top_rows=[]
        )

    # Load data from DB
    try:
        df = pd.read_sql(text('SELECT * FROM youtube_stats'), con=engine)
    except Exception:
        return render_template('dashboard.html', top_channels=[], country_labels=[], country_values=[], channel_labels=[], channel_subscribers=[], countries=[], selected_country='', country_top_rows=[])

    if df.empty:
        return render_template('dashboard.html', top_channels=[], country_labels=[], country_values=[], channel_labels=[], channel_subscribers=[], countries=[], selected_country='', country_top_rows=[])

    # Normalize column names: lower snake_case
    def normalize(col: str) -> str:
        return (
            str(col)
            .strip()
            .replace(' ', '_')
            .replace('-', '_')
            .replace('/', '_')
            .lower()
        )

    df.columns = [normalize(c) for c in df.columns]

    # Map common variants to expected names
    rename_map = {}
    for c in list(df.columns):
        if c in {'youtuber', 'channel', 'channelname', 'channel_name'}:
            rename_map[c] = 'channel_name'
        if c in {'subscriber', 'subs', 'subscriber_count', 'subscribers'}:
            rename_map[c] = 'subscribers'
        if c in {'video_views', 'view', 'total_views', 'views'}:
            rename_map[c] = 'views'
        if c in {'country/region', 'region', 'nation', 'country'}:
            rename_map[c] = 'country'

    if rename_map:
        df = df.rename(columns=rename_map)

    # Coerce numeric types safely
    for col in ('subscribers', 'views'):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop rows missing critical fields
    required_cols = ['channel_name', 'subscribers', 'views', 'country']
    present = [c for c in required_cols if c in df.columns]
    if present:
        df = df.dropna(subset=present)

    needed_for_top = ['channel_name', 'subscribers']
    extra_cols = [c for c in ['views', 'country'] if c in df.columns]
    if not set(needed_for_top).issubset(df.columns):
        top_channels = pd.DataFrame(columns=needed_for_top + extra_cols)
    else:
        cols = needed_for_top + extra_cols
        top_channels = df.nlargest(10, 'subscribers')[cols]

    # Prepare channel chart arrays
    if {'channel_name', 'subscribers'}.issubset(top_channels.columns) and not top_channels.empty:
        channel_labels = list(top_channels['channel_name'].astype(str))
        channel_subscribers = list(top_channels['subscribers'].fillna(0).astype(float))
    else:
        channel_labels, channel_subscribers = [], []

    if not {'country', 'views'}.issubset(df.columns):
        country_labels, country_values = [], []
    else:
        country_views = df.groupby('country', dropna=False)['views'].sum().nlargest(5)
        country_labels = list(country_views.index.astype(str))
        country_values = list(country_views.values)

    # Country selector: list of countries available
    if 'country' in df.columns:
        countries = sorted([str(c) for c in df['country'].dropna().unique()])
    else:
        countries = []

    # Selected country from query (default to first available)
    selected_country = request.args.get('country') if countries else ''
    if not selected_country and countries:
        selected_country = countries[0]

    # Top 5 channels for selected country
    if countries and selected_country:
        subset = df[df['country'].astype(str) == selected_country]
    else:
        subset = pd.DataFrame(columns=['channel_name','subscribers','views','country'])

    if not subset.empty and {'channel_name','subscribers'}.issubset(subset.columns):
        cols_for_table = [c for c in ['channel_name','subscribers','views','country'] if c in subset.columns]
        top5 = subset.sort_values('subscribers', ascending=False).head(5)[cols_for_table]
        for col in ['subscribers','views']:
            if col in top5.columns:
                top5[col] = pd.to_numeric(top5[col], errors='coerce').fillna(0)
        country_top_rows = top5.to_dict(orient='records')
    else:
        country_top_rows = []

    return render_template(
        'dashboard.html',
        top_channels=top_channels.to_dict(orient='records'),
        country_labels=country_labels,
        country_values=country_values,
        channel_labels=channel_labels,
        channel_subscribers=channel_subscribers,
        countries=countries,
        selected_country=selected_country,
        country_top_rows=country_top_rows,
    )

if __name__ == '__main__':
    app.run(debug=True)
