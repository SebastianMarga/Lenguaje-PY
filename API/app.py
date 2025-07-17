from flask import Flask, render_template, jsonify
from Funciones.carga_datos import cargar_datos
from Funciones.estadisticas import contar_jugadores, mejor_escuadra_general, mejor_jugador_por_pais
from Funciones.graficos import generar_grafico
from Funciones.mejor_once import seleccionar_jugadores
app = Flask(__name__)

# Ruta: Página Principal (Dashboard)
@app.route('/')
def mostrar_dashboard():
    df = cargar_datos()
    total_jugadores = cargar_datos()
    jugadores = df.sort_values(by=['overall', 'potential', 'value_eur'], ascending=False).head(15).to_dict(orient='records')
    total_jugadores = contar_jugadores(df)
    cantidad_paises = df['nationality_name'].nunique()
    mejor_jugador = df.head(1).to_dict(orient='records')
    
    mejor_pais = mejor_escuadra_general(df).sort_values(ascending=False).head(1).to_dict()
    mejor10_pais = mejor_escuadra_general(df).sort_values(ascending=False).head(10).to_dict()

    return render_template('Dashboard.html',
                           total_jugadores=total_jugadores,
                           numero_pais=cantidad_paises,
                           primero=mejor_jugador,
                           best=mejor_pais,
                           jugadores=jugadores,
                           paises_mejores=mejor10_pais)

# Ruta: Mejores Países
@app.route('/mejores-paises')
def mejores_paises():
    try:
        df = cargar_datos()
        mejores_paises = mejor_escuadra_general(df).sort_values(ascending=False).to_dict()
        jugador_pais = mejor_jugador_por_pais(df)
        return render_template('Mejorespaises.html',
                               total_paises=mejores_paises,
                               jugador_pais=jugador_pais)
    except Exception as e:
        # Muestra el error en la consola y devuelve una página de error simple
        print(f"Error en /mejores-paises: {e}")
        return render_template('error.html', mensaje_error=str(e)), 500

# Ruta: Estadísticas Adicionales
@app.route('/estadisticas')
def estadisticas():
    df = cargar_datos()
     # Diccionario de países por continente...
    paises_por_continente = {"África": [
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
        ]} 
    paises_dataset = set(df['nationality_name'].unique())
    paises_dict_total = set()
    for lista in paises_por_continente.values():
        paises_dict_total.update(lista)
    paises_presentes = paises_dict_total.intersection(paises_dataset)
    precision_total = round(len(paises_presentes) / len(paises_dict_total) * 100, 1)
    cantidad_paises = df['nationality_name'].nunique()
    grafico_html = generar_grafico(paises_por_continente)
    return render_template('Estadisticas.html',
                           precision_total=precision_total,
                           numero_pais=cantidad_paises,
                           grafico_html=grafico_html)

@app.route('/mejor_11')
@app.route('/mejor_11/<formacion>')
def mejor_once(formacion='4-4-2'):
    df = cargar_datos()
    formaciones = {
        "4-4-2": ['GK', 'LB', 'CB', 'CB', 'RB', 'LM', 'CM', 'CM', 'RM', 'ST', 'ST'],
        "4-3-3": ['GK', 'LB', 'CB', 'CB', 'RB', 'CDM', 'CM', 'CM', 'LW', 'ST', 'RW'],
        "4-2-3-1": ['GK', 'LB', 'CB', 'CB', 'RB', 'CDM', 'CDM', 'LM', 'CAM', 'RM', 'ST'],
    }

    if formacion not in formaciones:
        return jsonify({"error": "Formación no válida"}), 400

    equipo = seleccionar_jugadores(df, formaciones[formacion])
    return jsonify(equipo)

@app.route('/mejor_once')
def mostrar_once():
    return render_template('MejorOnce.html')

if __name__ == '__main__':
    app.run(debug=True)
