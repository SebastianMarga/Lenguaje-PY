from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objs as go
import os

app = Flask(__name__)

@app.route('/')
def mostrar_jugadores():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'Dataset', 'players_22.csv')

    # Cargar CSV
    df = pd.read_csv(csv_path, low_memory=False)
    df = df[['short_name', 'age', 'nationality_name', 'overall', 'potential',
             'club_name', 'value_eur', 'wage_eur', 'player_positions']]
    df['player_positions'] = df['player_positions'].str.split(',', expand=True)[0]
    df.dropna(inplace=True)
    
    #Numero de jugadores 
    def contar_jugadores(df):
        return len(df)
    num_jugadores = contar_jugadores(df)

    """
    # Filtros
    players_missing_worldcup = ['K. Benzema', 'S. Mané', 'S. Agüero', 'Sergio Ramos', 'P. Pogba',
                                'M. Reus', 'Diogo Jota', 'A. Harit', 'N. Kanté', 'G. Lo Celso', 'Piqué']
    df = df[~df['short_name'].isin(players_missing_worldcup)]
    """
    """
    teams_worldcup = [
        'Qatar', 'Brazil', 'Belgium', 'France', 'Argentina', 'England', 'Spain', 'Portugal',
        'Mexico', 'Netherlands', 'Denmark', 'Germany', 'Uruguay', 'Switzerland', 'United States', 'Croatia',
        'Senegal', 'Iran', 'Japan', 'Morocco', 'Serbia', 'Poland', 'South Korea', 'Tunisia',
        'Cameroon', 'Canada', 'Ecuador', 'Saudi Arabia', 'Ghana', 'Wales', 'Costa Rica', 'Australia'
    ]
    df = df[df['nationality_name'].isin(teams_worldcup)]
    """
    # Top 15 jugadores
    df.sort_values(by=['overall', 'potential', 'value_eur'], ascending=False, inplace=True)
    top15 = df.head(15)
    jugadores = top15.to_dict(orient='records')

    #Numero de paises
    paises=df['nationality_name'].drop_duplicates().sort_values(ascending=False)
    cantidad_paises=df['nationality_name'].nunique()
    
    #Mejor jugador del Fifa
    mejor_jugador=df.head(1).to_dict(orient='records')

    def mejor_escuadra_general(df):
        df_filtrado = df[df['age'] <= 37]
        # Toma hasta 2 jugadores por nacionalidad y posición
        df_top = df_filtrado.groupby(['nationality_name', 'player_positions']).head(2)
        # Ordena por país, posición, overall y potencial
        df_top = df_top.sort_values(['nationality_name', 'player_positions', 'overall', 'potential'], ascending=False)
        # Agrupa por nacionalidad y calcula el promedio del overall de su escuadra
        promedio_pais = df_top.groupby('nationality_name')['overall'].mean()
        return promedio_pais
    
    def mejor_jugador_por_pais(df):
        df_filtrado = df[df['age'] <= 37]
        df_ordenado = df_filtrado.sort_values(['nationality_name', 'overall', 'potential'], ascending=[True, False, False])
        mejores = df_ordenado.groupby('nationality_name').first()
        return mejores['short_name'].to_dict()
    
    mejor_pais=mejor_escuadra_general(df).sort_values(ascending=False).head(1).to_dict()
    mejor10_pais=mejor_escuadra_general(df).sort_values(ascending=False).head(10).to_dict()
    mejores_paises=mejor_escuadra_general(df).sort_values(ascending=False).to_dict()
    jugador_pais=mejor_jugador_por_pais(df)

    # Diccionario de países por continente (aquí te dejo un ejemplo reducido, debes completarlo)
    paises_por_continente = {
        "África": [
        "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cameroon", "Cape Verde Islands",
        "Central African Republic", "Chad", "Comoros", "Congo", "Congo DR", "Côte d'Ivoire", "Djibouti", "Egypt",
        "Equatorial Guinea", "Eritrea", "Eswatini", "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea", "Guinea Bissau",
        "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", "Morocco",
        "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "São Tomé and Príncipe", "Senegal", "Seychelles",
        "Sierra Leone", "Somalia", "South Africa", "South Sudan", "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda",
        "Zambia", "Zimbabwe"
        ],
        "Asia": [
        "Afghanistan", "Armenia", "Azerbaijan", "Bahrain", "Bangladesh", "Bhutan", "Brunei", "Cambodia", "China PR",
        "Chinese Taipei", "Cyprus", "Georgia", "Hong Kong", "India", "Indonesia", "Iran", "Iraq", "Israel", "Japan",
        "Jordan", "Kazakhstan", "Kuwait", "Kyrgyzstan", "Laos", "Lebanon", "Malaysia", "Maldives", "Mongolia", "Myanmar",
        "Nepal", "North Korea", "Oman", "Pakistan", "Palestine", "Philippines", "Qatar", "Saudi Arabia", "Singapore",
        "South Korea", "Sri Lanka", "Syria", "Tajikistan", "Thailand", "Timor-Leste", "Turkmenistan", "United Arab Emirates",
        "Uzbekistan", "Vietnam", "Yemen"
        ],
        "Europa": [
        "Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia", "Czech Republic",
        "Denmark", "England", "Estonia", "Faroe Islands", "Finland", "France", "Germany", "Gibraltar", "Greece", "Hungary",
        "Iceland", "Ireland", "Italy", "Kosovo", "Latvia", "Liechtenstein", "Lithuania", "Luxembourg", "Malta",
        "Moldova", "Monaco", "Montenegro", "Netherlands", "North Macedonia", "Northern Ireland", "Norway", "Poland",
        "Portugal", "Romania", "Russia", "San Marino", "Scotland", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden",
        "Switzerland", "Turkey", "Ukraine", "Wales"
        ],
        "América": [
        "Antigua and Barbuda", "Argentina", "Bahamas", "Barbados", "Belize", "Bolivia", "Brazil", "Canada", "Chile",
        "Colombia", "Costa Rica", "Cuba", "Dominican Republic", "Ecuador", "El Salvador", "Grenada", "Guatemala",
        "Guyana", "Haiti", "Honduras", "Jamaica", "Mexico", "Nicaragua", "Panama", "Paraguay", "Peru", "Puerto Rico",
        "Saint Kitts and Nevis", "Saint Lucia", "Suriname", "Trinidad and Tobago", "United States", "Uruguay", "Venezuela"
        ],
        "Oceanía": [
        "Australia", "Fiji", "Guam", "New Zealand", "Papua New Guinea"
        ]
        }

        # 1. Países del dataset
    paises_dataset = set(df['nationality_name'].unique())

    # 2. Países del diccionario total
    paises_dict_total = set()
    for lista in paises_por_continente.values():
        paises_dict_total.update(lista)

    # 3. Países que realmente están en el dataset
    paises_presentes = paises_dict_total.intersection(paises_dataset)

    # 4. Precisión total
    precision_total = len(paises_presentes) / len(paises_dict_total)
    precision_total_porcentaje = round(precision_total * 100, 1)


    def grafico():
        # Diccionario de países por continente (aquí te dejo un ejemplo reducido, debes completarlo)
        paises_por_continente = {
        "África": [
        "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cameroon", "Cape Verde Islands",
        "Central African Republic", "Chad", "Comoros", "Congo", "Congo DR", "Côte d'Ivoire", "Djibouti", "Egypt",
        "Equatorial Guinea", "Eritrea", "Eswatini", "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea", "Guinea Bissau",
        "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", "Morocco",
        "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "São Tomé and Príncipe", "Senegal", "Seychelles",
        "Sierra Leone", "Somalia", "South Africa", "South Sudan", "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda",
        "Zambia", "Zimbabwe"
        ],
        "Asia": [
        "Afghanistan", "Armenia", "Azerbaijan", "Bahrain", "Bangladesh", "Bhutan", "Brunei", "Cambodia", "China PR",
        "Chinese Taipei", "Cyprus", "Georgia", "Hong Kong", "India", "Indonesia", "Iran", "Iraq", "Israel", "Japan",
        "Jordan", "Kazakhstan", "Kuwait", "Kyrgyzstan", "Laos", "Lebanon", "Malaysia", "Maldives", "Mongolia", "Myanmar",
        "Nepal", "North Korea", "Oman", "Pakistan", "Palestine", "Philippines", "Qatar", "Saudi Arabia", "Singapore",
        "South Korea", "Sri Lanka", "Syria", "Tajikistan", "Thailand", "Timor-Leste", "Turkmenistan", "United Arab Emirates",
        "Uzbekistan", "Vietnam", "Yemen"
        ],
        "Europa": [
        "Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia", "Czech Republic",
        "Denmark", "England", "Estonia", "Faroe Islands", "Finland", "France", "Germany", "Gibraltar", "Greece", "Hungary",
        "Iceland", "Ireland", "Italy", "Kosovo", "Latvia", "Liechtenstein", "Lithuania", "Luxembourg", "Malta",
        "Moldova", "Monaco", "Montenegro", "Netherlands", "North Macedonia", "Northern Ireland", "Norway", "Poland",
        "Portugal", "Romania", "Russia", "San Marino", "Scotland", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden",
        "Switzerland", "Turkey", "Ukraine", "Wales"
        ],
        "América": [
        "Antigua and Barbuda", "Argentina", "Bahamas", "Barbados", "Belize", "Bolivia", "Brazil", "Canada", "Chile",
        "Colombia", "Costa Rica", "Cuba", "Dominican Republic", "Ecuador", "El Salvador", "Grenada", "Guatemala",
        "Guyana", "Haiti", "Honduras", "Jamaica", "Mexico", "Nicaragua", "Panama", "Paraguay", "Peru", "Puerto Rico",
        "Saint Kitts and Nevis", "Saint Lucia", "Suriname", "Trinidad and Tobago", "United States", "Uruguay", "Venezuela"
        ],
        "Oceanía": [
        "Australia", "Fiji", "Guam", "New Zealand", "Papua New Guinea"
        ]
        }
        # Conteo y porcentaje
        conteo = {k: len(v) for k, v in paises_por_continente.items()}
        total = sum(conteo.values())
        porcentajes = {k: round(v / total * 100, 2) for k, v in conteo.items()}

        # Gráfico de Plotly
        fig = go.Figure(data=[
        go.Bar(
            x=list(porcentajes.keys()),
            y=list(porcentajes.values()),
            text=[f"{v}%" for v in porcentajes.values()],
            textposition='outside'
        )
        ])

        fig.update_layout(
        xaxis_title='Continentes',
        yaxis_title='Porcentaje de países',
        yaxis=dict(ticksuffix='%'),
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        autosize=True,
        width=1000,
        height=600,
        )

        return pio.to_html(fig, full_html=False)
    grafico_html=grafico()


    # Renderizar HTML
    return render_template('Dashboard.html', jugadores=jugadores, grafico_html=grafico_html,numero_pais=cantidad_paises, pais=paises, total_jugadores=num_jugadores, primero=mejor_jugador, best=mejor_pais, paises_mejores=mejor10_pais, total_paises=mejores_paises, jugador_pais=jugador_pais, precision_total=precision_total_porcentaje)

if __name__ == '__main__':
    app.run(debug=True)

