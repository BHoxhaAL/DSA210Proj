import soccerdata as sd

fbref = sd.FBref(leagues=["ENG-Premier League"], seasons=[2021])

stats = fbref.read_player_match_stats(stat_type="summary")

print(stats.head())
print(stats.columns.tolist())