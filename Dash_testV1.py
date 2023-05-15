import io
import dash
import base64
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
from wordcloud import WordCloud
from PIL import Image
import pandas as pd
# from dash.dash_table.Format import Group
from dash import dash_table
# import dash_table
import plotly.express as px
import os

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)

chemin = "DonneeAbdNettoyeeAvecDate.csv"
df = pd.read_csv(chemin, sep='µ',engine='python', encoding="utf-8")

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#212529",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

image_url = "Logo_Meaux.svg"
encoded_image = base64.b64encode(open(image_url, 'rb').read())
sidebar = html.Div(
    [
        html.H2("Ça se discute", className="display-9", style={'color':'white'}),
        html.Hr(),
        html.P(
            "Restitution des tendances de la ville de Meaux", className="lead", style={'color':'white'}
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Page 1", href="/page-1", active="exact"),
                dbc.NavLink("Page 2", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
        html.Img(src='https://upload.wikimedia.org/wikipedia/fr/thumb/b/bf/Logo_Meaux.svg/1280px-Logo_Meaux.svg.png',
                 style={'position': 'absolute', 'bottom': '0', 'left': '0', 'width': '90%'})
    ],
    style=SIDEBAR_STYLE,
)

categories = df['categorie'].unique()

dropdown = dcc.Dropdown(
    id='dropdown',
    options=df["categorie"].unique(),
    #options=[{'label': cat, 'value': cat} for cat in categories],
    value=categories[0]
)
@app.callback(
    Output('mon_graphique', 'figure'),
    [Input('dropdown', 'value')]
)
def mettre_a_jour_graphique(cat_selectionnee):
    dfiltree = df[df["categorie"]==cat_selectionnee] 
    if dfiltree['note'].value_counts().shape[0]==1:
        nb_n=0
    else:
        nb_n=dfiltree['note'].value_counts()[1]
    nb_p=dfiltree['note'].value_counts()[0]
    df_temp=pd.DataFrame({'0_1':[nb_n,nb_p]})
    figure = px.pie(df_temp,values='0_1',names=['Positif','Negatif'], 
                    title=("Analyse des sentiments du secteur:{}".format(cat_selectionnee)))
    return figure


content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content,])


@app.callback(
        Output("page-content", "children"), 
        [Input("url", "pathname")],
)
def render_page_content(pathname):
    home_page_content = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns[1:]],
    data=df.to_dict('records')
    )

    page1_content = dcc.Graph(id='mon_graphique')

    # Définition des couleurs pour chaque carte
    colors = ["primary", "success", "warning", "danger", "info"]

    # Création des cartes
    cards = []
    for i, kpi_title in enumerate(["kpi", "kpi1", "kpi2", "kpi3", "kpi4"]):
        card = dbc.Card(
            dbc.CardBody(
                [
                    html.H4(kpi_title, className="card-title"),
                    html.P("Contenu de la carte {}".format(i+1), className="card-text"),
                ]
            ),
            color=colors[i]
        )
        cards.append(card)

    # Création d'une ligne pour aligner les cartes horizontalement
    cards_row = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(card) for card in cards
                ],
                className="mb-3",
            ),
        ],
        className="row justify-content-center"
    )

    if pathname == "/":
        return html.P("HomePage"),home_page_content
    elif pathname == "/page-1":
        return html.P("Analyse des données scrappées."),dropdown,page1_content
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!"),cards_row,
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P("The pathname {} was not recognized...".format(pathname)),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == "__main__":
    app.run_server(debug=True)