import dash
import dash_bootstrap_components as dbc

from dash_app.callbacks import configurar_callbacks
from dash_app.layout import configurar_layout
import plotly.io as pio
pio.templates.default = "plotly_dark"

app = dash.Dash("smart-k-means-dash_app", external_stylesheets=[dbc.themes.BOOTSTRAP], )
app.title = "Smart K-Means"
# Layout da aplicação
configurar_layout(app)
configurar_callbacks(app)

# if __name__ == '__main__':
#     app.run_server(debug=False)
