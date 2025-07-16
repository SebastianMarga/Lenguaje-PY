def contar_jugadores(df):
    return len(df)

def mejor_escuadra_general(df):
    df_filtrado = df[df['age'] <= 37]
    df_top = df_filtrado.groupby(['nationality_name', 'player_positions']).head(2)
    df_top = df_top.sort_values(['nationality_name', 'player_positions', 'overall', 'potential'], ascending=False)
    promedio_pais = df_top.groupby('nationality_name')['overall'].mean()
    return promedio_pais

def mejor_jugador_por_pais(df):
    df_filtrado = df[df['age'] <= 37]
    df_ordenado = df_filtrado.sort_values(['nationality_name', 'overall', 'potential'], ascending=[True, False, False])
    mejores = df_ordenado.groupby('nationality_name').first()
    return mejores['short_name'].to_dict()
