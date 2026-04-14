import pandas as pd

# Load datasets
fbref = pd.read_csv('fbref_all_leagues.csv')
muslim_players = pd.read_csv('muslim_players.csv')
ramadan = pd.read_csv('ramadan_dates.csv')

# Clean Muslim player names
muslim_players['clean_name'] = muslim_players['player_name'].str.replace(r'\s*\(\d+\)', '', regex=True).str.strip()
muslim_players = muslim_players.dropna(subset=['clean_name'])

# Extract date from game column
fbref['date'] = fbref['game'].str.extract(r'(\d{4}-\d{2}-\d{2})')
fbref['date'] = pd.to_datetime(fbref['date'])

# Clean FBRef player names
fbref['clean_name'] = fbref['player'].str.strip()

# Merge with Muslim players
merged = fbref.merge(muslim_players[['clean_name', 'citizenship', 'main_position']], on='clean_name', how='inner')

# Convert Ramadan dates
ramadan['ramadan_start'] = pd.to_datetime(ramadan['ramadan_start'])
ramadan['ramadan_end'] = pd.to_datetime(ramadan['ramadan_end'])

# Tag Ramadan matches
def tag_ramadan(date):
    for _, row in ramadan.iterrows():
        if row['ramadan_start'] <= date <= row['ramadan_end']:
            return True
    return False

def days_into_ramadan(date):
    for _, row in ramadan.iterrows():
        if row['ramadan_start'] <= date <= row['ramadan_end']:
            return (date - row['ramadan_start']).days + 1
    return 0

merged['is_ramadan'] = merged['date'].apply(tag_ramadan)
merged['days_into_ramadan'] = merged['date'].apply(days_into_ramadan)

# Save
merged.to_csv('muslim_player_matches.csv', index=False)

print(f"Total observations: {len(merged)}")
print(f"Ramadan observations: {merged['is_ramadan'].sum()}")
print(f"Non-Ramadan observations: {(~merged['is_ramadan']).sum()}")
print(f"Unique players: {merged['clean_name'].nunique()}")
print(f"Leagues: {merged['league'].unique()}")