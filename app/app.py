import dash
import dash_bootstrap_components as dbc

from callbacks import configurar_callbacks
from layout import configurar_layout
import plotly.io as pio

pio.templates.default = "plotly_dark"

app = dash.Dash("smart-k-means-app", external_stylesheets=[dbc.themes.BOOTSTRAP], )
app.title = "Smart K-Means"
# Layout da aplicação
configurar_layout(app)
configurar_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
