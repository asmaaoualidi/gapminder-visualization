from dash import Dash, html, dcc, Input, Output, dash_table
import pandas as pd
import plotly.express as px

# Chargement des données
df = pd.read_csv(r'C:\Users\user\Documents\IA\ADA\prof_yassin\tp dash pays\app\gapminder_unfiltered1.csv')

# Initialisation de l'application Dash
app = Dash()

# Définition de la mise en page
app.layout = html.Div(style={'padding': '20px', 'border': '2px solid black', 'border-radius': '10px', 'border-radius': '10px'}, children=[
    # Titre
    html.H1(
        "Visualisations de population des pays",
        style={'color': 'blue', 'textAlign': 'center', 'padding': '10px','border':'2px solid red'},
    ),

    # Conteneur pour tableau et graphique
    html.Div(style={'display': 'flex', 'justifyContent': 'space-between'}, children=[
        # Tableau interactif
        html.Div(style={'width': '48%', 'padding': '10px', 'border': '2px solid grey', 'border-radius': '10px'}, children=[
            html.H3("Tableau des données", style={'textAlign': 'center'}),
            dash_table.DataTable(
                id='data_table',
                columns=[
                    {"name": col, "id": col, "type": "text"} if df[col].dtype == 'O' else
                    {"name": col, "id": col, "type": "numeric"} for col in df.columns
                ],
                data=df.to_dict('records'),
                page_size=10,
                filter_action="native",
                sort_action="native",
                style_table={'margin': 'auto', 'width': '90%', 'overflowX': 'auto'},
                style_cell={'textAlign': 'center'}
            )
        ]),

        # Graphique interactif et Dropdown
        html.Div(style={'width': '48%', 'padding': '10px', 'border': '2px solid grey', 'border-radius': '10px'}, children=[
            html.H3("Graphique interactif", style={'textAlign': 'center'}),
            dcc.Dropdown(
                id='dropdown',
                options=[{'label': country, 'value': country} for country in df['country'].unique()],
                value='Canada',
                style={'width': '90%', 'margin': '10px auto'}
            ),
            dcc.Graph(
                id='graph_id',
                style={'margin': '20px'}
            )
        ])
    ]),

    # Histogramme des populations
    html.Div(style={'padding': '10px', 'border': '2px solid grey', 'border-radius': '10px', 'margin-top': '20px'}, children=[
        html.H3("Histogramme des populations", style={'textAlign': 'center'}),
        dcc.Dropdown(
            id='dropdown_id',
            options=[{'label': country, 'value': country} for country in df['country'].unique()],
            value='Canada',
            style={'width': '90%', 'margin': '10px auto'}
        ),
        dcc.Graph(
            id='histogram',
            style={'margin': '20px'}
        )
    ])
])

# Callback pour mettre à jour le graphique en fonction du pays sélectionné
@app.callback(
    Output('graph_id', 'figure'),
    Input('dropdown', 'value')
)
def update_graph(selected_country):
    filtered_data = df[df['country'] == selected_country]
    fig = px.line(filtered_data, x='year', y='pop', title=f"Population de {selected_country} au fil du temps")
    return fig

# Callback pour l'histogramme des populations
@app.callback(
    Output('histogram', 'figure'),
    Input('dropdown_id', 'value')
)
def update_histogram(selected_country):
    filtered_data = df[df['country'] == selected_country]
    fig = px.histogram(filtered_data, x='year', y='pop', nbins=10, title=f"Distribution de la population pour {selected_country}")
    return fig

# Exécution de l'application
if __name__ == "__main__":
    app.run(debug=True, port=8052)
