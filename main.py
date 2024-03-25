from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

name = 'Иванов Иван Иванович'
date = '21.07.2023'
age = 47
gender = 'М'

obmen_veshestv = 24
obmen_aminokislot = 41
nutrieviy_status = 30
stress_i_neyromoderatory = 31
toxicheskie_vosdeystvia = 44
markery_mikrobioty = 32
vospalenie = 46
funcii_serdca = 43
functii_pecheni = 64

obmen_veshestv_list = [10,20,30,40,50]
obmen_aminokislot_list = [60,70,80,90,100,40]
nutrieviy_status_list = [100,20,30,10,20]
stress_i_neyromoderatory_list = [10,20,34,100]
toxicheskie_vosdeystvia_list = [10,20,30]
markery_mikrobioty_list = [10,40]
vospalenie_list = [70]
funcii_serdca_list = [10,20,40,60]
functii_pecheni_list = [10,20,33,1000]

def get_color(n):
    """
    A function that returns a color based on the input number.
    
    Parameters:
    n (int): The input number to determine the color.
    
    Returns:
    str: A hexadecimal color code based on the input number.
    """
    if n <= 33:
        return '#a5cd9a'
    elif n <= 66:
        return '#feb61d'
    else:
        return '#de6d54'
    
def procent_validator(n):
    """
    A function that validates and formats a given number as a percentage.
    
    Parameters:
    n (int): The number to be validated and formatted as a percentage.
    
    Returns:
    str: A string representing the formatted percentage.
    """
    if n>100:
        return '100%'
    else:
        return f'{n}%'

app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('logo-sechenov.png'), style={'width':'100%','height':'100%','margin':'0px'})
        ],style={'width':'20%','height':'100px', 'margin':'0px'}),
        html.Div([
            html.Div([
                html.Div([
                    html.P('ФИО:',style={'margin':'0px'}), html.B(f'{name}',style={'margin':'0px','margin-left':'5px'})
                ],style={'margin':'0px','display':'flex', 'justify-content':'left', 'width':'40%'}),
                html.Div([
                    html.P('Дата:',style={'margin':'0px'}), html.B(f'{date}',style={'margin':'0px','margin-left':'5px'})
                ],style={'margin':'0px','display':'flex', 'justify-content':'left', 'width':'40%'}),
                html.Div([
                    html.P('Возраст:',style={'margin':'0px'}), html.B(f'{age}',style={'margin':'0px','margin-left':'5px'})
                ],style={'margin':'0px','display':'flex', 'justify-content':'left', 'width':'40%'}),
                html.Div([
                    html.P('Пол:',style={'margin':'0px'}), html.B(f'{gender}',style={'margin':'0px','margin-left':'5px'})
                ],style={'margin':'0px','display':'flex', 'justify-content':'left', 'width':'40%',}), 
            ],style={'margin-top':'10px','margin-left':'25px','color':'black','font-family':'Calibri','font-size':'15px'}),
            
        ],style={'width':'80%','height':'100px', 'color':'white','margin':'0px','background-image':'url("/assets/rHeader.png")','background-repeat':'no-repeat','background-size':'100%','background-position':'center'}),
    ], style={'display':'flex', 'justify-content':'space-between','width':'100%','height':'100px','margin-bottom':'10px'}),
    html.Div([
        html.H1(children='Панорамный метаболомный обзор', style={'textAlign':'center','margin':'0px'}),]
             , style={'width':'100%','background-color':'#336CA6', 'color':'white','font-family':'Calibri','margin':'0px'}),
    html.Div([
        html.Div([
            html.P('На графике представлены функциональные группы метаболитов, которые были оценены по уровню риска на основе Ваших результатов метаболомного профилирования',
                    style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px','height':'60px'}),
            # html.Br(),
            # html.Img(src=app.get_asset_url('level_of_risk.png'), style={'width':'100%','height':'100%'}),
            html.Div([
                html.H3(children='Уровень риска', style={'textAlign':'left', 'color':'#336CA6','font-family':'Calibri','margin':'0px','margin-top':'5px',}),
                # html.Img(src=app.get_asset_url('rArrow.png'), style={'width':'25px'}),
            ],style={'display':'flex', 'width':'100%','height':'30px'}),
            html.Div([
                html.Img(src=app.get_asset_url('risk_bar.png'), style={'width':'100%','pointer-events':'none'}),
            ], style={'margin':'0px', 'width':'100%','height':'50px'}),
            html.Div([
                
            ], style={'display':'flex', 'justify-content':'space-between', 'width':'100%','height':'330px','border':'1px solid black'}),
        ], style={ 'width':'65%',}),
        html.Div([
            html.Div([
                html.Img(src=app.get_asset_url('people.png'), style={'width':'150px','height':'150px','margin':'0px','margin-top':'10px'}),
                      ], style={'height':'170px','text-align':'center'}),
            html.P('На основании панорамного метаболомного профиля был оценен темп старения организма',style={'color':'black','height':'60px','font-family':'Calibri','font-size':'16px','margin':'0px','margin-left':'10px','text-align':"left "}),
            html.Div([], style={'height':'190px','border':'1px solid black'}),
            html.Div([], style={'height':'47px','border':'1px solid black'}),    
        ], style={'width':'35%',}),
    ], style={'display':'flex', 'justify-content':'space-between', 'width':'100%'}),
    html.Div([
        html.P('Ниже показано, какие классы метаболитов составляют функциональные группы, и как изменение в классе метаболитов повлияло на результат Панорамного метаболомного обзора.',
                style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px','text-align':"left"}),
        ], style={'width':'100%'}),
    html.Div([
        html.Div([
            html.Div([
                html.P('1. Обмен веществ – (',style={'margin':'0px','margin-bottom':'1px'}),html.B(f'{obmen_veshestv}',style={'margin':'0px'}),html.P('%)',style={'margin':'0px'})    
            ], style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-bottom':'1px'}),
            html.Hr(style={'margin':'0px','height':'2px','border-width':'0px','background-color':'#336CA6'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_veshestv_list[0])}','background-color':f'{get_color(obmen_veshestv_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center','margin-left':'2px'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Карнитин',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_veshestv_list[1])}','background-color':f'{get_color(obmen_veshestv_list[1])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Короткоцепочечные ацилкарнитины',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_veshestv_list[2])}','background-color':f'{get_color(obmen_veshestv_list[2])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Среднецепочечные ацилкарнитины',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_veshestv_list[3])}','background-color':f'{get_color(obmen_veshestv_list[3])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Длинноцепочечные ацилкарнитины',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_veshestv_list[4])}','background-color':f'{get_color(obmen_veshestv_list[4])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Функция эндотелия сосудов',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),



            html.Div([
                html.P('3. Нутриентный статус – (',style={'margin':'0px','margin-bottom':'1px'}),html.B(f'{nutrieviy_status}',style={'margin':'0px'}),html.P('%)',style={'margin':'0px'})    
            ], style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-top':'24px','margin-bottom':'1px'}),
            html.Hr(style={'margin':'0px','height':'2px','border-width':'0px','background-color':'#336CA6'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(nutrieviy_status_list[0])}','background-color':f'{get_color(nutrieviy_status_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Витамины',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(nutrieviy_status_list[1])}','background-color':f'{get_color(nutrieviy_status_list[1])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Метаболизм холина',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(nutrieviy_status_list[2])}','background-color':f'{get_color(nutrieviy_status_list[2])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Потребление рыбы',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(nutrieviy_status_list[3])}','background-color':f'{get_color(nutrieviy_status_list[3])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Потребление растительной пищи',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(nutrieviy_status_list[4])}','background-color':f'{get_color(nutrieviy_status_list[4])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Потребление мяса',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),



            html.Div([
                html.P('5. Токсическое воздействие – (',style={'margin':'0px','margin-bottom':'1px'}),html.B(f'{toxicheskie_vosdeystvia}',style={'margin':'0px'}),html.P('%)',style={'margin':'0px'})    
            ], style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-top':'6px','margin-bottom':'1px'}),
            html.Hr(style={'margin':'0px','height':'2px','border-width':'0px','background-color':'#336CA6'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(toxicheskie_vosdeystvia_list[0])}','background-color':f'{get_color(toxicheskie_vosdeystvia_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Аллергия',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(toxicheskie_vosdeystvia_list[1])}','background-color':f'{get_color(toxicheskie_vosdeystvia_list[1])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Окислительный стресс',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(toxicheskie_vosdeystvia_list[2])}','background-color':f'{get_color(toxicheskie_vosdeystvia_list[2])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Цикл мочевины',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),



            html.Div([
                html.P('7. Воспаление – (',style={'margin':'0px','margin-bottom':'1px'}),html.B(f'{vospalenie}',style={'margin':'0px'}),html.P('%)',style={'margin':'0px'})    
            ], style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-top':'6px','margin-bottom':'1px'}),
            html.Hr(style={'margin':'0px','height':'2px','border-width':'0px','background-color':'#336CA6'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(vospalenie_list[0])}','background-color':f'{get_color(vospalenie_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Маркеры воспаления',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),


            html.Div([
                html.P('9. Функция печени – (',style={'margin':'0px','margin-bottom':'1px'}),html.B(f'{functii_pecheni}',style={'margin':'0px'}),html.P('%)',style={'margin':'0px'})    
            ], style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-top':'6px','margin-bottom':'1px'}),
            html.Hr(style={'margin':'0px','height':'2px','border-width':'0px','background-color':'#336CA6'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(functii_pecheni_list[0])}','background-color':f'{get_color(functii_pecheni_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Индекс Фишера',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(functii_pecheni_list[1])}','background-color':f'{get_color(functii_pecheni_list[1])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Индекс Aor',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(functii_pecheni_list[2])}','background-color':f'{get_color(functii_pecheni_list[2])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Индекс GABR',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(functii_pecheni_list[3])}','background-color':f'{get_color(functii_pecheni_list[3])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Индекс GSG',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            

        ], style={'width':'38%','height':'480px'}),
        html.Div([
            html.Div([
                html.P('2. Обмен аминокислот – (',style={'margin':'0px'}),html.B(f'{obmen_aminokislot}',style={'margin':'0px'}),html.P('%)',style={'margin':'0px'})    
            ], style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left'}),
            html.Hr(style={'margin':'0px','height':'2px','border-width':'0px','background-color':'#336CA6','width':'94%'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_aminokislot_list[0])}','background-color':f'{get_color(obmen_aminokislot_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Метаболизм фенилаланина',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'78%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_aminokislot_list[1])}','background-color':f'{get_color(obmen_aminokislot_list[1])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Метаболизм аминокислот с разветвленной боковой цепью',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'78%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_aminokislot_list[2])}','background-color':f'{get_color(obmen_aminokislot_list[2])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Метаболизм триптофана',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'78%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_aminokislot_list[3])}','background-color':f'{get_color(obmen_aminokislot_list[3])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Метионин',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'78%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_aminokislot_list[4])}','background-color':f'{get_color(obmen_aminokislot_list[4])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Гистидин',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'78%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_aminokislot_list[5])}','background-color':f'{get_color(obmen_aminokislot_list[5])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Глутаминовая кислота и аспарагиновая кислота',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'78%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),



            html.Div([
                html.P('4. Стресс и нейромедиаторы – (',style={'margin':'0px'}),html.B(f'{nutrieviy_status}',style={'margin':'0px'}),html.P('%)',style={'margin':'0px'})    
            ], style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-top':'9px'}),
            html.Hr(style={'margin':'0px','height':'2px','border-width':'0px','background-color':'#336CA6','width':'94%'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(stress_i_neyromoderatory_list[0])}','background-color':f'{get_color(stress_i_neyromoderatory_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Стероидные гормоны',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'78%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(stress_i_neyromoderatory_list[1])}','background-color':f'{get_color(stress_i_neyromoderatory_list[1])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Нейромедиаторы',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'78%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(stress_i_neyromoderatory_list[2])}','background-color':f'{get_color(stress_i_neyromoderatory_list[2])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Метаболизм фенилаланина',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'78%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(stress_i_neyromoderatory_list[3])}','background-color':f'{get_color(stress_i_neyromoderatory_list[3])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Синтез серотонина и мелатонина',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'78%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),



            html.Div([
                html.P('6. Маркеры микробиоты – (',style={'margin':'0px'}),html.B(f'{toxicheskie_vosdeystvia}',style={'margin':'0px'}),html.P('%)',style={'margin':'0px'})    
            ], style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-top':'26px'}),
            html.Hr(style={'margin':'0px','height':'2px','border-width':'0px','background-color':'#336CA6','width':'94%'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(markery_mikrobioty_list[0])}','background-color':f'{get_color(markery_mikrobioty_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('ТМАО (триметиламин-N-оксид)',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'78%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(markery_mikrobioty_list[1])}','background-color':f'{get_color(markery_mikrobioty_list[1])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Индольный путь метаболизма триптофана',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'78%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),



            html.Div([
                html.P('8. Функция сердца – (',style={'margin':'0px'}),html.B(f'{vospalenie}',style={'margin':'0px'}),html.P('%)',style={'margin':'0px'})    
            ], style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-top':'25px'}),
            html.Hr(style={'margin':'0px','height':'2px','border-width':'0px','background-color':'#336CA6','width':'94%'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(funcii_serdca_list[0])}','background-color':f'{get_color(funcii_serdca_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Метаболизм аминокислот с разветвленной боковой цепью',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'78%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
                        html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(funcii_serdca_list[1])}','background-color':f'{get_color(funcii_serdca_list[1])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Окислительный стресс',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'78%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
                        html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(funcii_serdca_list[2])}','background-color':f'{get_color(funcii_serdca_list[2])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Функция эндотелия сосудов',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'78%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
                        html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(funcii_serdca_list[3])}','background-color':f'{get_color(funcii_serdca_list[3])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Системные маркеры',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px'})
                ],style={'width':'78%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
        ], style={'width':'57%','height':'480px',})
    ], style={'display':'flex', 'justify-content':'space-between','height':'480px'}),
    html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
           style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px','text-align':"left",'font-style':'italic','margin-top':'5px'}),
    ],style={'margin-left':'10px', 'margin-right':'10px','width':'800px'})
    
    

if __name__ == '__main__':
    app.run(debug=True)