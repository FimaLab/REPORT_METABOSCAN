from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
import matplotlib as mpl
from typing import List
import matplotlib.colors as mcolors

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

N = 1000
a = 3.5   
value = 1

part = [20, 25, 30, 40, 50 ,55, 45, 50, 30]

procent_speed = 70

def normal_dist(N, a, value):
    x = np.linspace(-a, a, N)
    y = (1 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * x**2)  # Формула для нормального распределения

    cmap = mpl.colors.LinearSegmentedColormap.from_list("", ["#0db350","#edd30e", "#ff051e"],gamma=1.2)

    plt.figure(figsize=(10, 5))

    plt.ylim(min(y), max(y) + 0.00001)

    plt.xticks([])  # Убрать деления по оси X
    plt.yticks([])  # Убрать деления по оси Y

    for pos in ['top', 'bottom', 'left', 'right']:
        plt.gca().spines[pos].set_visible(False)

    # print(x[1], len(y))

    for i in range(N-1):
        plt.fill_between([x[i], x[i+1]], [0, 0], [y[i], y[i+1]], color=cmap((x[i]+a)*N/(a*2)/N))

    plt.plot(x, y, color='grey')

    plt.axvline(value, ymin=min(y) * 1/max(y), ymax=1,color='#356ba6', linestyle='-', linewidth=3, clip_on=True)

    plt.savefig("assets/normal.png", bbox_inches='tight' , pad_inches=0)
    return 'normal.png'

def main_plot(part):
    names = ['Обмен веществ', 'Обмен аминокислот', 'Нутриентный статус', 'Стресс и нейромедиаторы', 
         'Токсическое воздействие', 'Маркеры микробиоты', 'Воспаление', 'Функция сердца', 'Функция печени']

    numbers=[1,2,3,4,5,6,7,8,9]

    y_line = np.linspace(14.3,0.2,9)

    plt.figure(figsize=(7,5))
    plt.plot(part, y_line, 'ro', marker='o', markersize=0)

    plt.rcParams['font.family'] = 'bahnschrift'
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['savefig.dpi'] = 300
    plt.grid(True, linewidth=0.5, color = 'Grey', which='major')

    plt.xlim(0,100)
    plt.ylim(-1,15)

    plt.yticks(np.linspace(-1,16,11),c='white')
    plt.xticks(np.linspace(0,100,11), c='b')

    for label in plt.gca().get_xticklabels():
        if label.get_text() in ['0', '20', '40', '60', '80', '100']:
            label.set_visible(True)
        else:
            label.set_visible(False)
            
    cmap = mpl.colors.LinearSegmentedColormap.from_list("", ["#77DD77","#FCE883", "#E4717A"],gamma=1.0)

    n=0
    for i_x, i_y in zip(part, y_line):
        number = dict(boxstyle='circle', facecolor='white', alpha=1, edgecolor='black')

        prop = dict(boxstyle='Round', facecolor=cmap(i_x/100), alpha=1, edgecolor=cmap(i_x/100),pad=0.8)

        plt.text(i_x+1, i_y+0.7, names[n], color = 'black',  bbox=prop, fontsize = 9)
        plt.text(i_x, i_y, numbers[n], color = 'black',  bbox=number, fontsize = 7)
        n=n+1
    plt.gca().spines['bottom'].set_color('blue')
    plt.gca().spines['top'].set_color('blue')
    plt.gca().spines['right'].set_color('blue')
    plt.gca().spines['left'].set_color('blue')

    plt.ylabel('')
    plt.gca().set_yticklabels([])
    
    fig = plt.Figure()
    fig.set_canvas(plt.gcf().canvas)

    plt.savefig("assets/main.png", bbox_inches='tight', pad_inches=0)
    return 'main.png'

def color_marker(value: float, lines: List[float] = [25*256/100, 75*256/100]) -> str:
    colors = ['red', 'yellow', 'green', 'yellow', 'red']  # красный - зеленый - красный
    n_bins = 256
    cmap_name = 'custom_gradient'
    cm = mcolors.LinearSegmentedColormap.from_list(cmap_name, colors, N=256)

    # Создание данных для градиента
    gradient_data = np.linspace(0, 1, n_bins).reshape(1, -1)
    plt.figure(figsize=(9,1))
    plt.imshow(gradient_data, aspect='auto', cmap=cm, origin='lower')
    plt.xticks([])  
    plt.yticks([])  

    
    plt.scatter(value, 0.45, color='black', s=350, marker = 'v',clip_on=False) 

    for i in lines:
        plt.axvline(i, ymax=10,color='black', linestyle='-', linewidth=1, clip_on=False)
    
    plt.axis('off')

    plt.savefig("assets/colorbar.png", bbox_inches='tight', pad_inches=0)
    return 'colorbar.png'

    
def color_marker_green(value: float, lines: List[float] = [75*256/100]) -> str:
    colors = ['green', 'yellow', 'red']  # красный - зеленый - красный
    n_bins = 256
    cmap_name = 'custom_gradient'
    cm = mcolors.LinearSegmentedColormap.from_list(cmap_name, colors, N=256, gamma=2.5)

    # Создание данных для градиента
    gradient_data = np.linspace(0, 1, n_bins).reshape(1, -1)
    plt.figure(figsize=(9,1))
    plt.imshow(gradient_data, aspect='auto', cmap=cm, origin='lower')
    plt.xticks([])  # Убрать деления по оси X
    plt.yticks([])  # Убрать деления по оси Y

    plt.scatter(value, 0.45, color='black', s=350, marker = 'v',clip_on=False)

    for i in lines:
        plt.axvline(i, ymax=10,color='black', linestyle='-', linewidth=1, clip_on=False)
    
    plt.axis('off')

    plt.savefig("assets/colorbar2.png", bbox_inches='tight', pad_inches=0)
    return 'colorbar2.png'

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
    

def get_color_under_normal_dist(n):
    if n < 30:
        return '#50c150'
    elif n < 60:
        return '#9fd047'
    elif n < 80:
        return '#feb61d'
    else:
        return '#de6d54'
    
def get_text_from_procent(n):
    if n < 30:
        return 'Замедленный'
    elif n < 60:
        return 'Нормальный'
    elif n < 80:
        return 'Умеренно ускоренный'
    else:
        return 'Сильно ускоренный'
    

app = Dash(__name__)

app.layout = html.Div([
    # 1 страница
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
                html.Img(src=app.get_asset_url('risk_bar.png'), style={'width':'98.2%','pointer-events':'none'}),
            ], style={'margin':'0px', 'width':'100%','height':'50px'}),
            html.Div([
                html.Img(src=app.get_asset_url(f'{main_plot(part=part)}'), style={'width':'100%','margin-top':'10px'}),
            ], style={'display':'flex', 'justify-content':'space-between', 'width':'100%','height':'330px'}),
        ], style={ 'width':'65%',}),
        html.Div([
            html.Div([
                html.Img(src=app.get_asset_url('people.png'), style={'width':'180px','height':'180px','margin':'0px','margin-top':'10px'}),
                      ], style={'height':'190px','text-align':'center'}),
            html.P('На основании панорамного метаболомного профиля был оценен темп старения организма',style={'color':'black','height':'60px','font-family':'Calibri','font-size':'16px','margin':'0px','margin-left':'10px','text-align':"left "}),
            html.Div([html.Img(src=app.get_asset_url(f'{normal_dist(N,a,value)}'), style={'width':'100%','margin-top':'10px'})], style={'height':'150px'}),
            html.Div([
                html.P("медленно",style={'margin':'0px','margin-left':'10px'}),
                html.P("нормально",style={'margin':'0px'}),
                html.P("быстро",style={'margin':'0px','margin-right':'10px'}),
            ],style={'height':'20px','display':'flex', 'justify-content':'space-between', 'width':'100%','font-family':'Calibri','font-size':'16px','margin':'0px'}),
            html.Div([
                html.P(f'{get_text_from_procent(procent_speed)}',style={'margin':'0','font-size':'18px','color':'white','font-family':'Calibri','font-weight':'bold','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            ], style={'height':'47px','background-color':f'{get_color_under_normal_dist(procent_speed)}','line-height':'47px','text-align':'center','margin-left':'40px','margin-right':'40px'}),    
        ], style={'width':'35%',}),
    ], style={'display':'flex', 'justify-content':'space-between', 'width':'100%'}),
    html.Div([
        html.P('Ниже показано, какие классы метаболитов составляют функциональные группы, и как изменение в классе метаболитов повлияло на результат Панорамного метаболомного обзора.',
                style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px','text-align':"left"}),
        ], style={'width':'100%'}),
    html.Div([
        html.Div([
            html.Div([
                html.P('1. Обмен веществ – (',style={'margin':'0px','margin-bottom':'1px'}),html.B(f'{obmen_veshestv}%',style={'margin':'0px'}),html.P(')',style={'margin':'0px'}),
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_veshestv)}','background-color':f'{get_color_under_normal_dist(obmen_veshestv)}','border-radius':'2px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center','margin-left':'5px','margin-top':'6px'}),
                ],style={'width':'50px','height':'18px','line-height':'18px'}),
            ], style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-bottom':'1px'}),
            html.Hr(style={'margin':'0px','height':'2px','border-width':'0px','background-color':'#336CA6'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_veshestv_list[0])}','background-color':f'{get_color(obmen_veshestv_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Карнитин',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'75%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_veshestv_list[1])}','background-color':f'{get_color(obmen_veshestv_list[1])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Короткоцепочечные ацилкарнитины',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_veshestv_list[2])}','background-color':f'{get_color(obmen_veshestv_list[2])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Среднецепочечные ацилкарнитины',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_veshestv_list[3])}','background-color':f'{get_color(obmen_veshestv_list[3])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Длинноцепочечные ацилкарнитины',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_veshestv_list[4])}','background-color':f'{get_color(obmen_veshestv_list[4])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Функция эндотелия сосудов',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),



            html.Div([
                html.P('3. Нутриентный статус – (',style={'margin':'0px','margin-bottom':'1px'}),html.B(f'{nutrieviy_status}%',style={'margin':'0px'}),html.P(')',style={'margin':'0px'}),
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(nutrieviy_status)}','background-color':f'{get_color_under_normal_dist(nutrieviy_status)}','border-radius':'2px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center','margin-left':'5px','margin-top':'6px'}),
                ],style={'width':'50px','height':'18px','line-height':'18px'}),  
            ], style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-top':'24px','margin-bottom':'1px'}),
            html.Hr(style={'margin':'0px','height':'2px','border-width':'0px','background-color':'#336CA6'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(nutrieviy_status_list[0])}','background-color':f'{get_color(nutrieviy_status_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Витамины',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(nutrieviy_status_list[1])}','background-color':f'{get_color(nutrieviy_status_list[1])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Метаболизм холина',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(nutrieviy_status_list[2])}','background-color':f'{get_color(nutrieviy_status_list[2])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Потребление рыбы',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(nutrieviy_status_list[3])}','background-color':f'{get_color(nutrieviy_status_list[3])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Потребление растительной пищи',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(nutrieviy_status_list[4])}','background-color':f'{get_color(nutrieviy_status_list[4])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Потребление мяса',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),



            html.Div([
                html.P('5. Токсическое воздействие – (',style={'margin':'0px','margin-bottom':'1px'}),html.B(f'{toxicheskie_vosdeystvia}%',style={'margin':'0px'}),html.P(')',style={'margin':'0px'}),
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(toxicheskie_vosdeystvia)}','background-color':f'{get_color_under_normal_dist(toxicheskie_vosdeystvia)}','border-radius':'2px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center','margin-left':'5px','margin-top':'6px'}),
                ],style={'width':'50px','height':'18px','line-height':'18px'}),
            ], style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-top':'6px','margin-bottom':'1px'}),
            html.Hr(style={'margin':'0px','height':'2px','border-width':'0px','background-color':'#336CA6'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(toxicheskie_vosdeystvia_list[0])}','background-color':f'{get_color(toxicheskie_vosdeystvia_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Аллергия',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(toxicheskie_vosdeystvia_list[1])}','background-color':f'{get_color(toxicheskie_vosdeystvia_list[1])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Окислительный стресс',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(toxicheskie_vosdeystvia_list[2])}','background-color':f'{get_color(toxicheskie_vosdeystvia_list[2])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Цикл мочевины',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),



            html.Div([
                html.P('7. Воспаление – (',style={'margin':'0px','margin-bottom':'1px'}),html.B(f'{vospalenie}%',style={'margin':'0px'}),html.P(')',style={'margin':'0px'}),
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(vospalenie)}','background-color':f'{get_color_under_normal_dist(vospalenie)}','border-radius':'2px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center','margin-left':'5px','margin-top':'5px'}),
                ],style={'width':'50px','height':'18px','line-height':'18px'}),
            ], style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-top':'6px','margin-bottom':'1px'}),
            html.Hr(style={'margin':'0px','height':'2px','border-width':'0px','background-color':'#336CA6'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(vospalenie_list[0])}','background-color':f'{get_color(vospalenie_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Маркеры воспаления',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),


            html.Div([
                html.P('9. Функция печени – (',style={'margin':'0px','margin-bottom':'1px'}),html.B(f'{functii_pecheni}%',style={'margin':'0px'}),html.P(')',style={'margin':'0px'}),
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(functii_pecheni)}','background-color':f'{get_color_under_normal_dist(functii_pecheni)}','border-radius':'2px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center','margin-left':'5px','margin-top':'6px'}),
                ],style={'width':'50px','height':'18px','line-height':'18px'}),  
            ], style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-top':'6px','margin-bottom':'1px'}),
            html.Hr(style={'margin':'0px','height':'2px','border-width':'0px','background-color':'#336CA6'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(functii_pecheni_list[0])}','background-color':f'{get_color(functii_pecheni_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Индекс Фишера',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(functii_pecheni_list[1])}','background-color':f'{get_color(functii_pecheni_list[1])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Индекс Aor',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(functii_pecheni_list[2])}','background-color':f'{get_color(functii_pecheni_list[2])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Индекс GABR',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(functii_pecheni_list[3])}','background-color':f'{get_color(functii_pecheni_list[3])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Индекс GSG',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            

        ], style={'width':'38%','height':'480px'}),
        html.Div([
            html.Div([
                html.P('2. Обмен аминокислот – (',style={'margin':'0px'}),html.B(f'{obmen_aminokislot}%',style={'margin':'0px'}),html.P(')',style={'margin':'0px'}),
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_aminokislot)}','background-color':f'{get_color_under_normal_dist(obmen_aminokislot)}','border-radius':'2px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center','margin-left':'5px','margin-top':'6px'}),
                ],style={'width':'50px','height':'18px','line-height':'18px'}),  
            ], style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-top':'2px'}),
            html.Hr(style={'margin':'0px','height':'2px','border-width':'0px','background-color':'#336CA6','width':'94%'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_aminokislot_list[0])}','background-color':f'{get_color(obmen_aminokislot_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Метаболизм фенилаланина',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'79%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_aminokislot_list[1])}','background-color':f'{get_color(obmen_aminokislot_list[1])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Метаболизм аминокислот с разветвленной боковой цепью',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'79%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_aminokislot_list[2])}','background-color':f'{get_color(obmen_aminokislot_list[2])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Метаболизм триптофана',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'79%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_aminokislot_list[3])}','background-color':f'{get_color(obmen_aminokislot_list[3])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Метионин',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'79%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_aminokislot_list[4])}','background-color':f'{get_color(obmen_aminokislot_list[4])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Гистидин',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'79%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_aminokislot_list[5])}','background-color':f'{get_color(obmen_aminokislot_list[5])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Глутаминовая кислота и аспарагиновая кислота',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'79%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),



            html.Div([
                html.P('4. Стресс и нейромедиаторы – (',style={'margin':'0px'}),html.B(f'{stress_i_neyromoderatory}%',style={'margin':'0px'}),html.P(')',style={'margin':'0px'}),
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(stress_i_neyromoderatory)}','background-color':f'{get_color_under_normal_dist(stress_i_neyromoderatory)}','border-radius':'2px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center','margin-left':'5px','margin-top':'6px'}),
                ],style={'width':'50px','height':'18px','line-height':'18px'}),   
            ], style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-top':'8px'}),
            html.Hr(style={'margin':'0px','height':'2px','border-width':'0px','background-color':'#336CA6','width':'94%'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(stress_i_neyromoderatory_list[0])}','background-color':f'{get_color(stress_i_neyromoderatory_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Стероидные гормоны',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'79%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(stress_i_neyromoderatory_list[1])}','background-color':f'{get_color(stress_i_neyromoderatory_list[1])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Нейромедиаторы',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'79%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(stress_i_neyromoderatory_list[2])}','background-color':f'{get_color(stress_i_neyromoderatory_list[2])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Метаболизм фенилаланина',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'79%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(stress_i_neyromoderatory_list[3])}','background-color':f'{get_color(stress_i_neyromoderatory_list[3])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Синтез серотонина и мелатонина',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'79%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),



            html.Div([
                html.P('6. Маркеры микробиоты – (',style={'margin':'0px'}),html.B(f'{markery_mikrobioty}%',style={'margin':'0px'}),html.P(')',style={'margin':'0px'}),
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(markery_mikrobioty)}','background-color':f'{get_color_under_normal_dist(markery_mikrobioty)}','border-radius':'2px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center','margin-left':'5px','margin-top':'6px'}),
                ],style={'width':'50px','height':'18px','line-height':'18px'}),    
            ], style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-top':'26px'}),
            html.Hr(style={'margin':'0px','height':'2px','border-width':'0px','background-color':'#336CA6','width':'94%'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(markery_mikrobioty_list[0])}','background-color':f'{get_color(markery_mikrobioty_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('ТМАО (триметиламин-N-оксид)',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'79%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(markery_mikrobioty_list[1])}','background-color':f'{get_color(markery_mikrobioty_list[1])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Индольный путь метаболизма триптофана',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'79%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),



            html.Div([
                html.P('8. Функция сердца – (',style={'margin':'0px'}),html.B(f'{funcii_serdca}%',style={'margin':'0px'}),html.P(')',style={'margin':'0px'}),
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(funcii_serdca)}','background-color':f'{get_color_under_normal_dist(funcii_serdca)}','border-radius':'2px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center','margin-left':'5px','margin-top':'6px'}),
                ],style={'width':'50px','height':'18px','line-height':'18px'}),    
            ], style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-top':'26px'}),
            html.Hr(style={'margin':'0px','height':'2px','border-width':'0px','background-color':'#336CA6','width':'94%'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(funcii_serdca_list[0])}','background-color':f'{get_color(funcii_serdca_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Метаболизм аминокислот с разветвленной боковой цепью',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'79%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
                        html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(funcii_serdca_list[1])}','background-color':f'{get_color(funcii_serdca_list[1])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Окислительный стресс',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'79%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
                        html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(funcii_serdca_list[2])}','background-color':f'{get_color(funcii_serdca_list[2])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Функция эндотелия сосудов',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'79%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
                        html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(funcii_serdca_list[3])}','background-color':f'{get_color(funcii_serdca_list[3])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Системные маркеры',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
                ],style={'width':'79%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
        ], style={'width':'57%','height':'480px',})
    ], style={'display':'flex', 'justify-content':'space-between','height':'480px','margin-top':'5px'}),
    html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
           style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"left",'font-style':'italic','margin-top':'5px'}),

    # 2 страница
    html.Div([
        html.Div([],style={'height':'8mm','width':'100%'}),
        html.Div([
            html.Div([
                html.B(f"Дата: {date}",style={'margin':'0px','font-size':'18px','font-family':'Calibri'}),
                html.Div([
                    html.B(f'Пациент: {name}',style={'margin':'0px','font-size':'18px','font-family':'Calibri'}),
                ],style={'margin-top':'10px'}),
            ], style={'width':'33.3%'}),
            html.Div([
                html.B("MetaboScan-Test01",style={'margin':'0px','font-size':'18px','font-family':'Calibri'}),
            ], style={'width':'33.3%','text-align':'center'}),
            html.Div([
                html.Img(src=app.get_asset_url('logo.jpg'),style={'height':'54px','float':'right'}),
            ], style={'width':'33.3%'}),
        ], style={'display':'flex', 'justify-content':'space-between','width':'100%','height':'54px','color':'#336CA6'}),    
        html.Div([
        html.H3(children='1. Аминокислоты', style={'textAlign':'center','margin':'0px','line-height':'normal','display':'inline-block','vertical-align':'center'}),]
             , style={'width':'100%','background-color':'#336CA6', 'color':'white','font-family':'Calibri','margin':'0px','height':'35px','line-height':'35px','text-align':'center','margin-top':'5px'}),
        html.Div([
            html.Div([
                html.Div([html.B('Метаболизм фенилаланина',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'36%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#336CA6','line-height':'40px'}),
                html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'40px'}),
                html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'30%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#336CA6','line-height':'40px'}),
                html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center'}),
            ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px'}),
            html.Div([
                html.Div([html.B('Фенилаланин (Phe)',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'36%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','line-height':'40px'}),
                html.Div([html.B('+',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'40px'}),
                html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'30%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#336CA6','line-height':'40px'}),
                html.Div([html.P('35.8 - 76.9')],style={'width':'21%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center'}),
            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'40px','margin-left':'5px'}),
            html.Div([
                html.Div([html.B('Индекс [Glu / Gln]',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'36%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','line-height':'40px'}),
                html.Div([html.B('+',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'40px'}),
                html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'30%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#336CA6','line-height':'40px'}),
                html.Div([html.P('35.8 - 76.9')],style={'width':'21%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center'}),
            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'40px','margin-left':'5px'}),
            html.Div([
                html.Div([html.B('Индекс GSG [Glu / (Ser + Gly)]',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'36%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','line-height':'40px'}),
                html.Div([html.Div([html.B('+',style={'width':'50%'}),html.B('100',style={'width':'50%'})],style={'width':'100%','height':'20px','display':'flex','justify-content':'space-between','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'40px'}),
                html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'30%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#336CA6','line-height':'40px'}),
                html.Div([html.P('35.8 - 76.9')],style={'width':'21%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center'}),
            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'40px','margin-left':'5px'}),
        ], style={'margin':'0px','height':'200px','border':'1px solid black','margin-left':'20px'}),
    ])
    ],style={'margin-right':'5mm','width':'800px'})
    
    

if __name__ == '__main__':
    app.run(debug=True)