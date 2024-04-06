import dash
import dash_bootstrap_components as dbc
from layout import layout
from callbacks import register_callbacks

# Inicialização do aplicativo Dash
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
                suppress_callback_exceptions=True)

# Layout
app.layout = layout

# Registrar callbacks
register_callbacks(app)

# Executar o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)
