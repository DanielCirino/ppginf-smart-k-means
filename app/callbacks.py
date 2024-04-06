from dash.exceptions import PreventUpdate
from dash import dcc, html, Input, Output, State

# Diretório onde os arquivos serão salvos
UPLOAD_DIRECTORY = "../upload"


# Função para registrar os callbacks
def register_callbacks(app):
    # Callback para atualizar o conteúdo da página com base na URL
    @app.callback(
        Output('page-content', 'children'),  # Adicionando a saída do callback ao elemento page-content
        [Input('url', 'pathname')]
    )
    def display_page(pathname):
        if pathname == '/page-1':
            return html.H1('Conteúdo da Página 1')
        elif pathname == '/page-2':
            return html.H1('Conteúdo da Página 2')
        else:
            return [html.H2("Página Inicial"),
                    html.P("Faça o upload de um arquivo:"),
                    dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                            'Arraste e solte ou ',
                            html.A('selecione um arquivo')
                        ]),
                        style={
                            'width': '100%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px'
                        },
                        # Permite o upload de múltiplos arquivos
                        multiple=False
                    ),
                    html.Div(id='output-data-upload'),
                    ]

    # Callback para processar o upload de arquivos
    @app.callback(
        Output('output-data-upload', 'children'),
        [Input('upload-data', 'contents')],
        [State('upload-data', 'filename'),
         State('upload-data', 'last_modified')]
    )
    def update_output(list_of_contents, list_of_names, list_of_dates):
        if list_of_contents is None:
            raise PreventUpdate

        html_text = f'''
            <h1>{list_of_names}</h1>
            <p>Este é um exemplo de texto dinâmico com tags HTML gerado por um callback.</p>
            <p>Valor atual do input: <strong>{list_of_contents}</strong></p>
            '''
        # Retorna a saída como HTML diretamente
        return html.Div(dcc.Markdown(html_text))
