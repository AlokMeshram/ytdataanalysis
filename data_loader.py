import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

def load_data_to_db(csv_file, db_file='youtube.db'):
    csv_path = Path(csv_file)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_file}")

    # Read the CSV with robust options
    try:
        df = pd.read_csv(csv_path, encoding_errors='ignore')
    except pd.errors.EmptyDataError:
        # Create an empty DataFrame with expected schema
        df = pd.DataFrame(columns=['channel_name', 'subscribers', 'views', 'country'])

    # Normalize column names: snake_case and lower
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

    # Map common variants to canonical names
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

    # Normalize numeric strings like '1,234', '2.3M', '120K'
    def parse_num(x):
        if pd.isna(x):
            return pd.NA
        if isinstance(x, (int, float)):
            return x
        s = str(x).strip().upper().replace(',', '')
        try:
            if s.endswith('K'):
                return float(s[:-1]) * 1e3
            if s.endswith('M'):
                return float(s[:-1]) * 1e6
            if s.endswith('B'):
                return float(s[:-1]) * 1e9
            return float(s)
        except ValueError:
            return pd.NA

    for col in ('subscribers', 'views'):
        if col in df.columns:
            df[col] = df[col].map(parse_num)

    # Create SQLite DB
    engine = create_engine(f'sqlite:///{Path(db_file).as_posix()}', echo=False)

    # Store data in table
    df.to_sql('youtube_stats', con=engine, if_exists='replace', index=False)
    print(f"Data loaded successfully into {db_file} (table: youtube_stats)")

if __name__ == "__main__":
    load_data_to_db("Global YouTube Statistics.csv")
