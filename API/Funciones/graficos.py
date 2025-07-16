import plotly.graph_objs as go
import plotly.io as pio

def generar_grafico(paises_por_continente):
    conteo = {k: len(v) for k, v in paises_por_continente.items()}
    total = sum(conteo.values())
    porcentajes = {k: round(v / total * 100, 2) for k, v in conteo.items()}

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
        width=1000,
        height=600
    )

    return pio.to_html(fig, full_html=False)
