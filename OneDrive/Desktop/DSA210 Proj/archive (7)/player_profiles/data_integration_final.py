import pandas as pd

# Load datasets
fpl = pd.read_csv('FPL_logs.csv')
muslim_players = pd.read_csv('muslim_players.csv')
ramadan = pd.read_csv('ramadan_dates.csv')

# Clean names
muslim_players['clean_name'] = muslim_players['player_name'].str.replace(r'\s*\(\d+\)', '', regex=True).str.strip()
fpl['clean_name'] = fpl['Name'].str.replace('-', ' ')
muslim_players = muslim_players.dropna(subset=['clean_name'])

# Merge FPL with Muslim players
merged = fpl.merge(muslim_players[['clean_name', 'citizenship', 'main_position']], on='clean_name', how='inner')

# Convert dates
merged['Date'] = pd.to_datetime(merged['Date'])
ramadan['ramadan_start'] = pd.to_datetime(ramadan['ramadan_start'])
ramadan['ramadan_end'] = pd.to_datetime(ramadan['ramadan_end'])

# Tag each match as Ramadan or not
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

merged['is_ramadan'] = merged['Date'].apply(tag_ramadan)
merged['days_into_ramadan'] = merged['Date'].apply(days_into_ramadan)

# Save final dataset
merged.to_csv('muslim_player_matches.csv', index=False)

print(f"Total observations: {len(merged)}")
print(f"Ramadan observations: {merged['is_ramadan'].sum()}")
print(f"Non-Ramadan observations: {(~merged['is_ramadan']).sum()}")
print(f"Unique players: {merged['clean_name'].nunique()}")
print("\nSample Ramadan matches:")
print(merged[merged['is_ramadan']][['clean_name', 'Date', 'days_into_ramadan', 'Gls', 'xG']].head(10))