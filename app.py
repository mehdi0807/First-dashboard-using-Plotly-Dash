import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import plotly
import plotly.graph_objs as go
import plotly.express as px
import dash
from dash import dcc
import dash_html_components as html
import datetime as dt

df = pd.read_csv("https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv")
# Fill NAs with 0s and create GDP per capita column
df = df.fillna(0)
df['gdp_per_capita'] = np.where(df['population']!= 0, df['gdp']/ df['population'], 0)
df0=df.groupby(["country", "year"])["co2", "gdp_per_capita", "oil_co2", "coal_co2", "gas_co2"].max()
df1 = df0.loc[["Africa", "Asia", "Europe", "North America", "South America", "Oceania", "World"],:]
df0 = df0.reset_index()
df1 = df1.reset_index()
filter = (df0.co2==0) | (df0.gdp_per_capita==0)
df2= df0[~filter]
df2=df2.sort_values(by="year")


#fig1
fig1 = go.Figure(go.Scatter(x=df1[df1.country == "Africa"].year.values, y=df1[df1.country == "Africa"].co2.values, mode='lines', showlegend=False, name="co2"))
for continent in ["Asia", "Europe", "North America", "South America", "Oceania", "World"]:
    fig1.add_trace(go.Scatter(x=df1[df1.country == continent].year.values, y=df1[df1.country == continent].co2.values, mode='lines', showlegend=False, name="co2"))
for i in range(1,7):
    fig1.data[i].visible = False
my_buttons = []
continents = ["Africa", "Asia", "Europe", "North America", "South America", "Oceania", "World"]
for continent in continents:
    my_buttons.append({'label': continent,
                        'method': "update",
                        'args': [{"visible":[False]*7}]})

for i in range(0,7) :
    my_buttons[i]["args"][0]["visible"][i] = True
fig1.update_layout({
                'updatemenus': [{'type': "buttons",
                                'direction': 'left',
                                'x': 0.65, 'y': 1.3,
                                'showactive': True,
                                'active': 0,
                                'buttons': my_buttons, 
                                "x": 1.05, "y":-0.2}], 
                                "title":{'text': "<b>Figure1: CO2 across years in ech continent</b>", "x": 0.5, "y": 0.9}})

#fig2
fig2 = go.Figure()
for year in range(1830,2019):
    df3 = df2[df2.year == year]
    fig2.add_trace(go.Scatter(
                    x=df3["gdp_per_capita"],
                    y=df3["co2"], 
                    mode='markers',
                    name=year,
                    text=df3["country"]))
steps=[]
for year in range(1830,2019):
    steps.append({'method': 'update', 
                 'label': year,
                 'args': [{'visible': [False] *189}]})
for i in range(0,189):
    steps[i]["args"][0]["visible"][i] = True

sliders = [{'steps':steps}]
for i in range(1,189):
    fig2.data[i].visible=False

fig2.update_layout({'sliders': sliders})
                   
fig2.update_layout({"title":{'text': "<b>Figure2: CO2 VS GDP Per capita across years</b>", "x": 0.5,"y":0.9}, 
                   "yaxis": {"title":{'text': "CO2"}}, 
                   "xaxis": {"title":{'text': "GDP Per capita"}}})


app = dash.Dash()
app.layout = html.Div(children=[html.H1("CO2 emissions and climate change"),
                                html.Div(dcc.Graph(id='graph1', figure=fig1), style={'width':'650px',
                                                                                     'margin':'5px',
                                                                                    "display": "inline-block"}),
                                html.Div(dcc.Graph(id='graph2', figure=fig2), style={'width':'600px',
                                                                                     'margin':'5px',
                                                                                    "display": "inline-block"}),
                                html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),
                                html.Span(children=[
                                    f"Prepared: {dt.date.today().year}",
                                    " by ", html.B("Mehdi AMOR OUAHMED, "),
                                    html.I("Data Science Student") 
                                    ])], style={'text-align':'center'})
if __name__ == '__main__':
    app.run_server(debug=True)