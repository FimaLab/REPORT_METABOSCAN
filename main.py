from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd


app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1(children='Панорамный метаболомный обзор', style={'textAlign':'center','margin':'0px'}),]
             , style={'background-color':'#336CA6', 'color':'white','font-family':'Calibri','margin':'0px'}),
    html.Div([
        html.Div([
            html.P('На графике представлены функциональные группы метаболитов, которые были оценены по уровню риска на основе Ваших результатов метаболомногопрофилирования',
                    style={'color':'black','font-family':'Calibri','font-size':'18px','margin':'0px'}),
            # html.Br(),
            # html.Img(src=app.get_asset_url('level_of_risk.png'), style={'width':'100%','height':'100%'}),
            html.Div([
                html.H3(children='Уровень риска', style={'textAlign':'left', 'color':'#336CA6','font-family':'Calibri','margin':'0px','margin-top':'5px'}),
                # html.Img(src=app.get_asset_url('rArrow.png'), style={'width':'25px'}),
            ],style={'display':'flex', 'width':'100%','border':'1px solid black'}),
            html.Div([
                
            ], style={'display':'flex', 'justify-content':'space-between', 'width':'100%','height':'60px','border':'1px solid black'}),
            html.Div([
                
            ], style={'display':'flex', 'justify-content':'space-between', 'width':'100%','height':'500px','border':'1px solid black'}),
        ], style={ 'width':'65%','height':'600px',}),
        html.Div([
            
        ], style={'display':'flex', 'justify-content':'space-between', 'width':'35%','height':'600px',}),
    ], style={'display':'flex', 'justify-content':'space-between', 'width':'100%'}),
    ],style={'aspect-ratio':'1:1,4143','margin-left':'10px', 'margin-right':'10px'})
    

if __name__ == '__main__':
    app.run(debug=True)