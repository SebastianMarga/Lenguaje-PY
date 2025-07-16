import pandas as pd
import os

def cargar_datos():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, '..', 'Dataset', 'players_22.csv')
    df = pd.read_csv(csv_path, low_memory=False)

    df = df[['short_name', 'age', 'nationality_name', 'overall', 'potential',
             'club_name', 'value_eur', 'wage_eur', 'player_positions']]
    df['player_positions'] = df['player_positions'].str.split(',', expand=True)[0]
    df.dropna(inplace=True)
    return df
