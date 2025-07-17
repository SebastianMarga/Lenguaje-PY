
def seleccionar_jugadores(df, posiciones):
    equipo = []
    usados = set()

    for pos in posiciones:
        candidatos = df[
            df['player_positions'].str.contains(pos)
            & ~df['short_name'].isin(usados)
        ]
        if not candidatos.empty:
            mejor = candidatos.sort_values('overall', ascending=False).iloc[0]
            equipo.append({
                'name': mejor['short_name'],
                'position': pos
            })
            usados.add(mejor['short_name'])
    return equipo