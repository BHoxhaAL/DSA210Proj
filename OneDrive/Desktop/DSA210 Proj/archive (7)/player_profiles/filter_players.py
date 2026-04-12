import pandas as pd

muslim_countries = [
    'Albania', 'Algeria', 'Azerbaijan', 'Bahrain', 'Bangladesh',
    'Bosnia-Herzegovina', 'Burkina Faso', 'Cameroon', 'Chad',
    'Comoros', 'Djibouti', 'Egypt', 'Gambia', 'Guinea',
    'Guinea-Bissau', 'Indonesia', 'Iran', 'Iraq', 'Jordan',
    'Kazakhstan', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Lebanon',
    'Libya', 'Malaysia', 'Mali', 'Mauritania', 'Morocco',
    'Niger', 'Nigeria', 'Oman', 'Pakistan', 'Palestine',
    'Qatar', 'Saudi Arabia', 'Senegal', 'Sierra Leone', 'Somalia',
    'Sudan', 'Syria', 'Tajikistan', 'Tunisia', 'Turkey', 'Türkiye',
    'Turkmenistan', 'UAE', 'Uzbekistan', 'Yemen'
]

df = pd.read_csv('player_profiles.csv')

def is_muslim_country(citizenship):
    if pd.isna(citizenship):
        return False
    for country in muslim_countries:
        if country in citizenship:
            return True
    return False

muslim_players = df[df['citizenship'].apply(is_muslim_country)][
    ['player_id', 'player_name', 'citizenship', 'position', 'main_position']
].drop_duplicates()

print(f"Total Muslim players found: {len(muslim_players)}")
muslim_players.to_csv('muslim_players.csv', index=False)