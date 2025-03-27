from dash import Dash, html
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from typing import List
import matplotlib.colors as mcolors
import os

app_pid = os.getpid()

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

part = [20, 25, 30, 40, 50 ,55, 45, 50, 90]

procent_speed = 50

ref_1 = ['35.8 - 76.9','27.8 - 83.3','60.0 - 180.0']
value_1 = [100, 50, 40]

ref_2 = ['92.6 - 310.0','133.0 - 317.1','212 - 577','3.0 - 3.5']
value_2 = [240, 404, 644, 2.3]

ref_3 = ['60 - 109','< 47.0','67.8 - 211.6','< 6.3','122 - 322','1.6 - 5.0','65 - 138','119 - 233','10 - 97','373 - 701','0.06 - 0.23','0.17 - 0.31']
value_3 = [158,21.5,132,0.1,218,0.12,148,463,133,489,0.27,0.36]

ref_4 = ['16 - 34','0.5 - 5.0','0.07 - 0.55','50 - 139','21 - 71','5.2 - 13.0','< 6.2','2.6 - 7.7']
value_4 = [49,0.9,0.33,64,29,10.9,12.1,2.8]

ref_5 = ['40 - 91','< 4.4','0.018 - 0.101','0.0049 - 1.1158','0.04 - 0.30','0.0035 - 0.7642','0.002 - 0.037','0.032 - 0.167','0.44 - 5.00']
value_5 = [62,4.6,0.075,0.01,0.10,0.059,0.008,0.098,1.66]

ref_6 = ['0.18 - 1.18','0.04 - 0.30','0.1 - 1.1','0.0153 - 0.0207']
value_6 = [0.57,0.36,0.2,0.018]

ref_7 = ['0.3 - 23','0.08 - 5.0','0.01 - 0.20','0.5 - 12.0','0.001 - 0.400','< 0.003','0.048 - 0.230']
value_7 = [2.67,1.95,0.095,0.61,0.04,0.0,0.148]

ref_8 = ['104 - 383','4.7 - 35.2','0.23 - 0.50','0.20 - 0.67','1.0 - 6.0','32 - 120','16 - 51','38 - 130','29.5 - 84.5','5.4 - 21.5','0.2 - 1.2','0.2 - 1.5','< 26.0','13 - 57']
value_8 = [270,30.4,0.84,1.32,6.7,132,55,124,312,20.2,0.74,1.1,15.4,44]

ref_9 = ['209 - 516','19 - 48','3.23 - 10.30']
value_9 = [664,67,16,5]

ref_10 = ['0.16 - 0.62','0.08 - 0.38','0.04 - 0.61','0.04 - 0.06','< 0.1','< 0.06']
value_10 = [0.43,0.27,0.12,0.01,0.0,0.006]

ref_11 = ['< 0.1','< 0.02','< 0.27','< 1.26','< 0.38','0.01 - 0.32','< 0.05','< 0.15','< 0.19']
value_11 = [0.083,0.002,0.009,0.129,0.285,0.225,0.004,0.103,0.100]

ref_12 = ['0.01 - 0.22','0.04 - 0.41','< 0.16','0.01 - 0.29','< 0.09','< 0.1','< 0.1','< 0.02','0.03 - 0.13','0.07 - 0.51','< 0.32','0.02 - 0.26','0.3 - 2.3']
value_12 = [0.028,0.077,0.040,0.003,0.089,0.019,0.020,0.005,0.026,0.220,0.002,0.073,0.006]

ref_13 = ['0.30 - 1.80','6.2 - 39.0','< 0.00123','0.0002 - 0.0204']
value_13 = [0.23,0.036,0.0,0.012]

ref_14 = ['0.23 - 2.58','0.13 - 0.27']
value_14 = [0.814,0.14]

ref_15 = ['0.1 - 0.5','0.0018 - 0.1329']
value_15 = [0.3,0.012]

def color_text_ref(value: float, ref: str):
    if ref.__contains__(' - '):
        if value < float(ref.split(' - ')[0]):
            return '#ee140b'
        elif value > float(ref.split(' - ')[1]):
            return '#ee140b'
        else:
            return 'black'
    else:
        if value < float(ref.split('< ')[1]):
            return 'black'
        else:
            return '#ee140b'

def need_of_plus(value: float, ref: str):
    if ref.__contains__(' - '):
        if value > float(ref.split(' - ')[1]):
            return '+'
        else:
            return ''
    elif value > float(ref.split('< ')[1]):
        return '+'
    else:
        return ''
    
def need_of_margin(value: float, ref: str):
    if ref.__contains__(' - '):
        if value > float(ref.split(' - ')[1]):
            return '0'
        else:
            return '17px'
    elif value > float(ref.split('< ')[1]):
        return '0'
    else:
        return '17px'


def normal_dist(N: int, a: float, value: float):
    x = np.linspace(-a, a, N)
    y = (1 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * x**2)  # Формула для нормального распределения

    cmap = mpl.colors.LinearSegmentedColormap.from_list("", ["#0db350","#edd30e", "#ff051e"],gamma=1.2)

    plt.figure(figsize=(10, 5))

    plt.ylim(min(y), max(y) + 0.001)

    plt.xticks([])  # Убрать деления по оси X
    plt.yticks([])  # Убрать деления по оси Y

    for pos in ['top', 'bottom', 'left', 'right']:
        plt.gca().spines[pos].set_visible(False)

    # print(x[1], len(y))

    for i in range(N-1):
        plt.fill_between([x[i], x[i+1]], [0, 0], [y[i], y[i+1]], color=cmap((x[i]+a)*N/(a*2)/N))

    plt.plot(x, y, color='grey')

    checked_value = 0
    if value < 0:
        checked_value = 0
    elif value > 100:
        checked_value = 100
    else:
        checked_value = value

    line = 2*a*checked_value/100 - a

    plt.axvline(line, ymin=min(y) * 1/max(y), ymax=1,color='#356ba6', linestyle='-', linewidth=3, clip_on=True)

    plt.savefig("assets/normal.png", bbox_inches='tight' , pad_inches=0)
    return 'normal.png'

def main_plot(part):
    names = ['Обмен веществ', 'Обмен аминокислот', 'Нутриентный статус', 'Стресс и нейромедиаторы', 
         'Токсическое воздействие', 'Маркеры микробиоты', 'Воспаление', 'Функция сердца', 'Функция печени']

    numbers=[1,2,3,4,5,6,7,8,9]

    left_margin = dict(zip(names, [16.8,21.55,21.9,28.3,28,23.4,13,18,18]))

    y_line = np.linspace(14.3,-0.5,9)

    # print(y_line)

    plt.figure(figsize=(7,5))
    # plt.plot(part, y_line, marker='o', markersize=0)

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

        if i_x > 80:
            mg = left_margin[names[n]]
            plt.text(i_x-mg, i_y+0.7, names[n], color = 'black',  bbox=prop, fontsize = 9)
        else:
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
            ],style={'margin-top':'10px','margin-left':'25px','color':'black','font-family':'Arial','font-size':'15px'}),
            
        ],style={'width':'80%','height':'100px', 'color':'white','margin':'0px','background-image':'url("/assets/rHeader.png")','background-repeat':'no-repeat','background-size':'100%','background-position':'center'}),
    ], style={'display':'flex', 'justify-content':'space-between','width':'100%','height':'100px','margin-bottom':'10px'}),
    html.Div([
        html.H1(children='Панорамный метаболомный обзор', style={'textAlign':'center','margin':'0px'}),]
             , style={'width':'100%','background-color':'#0874bc', 'color':'white','font-family':'Arial','margin':'0px'}),
    html.Div([
        html.Div([
            html.P('На графике представлены функциональные группы метаболитов, которые были оценены по уровню риска на основе Ваших результатов метаболомного профилирования',
                    style={'color':'black','font-family':'Arial','font-size':'16px','margin':'0px','height':'60px'}),
            html.Div([
                html.H3(children='Уровень риска', style={'textAlign':'left', 'color':'#0874bc','font-family':'Arial','margin':'0px','margin-top':'5px',}),
            ],style={'display':'flex', 'width':'100%','height':'30px'}),
            html.Div([
                html.Img(src=app.get_asset_url('risk_bar.png'), style={'width':'100%','pointer-events':'none', 'margin-left':'3px'}),
            ], style={'margin':'0px','height':'50px','margin-right':'10px'}),
            html.Div([
                html.Img(src=app.get_asset_url(f'{main_plot(part=part)}'), style={'width':'100%','margin-top':'10px'}),
            ], style={'display':'flex', 'justify-content':'space-between', 'width':'100%','height':'330px'}),
        ], style={ 'width':'65%',}),
        html.Div([
            html.P('На основании панорамного метаболомного профиля был оценен темп старения организма',style={'color':'black','height':'60px','font-family':'Arial','font-size':'16px','margin':'0px','margin-left':'10px','text-align':"left ",'margin-top':'100px'}),
            html.Div([html.Img(src=app.get_asset_url(f'{normal_dist(N,a,procent_speed)}'), style={'width':'100%','margin-top':'10px'})], style={'height':'150px'}),
            html.Div([
                html.P("медленно",style={'margin':'0px','margin-left':'10px'}),
                html.P("нормально",style={'margin':'0px'}),
                html.P("быстро",style={'margin':'0px','margin-right':'10px'}),
            ],style={'height':'20px','display':'flex', 'justify-content':'space-between', 'width':'100%','font-family':'Arial','font-size':'16px','margin':'0px'}),
            html.Div([
                html.P(f'{get_text_from_procent(procent_speed)}',style={'margin':'0','font-size':'18px','color':'white','font-family':'Arial','font-weight':'bold','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            ], style={'height':'47px','background-color':f'{get_color_under_normal_dist(procent_speed)}','line-height':'47px','text-align':'center','margin-left':'40px','margin-right':'40px'}),    
        ], style={'width':'35%',}),
    ], style={'display':'flex', 'justify-content':'space-between', 'width':'100%'}),
    html.Div([
        html.P('Ниже показано, какие классы метаболитов составляют функциональные группы, и как изменение в классе метаболитов повлияло на результат Панорамного метаболомного обзора.',
                style={'color':'black','font-family':'Arial','font-size':'16px','margin':'0px','text-align':"left"}),
        ], style={'width':'100%'}),
    html.Div([
        html.Div([
            html.Div([
                html.P('1. Обмен веществ – (',style={'margin':'0px','margin-bottom':'1px'}),html.B(f'{obmen_veshestv}%',style={'margin':'0px'}),html.P(')',style={'margin':'0px'}),
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_veshestv)}','background-color':f'{get_color_under_normal_dist(obmen_veshestv)}','border-radius':'2px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center','margin-left':'5px','margin-top':'6px'}),
                ],style={'width':'50px','height':'18px','line-height':'18px'}),
            ], style={'color':'black','font-family':'Arial','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-bottom':'1px'}),
            
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_veshestv_list[0])}','background-color':f'{get_color(obmen_veshestv_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Карнитин',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'75%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_veshestv_list[1])}','background-color':f'{get_color(obmen_veshestv_list[1])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Короткоцепочечные ацилкарнитины',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_veshestv_list[2])}','background-color':f'{get_color(obmen_veshestv_list[2])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Среднецепочечные ацилкарнитины',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_veshestv_list[3])}','background-color':f'{get_color(obmen_veshestv_list[3])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Длинноцепочечные ацилкарнитины',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_veshestv_list[4])}','background-color':f'{get_color(obmen_veshestv_list[4])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Функция эндотелия сосудов',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),



            html.Div([
                html.P('3. Нутриентный статус – (',style={'margin':'0px','margin-bottom':'1px'}),html.B(f'{nutrieviy_status}%',style={'margin':'0px'}),html.P(')',style={'margin':'0px'}),
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(nutrieviy_status)}','background-color':f'{get_color_under_normal_dist(nutrieviy_status)}','border-radius':'2px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center','margin-left':'5px','margin-top':'6px'}),
                ],style={'width':'50px','height':'18px','line-height':'18px'}),  
            ], style={'color':'black','font-family':'Arial','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-top':'24px','margin-bottom':'1px'}),
            
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(nutrieviy_status_list[0])}','background-color':f'{get_color(nutrieviy_status_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Витамины',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(nutrieviy_status_list[1])}','background-color':f'{get_color(nutrieviy_status_list[1])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Метаболизм холина',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(nutrieviy_status_list[2])}','background-color':f'{get_color(nutrieviy_status_list[2])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Потребление рыбы',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(nutrieviy_status_list[3])}','background-color':f'{get_color(nutrieviy_status_list[3])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Потребление растительной пищи',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(nutrieviy_status_list[4])}','background-color':f'{get_color(nutrieviy_status_list[4])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Потребление мяса',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),



            html.Div([
                html.P('5. Токсическое воздействие – (',style={'margin':'0px','margin-bottom':'1px'}),html.B(f'{toxicheskie_vosdeystvia}%',style={'margin':'0px'}),html.P(')',style={'margin':'0px'}),
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(toxicheskie_vosdeystvia)}','background-color':f'{get_color_under_normal_dist(toxicheskie_vosdeystvia)}','border-radius':'2px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center','margin-left':'5px','margin-top':'6px'}),
                ],style={'width':'50px','height':'18px','line-height':'18px'}),
            ], style={'color':'black','font-family':'Arial','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-top':'6px','margin-bottom':'1px'}),
            
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(toxicheskie_vosdeystvia_list[0])}','background-color':f'{get_color(toxicheskie_vosdeystvia_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Аллергия',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(toxicheskie_vosdeystvia_list[1])}','background-color':f'{get_color(toxicheskie_vosdeystvia_list[1])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Окислительный стресс',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(toxicheskie_vosdeystvia_list[2])}','background-color':f'{get_color(toxicheskie_vosdeystvia_list[2])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Цикл мочевины',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),



            html.Div([
                html.P('7. Воспаление – (',style={'margin':'0px','margin-bottom':'1px'}),html.B(f'{vospalenie}%',style={'margin':'0px'}),html.P(')',style={'margin':'0px'}),
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(vospalenie)}','background-color':f'{get_color_under_normal_dist(vospalenie)}','border-radius':'2px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center','margin-left':'5px','margin-top':'5px'}),
                ],style={'width':'50px','height':'18px','line-height':'18px'}),
            ], style={'color':'black','font-family':'Arial','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-top':'6px','margin-bottom':'1px'}),
            
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(vospalenie_list[0])}','background-color':f'{get_color(vospalenie_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Маркеры воспаления',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),


            html.Div([
                html.P('9. Функция печени – (',style={'margin':'0px','margin-bottom':'1px'}),html.B(f'{functii_pecheni}%',style={'margin':'0px'}),html.P(')',style={'margin':'0px'}),
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(functii_pecheni)}','background-color':f'{get_color_under_normal_dist(functii_pecheni)}','border-radius':'2px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center','margin-left':'5px','margin-top':'6px'}),
                ],style={'width':'50px','height':'18px','line-height':'18px'}),  
            ], style={'color':'black','font-family':'Arial','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-top':'6px','margin-bottom':'1px'}),
            
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(functii_pecheni_list[0])}','background-color':f'{get_color(functii_pecheni_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Индекс Фишера',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(functii_pecheni_list[1])}','background-color':f'{get_color(functii_pecheni_list[1])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Индекс Aor',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(functii_pecheni_list[2])}','background-color':f'{get_color(functii_pecheni_list[2])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Индекс GABR',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(functii_pecheni_list[3])}','background-color':f'{get_color(functii_pecheni_list[3])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'23%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Индекс GSG',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'77%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            

        ], style={'width':'38%','height':'480px'}),
        html.Div([
            html.Div([
                html.P('2. Обмен аминокислот – (',style={'margin':'0px'}),html.B(f'{obmen_aminokislot}%',style={'margin':'0px'}),html.P(')',style={'margin':'0px'}),
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_aminokislot)}','background-color':f'{get_color_under_normal_dist(obmen_aminokislot)}','border-radius':'2px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center','margin-left':'5px','margin-top':'6px'}),
                ],style={'width':'50px','height':'18px','line-height':'18px'}),  
            ], style={'color':'black','font-family':'Arial','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-top':'2px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_aminokislot_list[0])}','background-color':f'{get_color(obmen_aminokislot_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Метаболизм фенилаланина',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'79%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_aminokislot_list[1])}','background-color':f'{get_color(obmen_aminokislot_list[1])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Метаболизм аминокислот с разветвленной боковой цепью',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'79%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_aminokislot_list[2])}','background-color':f'{get_color(obmen_aminokislot_list[2])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Метаболизм триптофана',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'79%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_aminokislot_list[3])}','background-color':f'{get_color(obmen_aminokislot_list[3])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Метионин',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'79%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_aminokislot_list[4])}','background-color':f'{get_color(obmen_aminokislot_list[4])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Гистидин',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'79%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(obmen_aminokislot_list[5])}','background-color':f'{get_color(obmen_aminokislot_list[5])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Глутаминовая кислота и аспарагиновая кислота',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'79%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),



            html.Div([
                html.P('4. Стресс и нейромедиаторы – (',style={'margin':'0px'}),html.B(f'{stress_i_neyromoderatory}%',style={'margin':'0px'}),html.P(')',style={'margin':'0px'}),
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(stress_i_neyromoderatory)}','background-color':f'{get_color_under_normal_dist(stress_i_neyromoderatory)}','border-radius':'2px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center','margin-left':'5px','margin-top':'6px'}),
                ],style={'width':'50px','height':'18px','line-height':'18px'}),   
            ], style={'color':'black','font-family':'Arial','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-top':'8px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(stress_i_neyromoderatory_list[0])}','background-color':f'{get_color(stress_i_neyromoderatory_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Стероидные гормоны',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'79%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(stress_i_neyromoderatory_list[1])}','background-color':f'{get_color(stress_i_neyromoderatory_list[1])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Нейромедиаторы',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'79%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(stress_i_neyromoderatory_list[2])}','background-color':f'{get_color(stress_i_neyromoderatory_list[2])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Метаболизм фенилаланина',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'79%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(stress_i_neyromoderatory_list[3])}','background-color':f'{get_color(stress_i_neyromoderatory_list[3])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Синтез серотонина и мелатонина',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'79%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),



            html.Div([
                html.P('6. Маркеры микробиоты – (',style={'margin':'0px'}),html.B(f'{markery_mikrobioty}%',style={'margin':'0px'}),html.P(')',style={'margin':'0px'}),
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(markery_mikrobioty)}','background-color':f'{get_color_under_normal_dist(markery_mikrobioty)}','border-radius':'2px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center','margin-left':'5px','margin-top':'6px'}),
                ],style={'width':'50px','height':'18px','line-height':'18px'}),    
            ], style={'color':'black','font-family':'Arial','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-top':'26px'}),
            
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(markery_mikrobioty_list[0])}','background-color':f'{get_color(markery_mikrobioty_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('ТМАО (триметиламин-N-оксид)',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'79%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(markery_mikrobioty_list[1])}','background-color':f'{get_color(markery_mikrobioty_list[1])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Индольный путь метаболизма триптофана',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'79%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),



            html.Div([
                html.P('8. Функция сердца – (',style={'margin':'0px'}),html.B(f'{funcii_serdca}%',style={'margin':'0px'}),html.P(')',style={'margin':'0px'}),
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(funcii_serdca)}','background-color':f'{get_color_under_normal_dist(funcii_serdca)}','border-radius':'2px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center','margin-left':'5px','margin-top':'6px'}),
                ],style={'width':'50px','height':'18px','line-height':'18px'}),    
            ], style={'color':'black','font-family':'Arial','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-top':'26px'}),
            html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(funcii_serdca_list[0])}','background-color':f'{get_color(funcii_serdca_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Метаболизм аминокислот с разветвленной боковой цепью',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'79%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
                        html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(funcii_serdca_list[1])}','background-color':f'{get_color(funcii_serdca_list[1])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Окислительный стресс',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'79%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
                        html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(funcii_serdca_list[2])}','background-color':f'{get_color(funcii_serdca_list[2])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Функция эндотелия сосудов',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'79%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
                        html.Div([
                html.Div([
                    html.Div([],style={'width':f'{procent_validator(funcii_serdca_list[3])}','background-color':f'{get_color(funcii_serdca_list[3])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
                ],style={'width':'15%','height':'18px','line-height':'18px'}),
                html.Div([
                    html.P('Системные маркеры',style={'margin':'0px','font-size':'14px','font-family':'Arial','height':'18px','margin-left':'3px'})
                ],style={'width':'79%'}),
            ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
        ], style={'width':'57%','height':'480px',})
    ], style={'display':'flex', 'justify-content':'space-between','height':'480px','margin-top':'5px'}),
    html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
           style={'color':'black','font-family':'Arial','font-size':'14px','margin':'0px','text-align':"left",'font-style':'italic','margin-top':'5px'}),

    # 2 страница
    html.Div([
        html.Div([],style={'height':'8mm','width':'100%'}),
        html.Div([
            html.Div([
                html.B(f"Дата: {date}",style={'margin':'0px','font-size':'18px','font-family':'Arial'}),
                html.Div([
                    html.B(f'Пациент: {name}',style={'margin':'0px','font-size':'18px','font-family':'Arial'}),
                ],style={'margin-top':'10px'}),
            ], style={'width':'33.3%'}),
            html.Div([
                html.B("MetaboScan-Test01",style={'margin':'0px','font-size':'18px','font-family':'Arial'}),
            ], style={'width':'33.3%','text-align':'center'}),
            html.Div([
                html.Img(src=app.get_asset_url('logo.jpg'),style={'height':'54px','float':'right'}),
            ], style={'width':'33.3%'}),
        ], style={'display':'flex', 'justify-content':'space-between','width':'100%','height':'54px','color':'#0874bc'}),    
        html.Div([
        html.H3(children='1. Аминокислоты', style={'textAlign':'left','margin':'0px','line-height':'normal','display':'inline-block','vertical-align':'center'}),]
             , style={'width':'100%','background-color':'#0874bc', 'color':'white','font-family':'Arial','margin':'0px','height':'35px','line-height':'35px','text-align':'center','margin-top':'5px'}),
        html.Div([
            html.Div([
               html.Div([
                html.Div([html.B('Метаболизм фенилаланина',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'40px'}),
                html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'40px'}),
                html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'40px'}),
                html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'12px','font-family':'Arial','color':'black','text-align':'center'}),
            ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
            ], style={'margin':'0px','margin-left':'20px'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Фенилаланин (Phe)',style={'height':'20px'}),html.P('Незаменимая глюко-, кетогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_1[0],ref_1[0])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_1[0]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_1[0],ref_1[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_1[0],ref_1[0])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_1[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Тирозин (Tyr)',style={'height':'20px'}),html.P('Заменимая глюко-, кетогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_1[1],ref_1[1])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_1[1]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_1[1],ref_1[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_1[1],ref_1[1])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_1[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px',}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Индекс ААAs [Phe + Tyr]',style={'height':'20px'}),html.P('Запас ароматических аминокислот ',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_1[2],ref_1[2])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_1[2]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_1[2],ref_1[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_1[2],ref_1[2])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_1[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            
            html.Div([
               html.Div([
                html.Div([html.B('BCAA – аминокислоты с разветвленной цепью',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#4c86ae','line-height':'40px'}),
                html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'40px'}),
                html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'40px'}),
                html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center'}),
            ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
            ], style={'margin':'0px','margin-left':'20px'}),
            
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Лейцин + Изолейцин (Leu+Ile)',style={'height':'20px'}),html.P('Незаменимая глюко-, кетогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_2[0],ref_2[0])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_2[0]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_2[0],ref_2[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_2[0],ref_2[0])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_2[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Валин (Val)',style={'height':'20px'}),html.P('Незаменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_2[1],ref_2[1])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_2[1]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_2[1],ref_2[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_2[1],ref_2[1])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_2[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px',}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Индекс ВСААs [Leu + Ile + Val]',style={'height':'20px'}),html.P('Запас аминокислот с разветвленной боковой цепью',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_2[2],ref_2[2])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_2[2]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_2[2],ref_2[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_2[2],ref_2[0])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_2[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Индекс Фишера FR [BCAAs / AAAs]',style={'height':'20px'}),html.P('Отношение запаса аминокислот с разветвленной цепью к запасу ароматических аминокислот',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_2[3],ref_2[3])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_2[3]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_2[3],ref_2[3])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_2[3],ref_2[3])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_2[3]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px',}),
            
            html.Div([
               html.Div([
                html.Div([html.B('Метаболизм гистидина',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#4c86ae','line-height':'40px'}),
                html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'40px'}),
                html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'40px'}),
                html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center'}),
            ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
            ], style={'margin':'0px','margin-left':'20px'}),
            
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Гистидин (His)',style={'height':'20px'}),html.P('Незаменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_3[0],ref_3[0])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_3[0]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_3[0],ref_3[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_3[0],ref_3[0])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_3[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Метилгистидин (MH)',style={'height':'20px'}),html.P('Метаболит карнозина',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_3[1],ref_3[1])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_3[1]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_3[1],ref_3[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_3[1],ref_3[1])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_3[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px',}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Треонин (Thr)',style={'height':'20px'}),html.P('Незаменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_3[2],ref_3[2])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_3[2]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_3[2],ref_3[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_3[2],ref_3[2])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_3[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Карнозин (Car)',style={'height':'20px'}),html.P('Дипептид, состоящий из аланина и гистидина',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_3[3],ref_3[3])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_3[3]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_3[3],ref_3[3])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_3[3],ref_3[3])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_3[3]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px',}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Глицин (Gly)',style={'height':'20px'}),html.P('Заменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_3[4],ref_3[4])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_3[4]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_3[4],ref_3[4])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_3[4],ref_3[4])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_3[4]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Диметилглицин (DMG)',style={'height':'20px'}),html.P('Промежуточный продукт синтеза глицина',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_3[5],ref_3[5])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_3[5]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_3[5],ref_3[5])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_3[5],ref_3[5])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_3[5]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px',}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Серин (Ser)',style={'height':'20px'}),html.P('Заменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_3[6],ref_3[6])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_3[6]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_3[6],ref_3[6])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_3[6],ref_3[6])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_3[6]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Лизин (Lys)',style={'height':'20px'}),html.P('Незаменимая кетогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_3[7],ref_3[7])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_3[7]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_3[7],ref_3[7])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_3[7],ref_3[7])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_3[7]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px',}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Глутаминовая кислота (Glu)',style={'height':'20px'}),html.P('Заменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_3[8],ref_3[8])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_3[8]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_3[8],ref_3[8])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_3[8],ref_3[8])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_3[8]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
        ], style={'margin':'0px'}),
    ]),
    html.Div([
        html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
           style={'color':'black','font-family':'Arial','font-size':'14px','margin':'0px','text-align':"left",'font-style':'italic','margin-top':'5px','width':'85%'}),
        html.P('|1',
            style={'color':'black','font-family':'Arial','font-size':'14px','margin':'0px','text-align':"right",'font-style':'italic','margin-top':'5px','width':'10%','margin-top':'20px'}),
    ], style={'margin':'0px','display':'flex','justify-content':'space-between','width':'100%','margin-top':'55px'}),
    
    
    # 3 страница
    html.Div([
        html.Div([],style={'height':'8mm','width':'100%'}),
        html.Div([
            html.Div([
                html.B(f"Дата: {date}",style={'margin':'0px','font-size':'18px','font-family':'Arial'}),
                html.Div([
                    html.B(f'Пациент: {name}',style={'margin':'0px','font-size':'18px','font-family':'Arial'}),
                ],style={'margin-top':'10px'}),
            ], style={'width':'33.3%'}),
            html.Div([
                html.B("MetaboScan-Test01",style={'margin':'0px','font-size':'18px','font-family':'Arial'}),
            ], style={'width':'33.3%','text-align':'center'}),
            html.Div([
                html.Img(src=app.get_asset_url('logo.jpg'),style={'height':'53px','float':'right'}),
            ], style={'width':'33.3%'}),
        ], style={'display':'flex', 'justify-content':'space-between','width':'100%','height':'53px','color':'#0874bc'}),    
        
        html.Div([
            html.Div([
               html.Div([
                html.Div([html.B('Метаболизм гистидина',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#4c86ae','line-height':'40px'}),
                html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'40px'}),
                html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'40px'}),
                html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center'}),
            ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
            ], style={'margin':'0px','margin-left':'20px'}),
            
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Глутамин (Gln)',style={'height':'20px'}),html.P('Заменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_3[9],ref_3[9])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_3[9]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_3[9],ref_3[9])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_3[9],ref_3[9])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_3[9]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Индекс [Gln / Glu]',style={'height':'20px'}),html.P('Активность глутаминсинтетазы',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_3[10],ref_3[10])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_3[10]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_3[10],ref_3[10])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_3[10],ref_3[10])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_3[10]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px',}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Индекс GSG [Glu / (Ser + Gly)]',style={'height':'20px'}),html.P('Запас аминокислот для синтеза глутатиона',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_3[11],ref_3[11])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_3[11]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_3[11],ref_3[11])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_3[11],ref_3[11])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_3[11]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Индекс [Gly / Ser]',style={'height':'20px'}),html.P('Активность глутаминсинтетазы',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_3[10],ref_3[10])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_3[10]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_3[10],ref_3[10])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_3[10],ref_3[10])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_3[10]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px',}),
            
            html.Div([
               html.Div([
                html.Div([html.B('Метаболизм метионина',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#4c86ae','line-height':'40px'}),
                html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'40px'}),
                html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'40px'}),
                html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center'}),
            ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
            ], style={'margin':'0px','margin-left':'20px'}),
            
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Метионин (Met)',style={'height':'20px'}),html.P('Незаменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_4[0],ref_4[0])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_4[0]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_4[0],ref_4[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_4[0],ref_4[0])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_4[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Метионин сульфоксид (MetSO4)',style={'height':'20px'}),html.P('Продукт окисления метионина',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_4[1],ref_4[1])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_4[1]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_4[1],ref_4[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_4[1],ref_4[1])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_4[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px',}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Цистатионин (Cys)',style={'height':'20px'}),html.P('Серосодержащая аминокислота',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_4[2],ref_4[2])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_4[2]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_4[2],ref_4[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_4[2],ref_4[2])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_4[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Таурин (Tau)',style={'height':'20px'}),html.P('Заменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_4[3],ref_4[3])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_4[3]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_4[3],ref_4[3])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_4[3],ref_4[3])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_4[3]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px',}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Бетаин (Bet)',style={'height':'20px'}),html.P('Продукт метаболизма холина',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_4[4],ref_4[4])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_4[4]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_4[4],ref_4[4])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_4[4],ref_4[4])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_4[4]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Холин (Chl)',style={'height':'20px'}),html.P('Компонент мембран клеток, источник ацетилхолина',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_4[5],ref_4[5])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_4[5]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_4[5],ref_4[5])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_4[5],ref_4[5])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_4[5]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px',}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Триметиламин-N-оксид (TMAO)',style={'height':'20px'}),html.P('Продукт метаболизма холина, бетаина и др. бактериями ЖКТ',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_4[6],ref_4[6])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_4[6]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_4[6],ref_4[6])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_4[6],ref_4[6])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_4[6]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Индекс Chl / Bet',style={'height':'20px'}),html.P('Соотношение холина к бетаину',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_4[7],ref_4[7])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_4[7]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_4[7],ref_4[7])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_4[7],ref_4[7])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_4[7]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px'}),
            html.Div([
        html.H3(children='2. Метаболизм триптофана', style={'textAlign':'center','margin':'0px','line-height':'normal','display':'inline-block','vertical-align':'center'}),]
             , style={'width':'100%','background-color':'#0874bc', 'color':'white','font-family':'Arial','margin':'0px','height':'35px','line-height':'35px','text-align':'center','margin-top':'5px'}),
            html.Div([
               html.Div([
                html.Div([html.B('Кинурениновый путь',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#4c86ae','line-height':'40px'}),
                html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'40px'}),
                html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'40px'}),
                html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center'}),
            ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
            ], style={'margin':'0px','margin-left':'20px'}),
            
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Триптофан (Trp)',style={'height':'20px'}),html.P('Незаменимая глюко-, кетогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_5[0],ref_5[0])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_5[0]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_5[0],ref_5[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_5[0],ref_5[0])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_5[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Кинуренин (Kyn)',style={'height':'20px'}),html.P('Продукт метаболизма триптофана по кинурениновому пути',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_5[1],ref_5[1])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_5[1]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_5[1],ref_5[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_5[1],ref_5[1])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_5[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Индекс Kyn / Trp',style={'height':'20px'}),html.P('Показывает активность ферментов, метаболизирующих триптофан до кинуренина',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_5[2],ref_5[2])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_5[2]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_5[2],ref_5[5])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_5[2],ref_5[2])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_5[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Антраниловая кислота (Ant)',style={'height':'20px'}),html.P('Продукт метаболизма кинуренина',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_5[3],ref_5[3])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_5[3]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_5[3],ref_5[3])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_5[3],ref_5[3])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_5[3]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('3-Гидроксиантраниловая кислота',style={'height':'20px'}),html.P('Продукт метаболизма антраниловой кислоты',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_5[4],ref_5[4])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_5[4]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_5[4],ref_5[4])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_5[4],ref_5[4])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_5[4]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Хинолиновая кислота (Qnl)',style={'height':'20px'}),html.P('Продукт метаболизма 3-гидроксиантраниловой кислоты',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_5[5],ref_5[5])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_5[5]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_5[5],ref_5[5])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_5[5],ref_5[5])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_5[5]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px'}),
        ], style={'margin':'0px'}),
    ]),
    html.Div([
        html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
           style={'color':'black','font-family':'Arial','font-size':'14px','margin':'0px','text-align':"left",'font-style':'italic','margin-top':'5px','width':'85%'}),
        html.P('|2',
            style={'color':'black','font-family':'Arial','font-size':'14px','margin':'0px','text-align':"right",'font-style':'italic','margin-top':'5px','width':'10%','margin-top':'20px'}),
    ], style={'margin':'0px','display':'flex','justify-content':'space-between','width':'100%','margin-top':'5px'}),
    
    #4 страница
    html.Div([
        html.Div([],style={'height':'8mm','width':'100%'}),
        html.Div([
            html.Div([
                html.B(f"Дата: {date}",style={'margin':'0px','font-size':'18px','font-family':'Arial'}),
                html.Div([
                    html.B(f'Пациент: {name}',style={'margin':'0px','font-size':'18px','font-family':'Arial'}),
                ],style={'margin-top':'10px'}),
            ], style={'width':'33.3%'}),
            html.Div([
                html.B("MetaboScan-Test01",style={'margin':'0px','font-size':'18px','font-family':'Arial'}),
            ], style={'width':'33.3%','text-align':'center'}),
            html.Div([
                html.Img(src=app.get_asset_url('logo.jpg'),style={'height':'53px','float':'right'}),
            ], style={'width':'33.3%'}),
        ], style={'display':'flex', 'justify-content':'space-between','width':'100%','height':'53px','color':'#0874bc'}),    
        
        html.Div([
            html.Div([
               html.Div([
                html.Div([html.B('Кинурениновый путь',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#4c86ae','line-height':'40px'}),
                html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'40px'}),
                html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'40px'}),
                html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center'}),
            ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
            ], style={'margin':'0px','margin-left':'20px'}),
            
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Ксантуреновая кислота (Xnt)',style={'height':'20px'}),html.P('Продукт метаболизма кинуренина',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_5[6],ref_5[6])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_5[6]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_5[6],ref_5[6])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_5[6],ref_5[6])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_5[6]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Кинурениновая кислота (Kyna)',style={'height':'20px'}),html.P('Продукт метаболизма кинуренина',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_5[7],ref_5[7])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_5[7]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_5[7],ref_5[7])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_5[7],ref_5[7])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_5[7]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px',}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Индекс Kyn / Qnl',style={'height':'20px'}),html.P('Соотношение кинуренина к хинолиновой кислоте',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_5[8],ref_5[8])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_5[8]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_5[8],ref_5[8])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_5[8],ref_5[8])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_5[8]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            
            html.Div([
               html.Div([
                html.Div([html.B('Серотониновый путь',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#4c86ae','line-height':'40px'}),
                html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'40px'}),
                html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'40px'}),
                html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center'}),
            ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
            ], style={'margin':'0px','margin-left':'20px'}),
            
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Серотонин',style={'height':'20px'}),html.P('Нейромедиатор',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_6[0],ref_6[0])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_6[0]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_6[0],ref_6[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_6[0],ref_6[0])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_6[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('5-Гидроксииндолуксусная кислота (5-HIAA)',style={'height':'20px'}),html.P('Метаболит серотонина',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_6[1],ref_6[1])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_6[1]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_6[1],ref_6[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_6[1],ref_6[1])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_6[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px',}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Индекс Qnl / 5-HIAA',style={'height':'20px'}),html.P('Соотношение 5-гидроксииндолуксусной кислоты к хинолиновой кислота',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_6[2],ref_6[2])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_6[2]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_6[2],ref_6[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_6[2],ref_6[2])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_6[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('5-Гидрокситриптофан (5-HTP)',style={'height':'20px'}),html.P('Прекурсор серотонина',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_6[3],ref_6[3])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_6[3]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_6[3],ref_6[3])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_6[3],ref_6[3])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_6[3]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px',}),
            
            html.Div([
               html.Div([
                html.Div([html.B('Индоловый путь',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#4c86ae','line-height':'40px'}),
                html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'40px'}),
                html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'40px'}),
                html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center'}),
            ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
            ], style={'margin':'0px','margin-left':'20px'}),
            
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('3-Индолуксусная кислота (I3A)',style={'height':'20px'}),html.P('Продукт катаболизма триптофана кишечной микробиотой',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_7[0],ref_7[0])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_7[0]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_7[0],ref_7[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_7[0],ref_7[0])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_7[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('3-Индолмолочная кислота (I3L)',style={'height':'20px'}),html.P('Продукт катаболизма триптофана кишечной микробиотой',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_7[1],ref_7[1])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_7[1]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_7[1],ref_7[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_7[1],ref_7[1])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_7[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('3-Индолкарбоксальдегид (I3Al)',style={'height':'20px'}),html.P('Продукт катаболизма триптофана кишечной микробиотой',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_7[2],ref_7[2])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_7[2]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_7[2],ref_7[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_7[2],ref_7[2])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_7[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('3-Индолпропионовая кислота (I3P)',style={'height':'20px'}),html.P('Продукт катаболизма триптофана кишечной микробиотой',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_7[3],ref_7[3])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_7[3]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_7[3],ref_7[3])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_7[3],ref_7[3])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_7[3]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('3-Индолмасляная кислота (I3B)',style={'height':'20px'}),html.P('Продукт катаболизма триптофана кишечной микробиотой',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_7[4],ref_7[4])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_7[4]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_7[4],ref_7[4])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_7[4],ref_7[4])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_7[4]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Триптамин',style={'height':'20px'}),html.P('Продукт катаболизма триптофана кишечной микробиотой, прекурсор для нейромедиаторов',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_7[5],ref_7[5])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_7[5]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_7[5],ref_7[5])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_7[5],ref_7[5])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_7[5]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('5-Метокситриптамин',style={'height':'20px'}),html.P('Производное триптамина',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_7[6],ref_7[6])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_7[6]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_7[6],ref_7[6])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_7[6],ref_7[6])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_7[6]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
        html.H3(children='3. Метаболизм аргинина', style={'textAlign':'center','margin':'0px','line-height':'normal','display':'inline-block','vertical-align':'center'}),]
             , style={'width':'100%','background-color':'#0874bc', 'color':'white','font-family':'Arial','margin':'0px','height':'35px','line-height':'35px','text-align':'center','margin-top':'5px'}),
            html.Div([
               html.Div([
                html.Div([html.B('Метаболизм аргинина',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#4c86ae','line-height':'40px'}),
                html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'40px'}),
                html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'40px'}),
                html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center'}),
            ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
            ], style={'margin':'0px','margin-left':'20px'}),
            
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Пролин (Pro)',style={'height':'20px'}),html.P('Заменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_8[0],ref_8[0])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_8[0]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_8[0],ref_8[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_8[0],ref_8[0])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_8[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Гидроксипролин (Hyp)',style={'height':'20px'}),html.P('Источник коллагена',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_8[1],ref_8[1])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_8[1]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_8[1],ref_8[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_8[1],ref_8[1])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_8[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px'}),
            
        ], style={'margin':'0px'}),
    ]),
    html.Div([
        html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
           style={'color':'black','font-family':'Arial','font-size':'14px','margin':'0px','text-align':"left",'font-style':'italic','margin-top':'5px','width':'85%'}),
        html.P('|3',
            style={'color':'black','font-family':'Arial','font-size':'14px','margin':'0px','text-align':"right",'font-style':'italic','margin-top':'5px','width':'10%','margin-top':'20px'}),
    ], style={'margin':'0px','display':'flex','justify-content':'space-between','width':'100%','margin-top':'15px'}),
    
    # 5 страница
    html.Div([
        html.Div([],style={'height':'8mm','width':'100%'}),
        html.Div([
            html.Div([
                html.B(f"Дата: {date}",style={'margin':'0px','font-size':'18px','font-family':'Arial'}),
                html.Div([
                    html.B(f'Пациент: {name}',style={'margin':'0px','font-size':'18px','font-family':'Arial'}),
                ],style={'margin-top':'10px'}),
            ], style={'width':'33.3%'}),
            html.Div([
                html.B("MetaboScan-Test01",style={'margin':'0px','font-size':'18px','font-family':'Arial'}),
            ], style={'width':'33.3%','text-align':'center'}),
            html.Div([
                html.Img(src=app.get_asset_url('logo.jpg'),style={'height':'53px','float':'right'}),
            ], style={'width':'33.3%'}),
        ], style={'display':'flex', 'justify-content':'space-between','width':'100%','height':'53px','color':'#0874bc'}),    
        
        html.Div([
            html.Div([
               html.Div([
                html.Div([html.B('Метаболизм аргинина',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#4c86ae','line-height':'40px'}),
                html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'40px'}),
                html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'40px'}),
                html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center'}),
            ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
            ], style={'margin':'0px','margin-left':'20px'}),
            
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Асимметричный диметиларгинин (ADMA)',style={'height':'20px'}),html.P('Эндогенный ингибитор синтазы оксида азота',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_8[2],ref_8[2])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_8[2]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_8[2],ref_8[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_8[2],ref_8[2])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_8[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Симметричный диметиларгинин (SDMA)',style={'height':'20px'}),html.P('Продукт метаболизма аргинина, выводится с почками',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_8[3],ref_8[3])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_8[3]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_8[3],ref_8[3])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_8[3],ref_8[3])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_8[3]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px',}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Гомоаргинин',style={'height':'20px'}),html.P('Субстрат для синтазы оксида азота',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_8[4],ref_8[4])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_8[4]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_8[4],ref_8[4])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_8[4],ref_8[4])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_8[4]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Аргинин',style={'height':'20px'}),html.P('Незаменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_8[5],ref_8[5])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_8[5]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_8[5],ref_8[5])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_8[5],ref_8[5])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_8[5]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Цитруллин (Cit)',style={'height':'20px'}),html.P('Метаболит цикла мочевины',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_8[6],ref_8[6])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_8[6]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_8[6],ref_8[6])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_8[6],ref_8[6])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_8[6]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Орнитин (Orn)',style={'height':'20px'}),html.P('Метаболит цикла мочевины',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_8[7],ref_8[7])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_8[7]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_8[7],ref_8[7])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_8[7],ref_8[7])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_8[7]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Аспарагин (Asn)',style={'height':'20px'}),html.P('Заменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_8[8],ref_8[8])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_8[8]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_8[8],ref_8[8])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_8[8],ref_8[8])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_8[8]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Аспарагиновая кислота (Asp)',style={'height':'20px'}),html.P('Заменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_8[9],ref_8[9])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_8[9]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_8[9],ref_8[9])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_8[9],ref_8[9])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_8[9]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Индекс GABR [Arg / (Orn + Cit)]',style={'height':'20px'}),html.P('Общая биодоступность аргинина',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_8[10],ref_8[10])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_8[10]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_8[10],ref_8[10])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_8[10],ref_8[10])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_8[10]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Индекс AOR [Arg / Orn]',style={'height':'20px'}),html.P('Показывает активность аргиназы',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_8[11],ref_8[11])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_8[11]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_8[11],ref_8[11])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_8[11],ref_8[11])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_8[11]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Индекс Asn / Asp',style={'height':'20px'}),html.P('Показывает активность аспарагинсинтетазы',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_8[12],ref_8[12])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_8[12]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_8[12],ref_8[12])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_8[12],ref_8[12])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_8[12]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Креатинин',style={'height':'20px'}),html.P('Продукт метаболизма аргинина',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_8[13],ref_8[13])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_8[13]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_8[13],ref_8[13])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_8[13],ref_8[13])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_8[13]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px'}),
            html.Div([
        html.H3(children='4. Метаболизм жирных кислот', style={'textAlign':'center','margin':'0px','line-height':'normal','display':'inline-block','vertical-align':'center'}),]
             , style={'width':'100%','background-color':'#0874bc', 'color':'white','font-family':'Arial','margin':'0px','height':'35px','line-height':'35px','text-align':'center','margin-top':'5px'}),
            html.Div([
               html.Div([
                html.Div([html.B('Метаболизм ацилкарнитинов',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#4c86ae','line-height':'40px'}),
                html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'40px'}),
                html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'40px'}),
                html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center'}),
            ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
            ], style={'margin':'0px','margin-left':'20px'}),
            
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Аланин',style={'height':'20px'}),html.P('Заменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_9[0],ref_9[0])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_9[0]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_9[0],ref_9[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_9[0],ref_9[0])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_9[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Карнитин (C0)',style={'height':'20px'}),html.P('Основа для ацилкарнитинов, транспорт жирных кислот',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_9[1],ref_9[1])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_9[1]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_9[1],ref_9[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_9[1],ref_9[1])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_9[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Ацетилкарнитин (C2)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_9[2],ref_9[2])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_9[2]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_9[2],ref_9[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_9[2],ref_9[2])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_9[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            
            html.Div([
               html.Div([
                html.Div([html.B('Короткоцепочечные ацилкарнитины',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#4c86ae','line-height':'40px'}),
                html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'40px'}),
                html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'40px'}),
                html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center'}),
            ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
            ], style={'margin':'0px','margin-left':'20px'}),
            
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Пропионилкарнитин (С3)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_10[0],ref_10[0])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_10[0]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_10[0],ref_10[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_10[0],ref_10[0])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_10[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Бутирилкарнитин (C4)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_10[1],ref_10[1])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_10[1]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_10[1],ref_10[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_10[1],ref_10[1])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_10[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px'}),
        ], style={'margin':'0px'}),
    ]),
    html.Div([
        html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
           style={'color':'black','font-family':'Arial','font-size':'14px','margin':'0px','text-align':"left",'font-style':'italic','margin-top':'5px','width':'85%'}),
        html.P('|4',
            style={'color':'black','font-family':'Arial','font-size':'14px','margin':'0px','text-align':"right",'font-style':'italic','margin-top':'5px','width':'10%','margin-top':'20px'}),
    ], style={'margin':'0px','display':'flex','justify-content':'space-between','width':'100%','margin-top':'5px'}),
    
    # 6 страница
    html.Div([
        html.Div([],style={'height':'8mm','width':'100%'}),
        html.Div([
            html.Div([
                html.B(f"Дата: {date}",style={'margin':'0px','font-size':'18px','font-family':'Arial'}),
                html.Div([
                    html.B(f'Пациент: {name}',style={'margin':'0px','font-size':'18px','font-family':'Arial'}),
                ],style={'margin-top':'10px'}),
            ], style={'width':'33.3%'}),
            html.Div([
                html.B("MetaboScan-Test01",style={'margin':'0px','font-size':'18px','font-family':'Arial'}),
            ], style={'width':'33.3%','text-align':'center'}),
            html.Div([
                html.Img(src=app.get_asset_url('logo.jpg'),style={'height':'54px','float':'right'}),
            ], style={'width':'33.3%'}),
        ], style={'display':'flex', 'justify-content':'space-between','width':'100%','height':'54px','color':'#0874bc'}),    
        html.Div([
            html.Div([
               html.Div([
                html.Div([html.B('Короткоцепочечные ацилкарнитины',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#4c86ae','line-height':'40px'}),
                html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'40px'}),
                html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'40px'}),
                html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center'}),
            ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
            ], style={'margin':'0px','margin-left':'20px'}),
            
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Изовалерилкарнитин (С5)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_10[2],ref_10[2])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_10[2]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_10[2],ref_10[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_10[2],ref_10[2])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_10[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Тиглилкарнитин (C5-1)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_10[3],ref_10[3])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_10[3]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_10[3],ref_10[3])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_10[3],ref_10[3])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_10[3]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px',}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Глутарилкарнитин (C5-DC)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_10[4],ref_10[4])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_10[4]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_10[4],ref_10[4])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_10[4],ref_10[4])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_10[4]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Гидроксиизовалерилкарнитин (C5-OH)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_10[5],ref_10[5])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_10[5]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_10[5],ref_10[5])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_10[5],ref_10[5])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_10[5]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px'}),
            
            html.Div([
               html.Div([
                html.Div([html.B('Среднецепочечные ацилкарнитины',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#4c86ae','line-height':'40px'}),
                html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'40px'}),
                html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'40px'}),
                html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center'}),
            ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
            ], style={'margin':'0px','margin-left':'20px'}),
            
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Гексаноилкарнитин (C6)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_11[0],ref_11[0])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_11[0]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_11[0],ref_11[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_11[0],ref_11[0])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_11[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Адипоилкарнитин (C6-DC)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_11[1],ref_11[1])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_11[1]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_11[1],ref_11[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_11[1],ref_11[1])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_11[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px',}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Октаноилкарнитин (C8)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_11[2],ref_11[2])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_11[2]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_11[2],ref_11[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_11[2],ref_11[2])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_11[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Октеноилкарнитин (C8-1)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_11[3],ref_11[3])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_11[3]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_11[3],ref_11[3])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_11[3],ref_11[3])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_11[3]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px',}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Деканоилкарнитин (C10)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_11[4],ref_11[4])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_11[4]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_11[4],ref_11[4])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_11[4],ref_11[4])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_11[4]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Деценоилкарнитин (C10-1)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_11[5],ref_11[5])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_11[5]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_11[5],ref_11[5])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_11[5],ref_11[5])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_11[5]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px',}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Декадиеноилкарнитин (C10-2)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_11[6],ref_11[6])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_11[6]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_11[6],ref_11[6])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_11[6],ref_11[6])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_11[6]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Додеканоилкарнитин (C12)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_11[7],ref_11[7])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_11[7]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_11[7],ref_11[7])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_11[7],ref_11[7])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_11[7]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px',}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Додеценоилкарнитин (C12-1)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_11[8],ref_11[8])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_11[8]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_11[8],ref_11[8])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_11[8],ref_11[8])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_11[8]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            
            html.Div([
               html.Div([
                html.Div([html.B('Длинноцепочечные ацилкарнитины',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#4c86ae','line-height':'40px'}),
                html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'40px'}),
                html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'40px'}),
                html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center'}),
            ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
            ], style={'margin':'0px','margin-left':'20px'}),
            
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Тетрадеканоилкарнитин (C14)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_12[0],ref_12[0])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_12[0]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_12[0],ref_12[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_12[0],ref_12[0])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_12[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Тетрадеценоилкарнитин (С14-1)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_12[1],ref_12[1])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_12[1]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_12[1],ref_12[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_12[1],ref_12[1])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_12[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Тетрадекадиеноилкарнитин (C14-2)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_12[2],ref_12[2])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_12[2]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_12[2],ref_12[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_12[2],ref_12[2])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_12[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Гидрокситетрадеканоилкарнитин (C14-OH)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_12[3],ref_12[3])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_12[3]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_12[3],ref_12[3])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_12[3],ref_12[3])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_12[3]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Пальмитоилкарнитин (C16)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_12[4],ref_12[4])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_12[4]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_12[4],ref_12[4])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_12[4],ref_12[4])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_12[4]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
        ], style={'margin':'0px'}),
    ]),
    html.Div([
        html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
           style={'color':'black','font-family':'Arial','font-size':'14px','margin':'0px','text-align':"left",'font-style':'italic','margin-top':'5px','width':'85%'}),
        html.P('|5',
            style={'color':'black','font-family':'Arial','font-size':'14px','margin':'0px','text-align':"right",'font-style':'italic','margin-top':'5px','width':'10%','margin-top':'20px'}),
    ], style={'margin':'0px','display':'flex','justify-content':'space-between','width':'100%','margin-top':'0px'}),
    
    #7 страница
    html.Div([
        html.Div([],style={'height':'8mm','width':'100%'}),
        html.Div([
            html.Div([
                html.B(f"Дата: {date}",style={'margin':'0px','font-size':'18px','font-family':'Arial'}),
                html.Div([
                    html.B(f'Пациент: {name}',style={'margin':'0px','font-size':'18px','font-family':'Arial'}),
                ],style={'margin-top':'10px'}),
            ], style={'width':'33.3%'}),
            html.Div([
                html.B("MetaboScan-Test01",style={'margin':'0px','font-size':'18px','font-family':'Arial'}),
            ], style={'width':'33.3%','text-align':'center'}),
            html.Div([
                html.Img(src=app.get_asset_url('logo.jpg'),style={'height':'53px','float':'right'}),
            ], style={'width':'33.3%'}),
        ], style={'display':'flex', 'justify-content':'space-between','width':'100%','height':'53px','color':'#0874bc'}),    
        
        html.Div([
            html.Div([
               html.Div([
                html.Div([html.B('Длинноцепочечные ацилкарнитины',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#4c86ae','line-height':'40px'}),
                html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'40px'}),
                html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'40px'}),
                html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center'}),
            ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
            ], style={'margin':'0px','margin-left':'20px'}),
            
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Гексадецениолкарнитин (C16-1)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_12[5],ref_12[5])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_12[5]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_12[5],ref_12[5])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_12[5],ref_12[5])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_12[5]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Гидроксигексадецениолкарнитин (C16-1-OH)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_12[6],ref_12[6])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_12[6]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_12[6],ref_12[6])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_12[6],ref_12[6])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_12[6]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px',}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Гидроксигексадеканоилкарнитин (C16-OH)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_12[7],ref_12[7])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_12[7]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_12[7],ref_12[7])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_12[7],ref_12[7])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_12[7]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Стеароилкарнитин (С18)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_12[8],ref_12[8])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_12[8]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_12[8],ref_12[8])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_12[8],ref_12[8])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_12[8]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Олеоилкарнитин (C18-1)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_12[9],ref_12[9])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_12[9]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_12[9],ref_12[9])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_12[9],ref_12[9])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_12[9]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Гидроксиоктадеценоилкарнитин (C18-1-OH)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_12[10],ref_12[10])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_12[10]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_12[10],ref_12[10])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_12[10],ref_12[10])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_12[10]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Линолеоилкарнитин (C18-2)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_12[11],ref_12[11])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_12[11]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_12[11],ref_12[11])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_12[11],ref_12[11])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_12[11]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Гидроксиоктадеканоилкарнитин (C18-OH)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_12[12],ref_12[12])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_12[12]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_12[12],ref_12[12])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_12[12],ref_12[12])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_12[12]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px'}),
            html.Div([
                html.H3(children='4. Метаболизм жирных кислот', style={'textAlign':'center','margin':'0px','line-height':'normal','display':'inline-block','vertical-align':'center'}),]
             , style={'width':'100%','background-color':'#0874bc', 'color':'white','font-family':'Arial','margin':'0px','height':'35px','line-height':'35px','text-align':'center','margin-top':'5px'}),
            html.Div([
               html.Div([
                html.Div([html.B('Витамины и нейромедиаторы',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#4c86ae','line-height':'40px'}),
                html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'40px'}),
                html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'40px'}),
                html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center'}),
            ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
            ], style={'margin':'0px','margin-left':'20px'}),
            
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Пантотеновая кислота',style={'height':'20px'}),html.P('Витамин B5',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_13[0],ref_13[0])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_13[0]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_13[0],ref_13[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_13[0],ref_13[0])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_13[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Рибофлавин',style={'height':'20px'}),html.P('Витамин B2',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_13[1],ref_13[1])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_13[1]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_13[1],ref_13[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_13[1],ref_13[1])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_13[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Биотин',style={'height':'20px'}),html.P('Витамин H (B7)',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_13[2],ref_13[2])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_13[2]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_13[2],ref_13[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_13[2],ref_13[2])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_13[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Мелатонин',style={'height':'20px'}),html.P('Регулирует циркадные ритмы',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_13[3],ref_13[3])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_13[3]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_13[3],ref_13[3])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_13[3],ref_13[3])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_13[3]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px'}),
            
            html.Div([
               html.Div([
                html.Div([html.B('Нуклеозиды',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#4c86ae','line-height':'40px'}),
                html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'40px'}),
                html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'40px'}),
                html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center'}),
            ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
            ], style={'margin':'0px','margin-left':'20px'}),
            
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Уридин',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_14[0],ref_14[0])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_14[0]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_14[0],ref_14[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_14[0],ref_14[0])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_14[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#FFFFFF'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Инозин',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_14[1],ref_14[1])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_14[1]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_14[1],ref_14[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_14[1],ref_14[1])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_14[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px'}),
            
            html.Div([
               html.Div([
                html.Div([html.B('Аллергия и стресс',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#4c86ae','line-height':'40px'}),
                html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'40px'}),
                html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'40px'}),
                html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center'}),
            ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
            ], style={'margin':'0px','margin-left':'20px'}),
            
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Кортизол',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_15[0],ref_15[0])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_15[0]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_15[0],ref_15[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_15[0],ref_15[0])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_15[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px','background-color':'#000000'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.B('Гистамин',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Arial','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','margin-top':'5px'}),
                        html.Div([html.Div([html.Div([html.B(f'{need_of_plus(value_15[1],ref_15[1])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_15[1]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_15[1],ref_15[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':f'{color_text_ref(value_15[1],ref_15[1])}','line-height':'53px'}),
                        html.Div([html.Img(src=app.get_asset_url('123'),style={'width':'100%','height':'55px','line-height':'normal','display':'inline-block','vertical-align':'center','border':'1px solid black'}),],style={'width':'27%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'#0874bc','line-height':'53px'}),
                        html.Div([html.P(f'{ref_15[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Arial','color':'black','text-align':'center','line-height':'53px'}),
                    ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                ], style={'margin':'0px','margin-left':'20px'}),
            ],style={'margin':'0px'}),
        ], style={'margin':'0px'}),
    ]),
    html.Div([
        html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
           style={'color':'black','font-family':'Arial','font-size':'14px','margin':'0px','text-align':"left",'font-style':'italic','margin-top':'5px','width':'85%'}),
        html.P('|6',
            style={'color':'black','font-family':'Arial','font-size':'14px','margin':'0px','text-align':"right",'font-style':'italic','margin-top':'5px','width':'10%','margin-top':'20px'}),
    ], style={'margin':'0px','display':'flex','justify-content':'space-between','width':'100%','margin-top':'10px'}),

    ],style={'margin-right':'5mm','width':'800px'}) 

if __name__ == '__main__':
    # Enable debug mode and automatic reloader
    app.run_server(
        debug=True,
        dev_tools_hot_reload=True,
        dev_tools_hot_reload_interval=1000,
        dev_tools_hot_reload_watch_interval=1000,
        dev_tools_hot_reload_max_retry=30
    )

