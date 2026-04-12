import pandas as pd

# Load datasets
fpl = pd.read_csv('FPL_logs.csv')
muslim_players = pd.read_csv('muslim_players.csv')
ramadan = pd.read_csv('ramadan_dates.csv')

# Clean Transfermarkt names — remove ID in brackets, strip whitespace
muslim_players['clean_name'] = muslim_players['player_name'].str.replace(r'\s*\(\d+\)', '', regex=True).str.strip()

# Clean FPL names — replace hyphens with spaces
fpl['clean_name'] = fpl['Name'].str.replace('-', ' ')

# Drop nulls
muslim_players = muslim_players.dropna(subset=['clean_name'])

# Try joining
merged = fpl.merge(muslim_players[['clean_name', 'citizenship', 'main_position']], on='clean_name', how='inner')

print(f"Muslim player match observations: {len(merged)}")
print(f"Unique Muslim players found: {merged['clean_name'].nunique()}")
print("\nSample matched players:")
print(merged[['clean_name', 'citizenship', 'Date', 'Gls', 'xG']].head(10))