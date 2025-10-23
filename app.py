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
            channel_labels=[],
            channel_subscribers=[],
            country_labels=[],
            country_values=[],
            all_countries=[],
            selected_country='',
            country_top_rows=[],
            total_channels=0,
            total_subscribers=0,
            total_views=0,
            avg_subscribers=0,
            num_channels=10,
            num_countries=5
        )

    # Load data from DB
    try:
        df = pd.read_sql(text('SELECT * FROM youtube_stats'), con=engine)
    except Exception:
        return render_template(
            'dashboard.html',
            channel_labels=[],
            channel_subscribers=[],
            country_labels=[],
            country_values=[],
            all_countries=[],
            selected_country='',
            country_top_rows=[],
            total_channels=0,
            total_subscribers=0,
            total_views=0,
            avg_subscribers=0,
            num_channels=10,
            num_countries=5
        )

    if df.empty:
        return render_template(
            'dashboard.html',
            channel_labels=[],
            channel_subscribers=[],
            country_labels=[],
            country_values=[],
            all_countries=[],
            selected_country='',
            country_top_rows=[],
            total_channels=0,
            total_subscribers=0,
            total_views=0,
            avg_subscribers=0,
            num_channels=10,
            num_countries=5
        )

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

    # Get user-selected number of items for charts
    num_channels = request.args.get('num_channels', 10, type=int)
    num_countries = request.args.get('num_countries', 5, type=int)
    
    # Ensure valid ranges
    num_channels = max(3, min(num_channels, 50))  # Between 3 and 50
    num_countries = max(3, min(num_countries, 20))  # Between 3 and 20
    
    # Get top N channels for bar chart
    top_channels = df.nlargest(num_channels, 'subscribers')
    channel_labels = top_channels['channel_name'].tolist()
    channel_subscribers = top_channels['subscribers'].tolist()
    
    # Get top N countries for pie chart
    country_views = df.groupby('country')['views'].sum().nlargest(num_countries)
    country_labels = country_views.index.tolist()
    country_values = country_views.values.tolist()
    
    # Get all countries for dropdown
    all_countries = sorted(df['country'].unique().tolist())
    selected_country = request.args.get('country', all_countries[0] if all_countries else '')
    
    # Get top 5 channels for selected country
    if selected_country:
        country_df = df[df['country'] == selected_country]
        top_5_country = country_df.nlargest(5, 'subscribers')
        country_top_rows = top_5_country[['channel_name', 'subscribers', 'views', 'country']].to_dict('records')
    else:
        country_top_rows = []
    
    # Calculate statistics for KPI cards
    total_channels = len(df)
    total_subscribers = int(df['subscribers'].sum())
    total_views = int(df['views'].sum())
    avg_subscribers = int(df['subscribers'].mean())

    return render_template(
        'dashboard.html',
        channel_labels=channel_labels,
        channel_subscribers=channel_subscribers,
        country_labels=country_labels,
        country_values=country_values,
        all_countries=all_countries,
        selected_country=selected_country,
        country_top_rows=country_top_rows,
        total_channels=total_channels,
        total_subscribers=total_subscribers,
        total_views=total_views,
        avg_subscribers=avg_subscribers,
        num_channels=num_channels,
        num_countries=num_countries
    )

if __name__ == '__main__':
    app.run(debug=True)
