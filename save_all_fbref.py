import soccerdata as sd
import pandas as pd

leagues = [
    "ENG-Premier League",
    "ESP-La Liga",
    "GER-Bundesliga",
    "ITA-Serie A",
    "FRA-Ligue 1"
]
seasons = [2021, 2022, 2023, 2024]

all_data = []

for season in seasons:
    for league in leagues:
        try:
            fbref = sd.FBref(leagues=[league], seasons=[season])
            stats = fbref.read_player_match_stats(stat_type="summary")
            stats = stats.reset_index()
            stats.columns = [b if b else a for a, b in stats.columns]
            stats['season'] = season
            stats['league'] = league
            all_data.append(stats)
            print(f"Loaded {league} {season}: {len(stats)} rows")
        except Exception as e:
            print(f"Skipped {league} {season}: {e}")

combined = pd.concat(all_data, ignore_index=True)
combined.to_csv('fbref_all_leagues.csv', index=False)
print(f"\nTotal rows: {len(combined)}")
print(f"Columns: {combined.columns.tolist()}")
print("Saved.")