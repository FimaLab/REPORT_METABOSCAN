import base64
from io import BytesIO
import json
from dash import Dash, html
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import os
import pandas as pd
import dash_core_components as dcc

app_pid = os.getpid()


procent_speed = 50
N = 1000
a = 3.5

def create_ref_stats_from_excel(excel_path):
    # Read the Excel file with explicit encoding support
    df = pd.read_excel(excel_path, engine='openpyxl')
    
    # Initialize the dictionary
    ref_stats = {}
    
    # Get all metabolite columns (skip the first column which is 'metabolite')
    metabolites = df.columns[1:]
    
    # Create a mapping of metric names to their row indices
    metric_map = {metric.lower(): idx for idx, metric in enumerate(df['metabolite'])}
    
    for metabolite in metabolites:
        try:
            # Get the Russian name if available (case-insensitive check)
            name_view_idx = metric_map.get('name_view')
            name = str(df[metabolite].iloc[name_view_idx]) if name_view_idx is not None else str(metabolite)
            
            # Ensure proper encoding of Cyrillic characters
            try:
                name = name.encode('latin1').decode('utf-8') if not name.isascii() else name
            except:
                pass
            
            # Get mean and sd
            mean = float(str(df[metabolite].iloc[metric_map['mean']]).replace(',', '.'))
            sd = float(str(df[metabolite].iloc[metric_map['sd']]).replace(',', '.'))
            
            # Get reference ranges with comma-to-dot conversion
            ref_min = float(str(df[metabolite].iloc[metric_map['ref_min']]).replace(',', '.')) if 'ref_min' in metric_map else None
            ref_max = float(str(df[metabolite].iloc[metric_map['ref_max']]).replace(',', '.')) if 'ref_max' in metric_map else None
            
            # Create norm string
            norm = None
            if ref_min is not None and ref_max is not None:
                if ref_min == 0:
                    norm = f"< {ref_max}"
                else:
                    norm = f"{ref_min} - {ref_max}"
            
            # Create the metabolite entry
            metabolite_data = {
                "mean": mean,
                "sd": sd,
                "norm": norm
            }
            
            # Add optional fields
            if ref_min is not None:
                metabolite_data["ref_min"] = ref_min
            if ref_max is not None:
                metabolite_data["ref_max"] = ref_max
            
            # Add smart_round if available
            if 'smart_round' in metric_map:
                smart_round = int(df[metabolite].iloc[metric_map['smart_round']])
                metabolite_data["smart_round"] = smart_round
            
            # Add to dictionary with proper Unicode handling
            ref_stats[name] = metabolite_data
            
        except Exception as e:
            print(f"Error processing metabolite {metabolite}: {str(e)}")
            continue
    return ref_stats

ref_stats = create_ref_stats_from_excel("Ref.xlsx")

def plot_metabolite_z_scores(metabolite_concentrations, group_title, norm_ref = [-1, 1]):
    # Set font to Calibri
    mpl.rcParams['font.family'] = 'Calibri'
    
    # Calculate z-scores and determine colors
    data = []
    highlight_green_metabolites = []
    for name, conc in metabolite_concentrations.items():
        
        # Calculate z-score (deviation from mean in SD units)
        z_score = round((conc - ref_stats[name]["mean"]) / ref_stats[name]["sd"], 2)
        
        
        if "<" in ref_stats[name]["norm"] and z_score <= 0:
            z_score = 0
            highlight_green_metabolites.append(name)
        
        # Determine color based on z-score
        if abs(z_score) > 1.2:  # Significant deviation
            color = "#dc2626"  # red
        elif abs(z_score) > 1:   # Moderate deviation
            color = "#feb61d"  # orange
        else:                   # Normal range
            color = "#10b981"  # green
        
        data.append({
            "name": name,
            "value": z_score,
            "color": color,
            "original_value": conc
        })

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)

    # Create bars
    bars = ax.bar([d["name"] for d in data], 
                 [d["value"] for d in data], 
                 color=[d["color"] for d in data], 
                 edgecolor='white', 
                 linewidth=1)
    
    
    xticklabels = ax.get_xticklabels()
    

            
    # Add value labels on top of bars
    for bar, item in zip(bars, data):
        height = item["value"]
        va = 'bottom' if height >= 0 else 'top'
        y = height + 0.05 if height >= 0 else height - 0.05
        
        # Determine text color - green if in highlight list, otherwise black
        text_color = '#10b981' if item["name"] in highlight_green_metabolites else 'black'
        
        # Adjust fontsize based on number of labels
        fontsize = 11 if len(xticklabels) > 15 else 14
        
        ax.text(bar.get_x() + bar.get_width()/2., y,
            f'{height:.2f}',
            ha='center', va=va, 
            fontsize=fontsize, 
            fontweight='bold',
            color=text_color)  # Set the text color here

    

    # Add horizontal lines
    ax.axhline(0, color='#374151', linewidth=1)
    ax.axhline(norm_ref[1], color='#6B7280', linestyle='--', linewidth=1)
    ax.axhline(norm_ref[0], color='#6B7280', linestyle='--', linewidth=1)

    # Add additional reference lines at ±1.2
    ax.axhline(1.2, color='#6B7280', linestyle=':', linewidth=1, alpha=0.5)
    ax.axhline(-1.2, color='#6B7280', linestyle=':', linewidth=1, alpha=0.5)

    # Set title and labels
    ax.set_title(group_title, fontsize=22, pad=20, color='#404547', fontweight='bold')
    ax.set_ylabel(f"Отклонение от состояния ЗДОРОВЫЙ, норма от {norm_ref[0]} до {norm_ref[1]}", 
                 fontsize=14, labelpad=15)
                 
    # Set y-axis scale with 0.5 steps
    y_min = round(min(-1.5, min([d["value"] for d in data])) - 0.2, 1)
    y_max = round(max(1.5, max([d["value"] for d in data])) + 0.2, 1)
    ax.set_ylim(y_min, y_max)
    # Determine the step size based on y_min and y_max
    y_range = max(abs(y_min), abs(y_max))
    if y_range > 15:
        step= 3.0
    elif y_range > 10:
        step = 1.5
    elif y_range > 7:
        step = 1.0
    elif y_range > 5:
        step = 0.75
    else:
        step = 0.5

    # Generate the ticks
    ax.set_yticks(np.arange(np.floor(y_min), np.ceil(y_max) + step, step))

    # Customize axes
    for spine in ['top', 'right', 'bottom', 'left']:
        ax.spines[spine].set_visible(False)
    
    ax.xaxis.set_tick_params(length=0)
    ax.yaxis.set_tick_params(length=0)
    plt.yticks(fontsize=13)

    # Get the x-axis tick labels
    xticklabels = ax.get_xticklabels()
    
    def get_fontsize(label):
        if len(label) > 20:
            return 13.5
        elif len(label) > 12:
            return 15
        else:
            return 15.5
    
    font_sizes= [get_fontsize(label.get_text()) for label in xticklabels]
    
    for i, label in enumerate(xticklabels):
        label.set_fontsize(font_sizes[i])
        label.set_rotation(45)
        label.set_ha('right')
    # Adjust layout
    plt.tight_layout()
    
    def fig_to_uri(fig):
        buf = BytesIO()
        fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
        buf.seek(0)
        img = base64.b64encode(buf.getvalue()).decode("ascii")
        
        return f"data:image/png;base64,{img}"
    
    plt.close()
    return fig_to_uri(fig)

def safe_parse_metabolite_data(file_path):
    """Your existing parse_metabolite_data function with added safety checks"""
    if not os.path.exists(file_path):
        print(f"Error: File not found - {file_path}")
        return {}
    
    try:
        # here excel file is first column name of sample and next columns are metabolites with conc below
        df = pd.read_excel(file_path, header=None)
        metabolite_headers = df.iloc[0]
        metabolite_data = {}
        
        for col_idx in range(1, len(metabolite_headers)):
            metabolite_name = str(metabolite_headers[col_idx]).replace(' Results', '').strip()
            if pd.isna(metabolite_name):
                continue
            
            conc_value = df.iloc[1, col_idx]
            try:
                if isinstance(conc_value, str):
                    conc_value = float(conc_value.replace(',', '.'))
                elif pd.isna(conc_value):
                    conc_value = 0.0
                metabolite_data[metabolite_name] = conc_value
            except:
                metabolite_data[metabolite_name] = 0.0
        
        return metabolite_data
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")
        return {}
    
def get_status_color(value, norm_str):
    try:
        norm_min = 0
        norm_max = 0
        if norm_str.__contains__(' - '):
            norm_min, norm_max = map(float, norm_str.split(' - '))
        elif norm_str.startswith('< '):
            norm_max = float(norm_str.split('< ')[1])
            norm_min = 0
        
        if value < norm_min:
            return "blue"  # Below normal range
        elif value > norm_max:
            return "red"   # Above normal range
        else:
            return "green" # Within normal range
            
    except (ValueError, AttributeError):
        # Handle cases where norm_str is not in expected format
        return "gray"  # Default color for invalid format

def get_status_text(value, norm_str):
    try:
        norm_min = 0
        norm_max = 0
        if norm_str.__contains__(' - '):
            norm_min, norm_max = map(float, norm_str.split(' - '))
        elif norm_str.startswith('< '):
            norm_max = float(norm_str.split('< ')[1])
            norm_min = 0
        
        if value < norm_min:
            return "Снижен"  # Below normal range
        elif value > norm_max:
            return "Повышен" # Above normal range
        else:
            return "Норма"   # Within normal range
            
    except (ValueError, AttributeError):
        # Handle cases where norm_str is not in expected format
        return "Не определено"  # Default text for invalid format
    
def smart_round(value, decimals=3):
    """
    Округляет число с сохранением первой ненулевой цифры после запятой,
    если округление приводит к нулю.
    
    :param value: исходное значение (число или строка)
    :param decimals: количество знаков после запятой для округления
    :return: округлённое значение с учётом значащих цифр
    """
    try:
        num = float(value)
    except (ValueError, TypeError):
        return 0.0
    
    if num == 0:
        return 0.0
    
    rounded = round(num, decimals)
    
    # Если округлённое значение не ноль, возвращаем его
    if rounded != 0:
        return rounded
    
    # Если округлили до нуля, находим первую ненулевую цифру после запятой
    abs_num = abs(num)
    precision = decimals
    while round(abs_num, precision) == 0:
        precision += 1
    
    return round(num, precision)

def get_color_age(n):
    if n <= 10:
        return "#50c15085"  # Light green (similar to 9-10)
    elif n <= 20:
        return "#96c93881"   # Light yellow (similar to 7-8)
    elif n<= 30:
        return "#b2d04785"  # Light orange (similar to 5-6)
    elif n <= 40:
        return "#cfdc4081"  # Light orange (similar to 5-6)
    elif n <= 50:
        return "#cfdc407c"  # Light orange (similar to 5-6)
    elif n <=60:
        return "#fef31d80"  # Light orange (similar to 5-6)
    elif n <= 70:
        return "#f290087c"  # Light orange (similar to 5-6)
    elif n <= 80:
        return "#f2620881"  # Light orange (similar to 5-6)
    else:
        return "#c93c0979" # Orange-red (similar to 3-4)
    
def get_color_age_border(n):
    if n <= 10:
        return "#327a32"  # Light green (similar to 9-10)
    elif n <= 20:
        return "#577520"   # Light yellow (similar to 7-8)
    elif n<= 30:
        return "#697a2a"  # Light orange (similar to 5-6)
    elif n <= 40:
        return "#6c7222"  # Light orange (similar to 5-6)
    elif n <= 50:
        return "#7a8228"  # Light orange (similar to 5-6)
    elif n <=60:
        return "#928C1E"  # Light orange (similar to 5-6)
    elif n <= 70:
        return "#865004"  # Light orange (similar to 5-6)
    elif n <= 80:
        return "#843606"  # Light orange (similar to 5-6)
    else:
        return "#762407" # Orange-red (similar to 3-4)
    

def get_value_1(metabolite_data):
    """
    Processes the parsed metabolite data to extract specific values and rounds to 1 decimal place
    """
    ref_1 = ['43.5 - 91.7', '36.8 - 98.3']
    value_1 = []
    
    try:
        # Get Phenylalanine and round to 1 decimal
        phenylalanine = smart_round(float(metabolite_data.get('Phenylalanine', 0)), 1)
        value_1.append(phenylalanine)
        
        # Get Tyrosin (handle different spellings) and smart_round to 1 decimal
        tyrosin = smart_round(float(metabolite_data.get('Tyrosin', 0)), 1)
        value_1.append(tyrosin)
        
        return ref_1, value_1
        
    except Exception as e:
        print(f"Error in processing: {e}")
        # Return rounded default values
        return ref_1, [0.0, 0.0, 0.0]

def get_value_2(metabolite_data):
    """
    Processes the parsed metabolite data to extract specific values and rounds to 1 decimal place
    """
    ref_2 = ['115.2 - 290.0','137.0 - 288.5']
    value_2 = []
    
    try:
        Summ_Leu_Ile = smart_round(float(metabolite_data.get('Summ Leu-Ile', 0)), 1)
        value_2.append(Summ_Leu_Ile)
        
        valine= smart_round(float(metabolite_data.get('Valine', 0)), 1)
        value_2.append(valine)
                
        return ref_2, value_2
        
    except Exception as e:
        print(f"Error in processing: {e}")
        # Return rounded default values
        return ref_2, [0.0, 0.0, 0.0]
def get_value_3(metabolite_data):
    """
    Processes the parsed metabolite data to extract specific values and rounds to 1 decimal place
    """
    ref_3 = ['59.9 - 148.4','2.18 - 45.57','55.1 - 136.5','< 0.46','137.7 - 350.8','0.15 - 0.68','78.3 - 216.9','161.7 - 298.0','43.5 - 250.0','196.1 - 405.7']
    value_3 = []
    
    try:
        # Histidine
        histidine = smart_round(float(metabolite_data.get('Histidine', 0)), 1)
        value_3.append(histidine)
        metilhistidine = smart_round(float(metabolite_data.get('Methylhistidine', 0)), 2)
        value_3.append(metilhistidine)
        treonine = smart_round(float(metabolite_data.get('Threonine', 0)), 1)
        value_3.append(treonine)
        carnosine = smart_round(float(metabolite_data.get('Carnosine', 0)), 2)
        value_3.append(carnosine)
        glycine = smart_round(float(metabolite_data.get('Glycine', 0)), 1)
        value_3.append(glycine)
        dymetilglycine = smart_round(float(metabolite_data.get('DMG', 0)), 2)
        value_3.append(dymetilglycine)
        serine = smart_round(float(metabolite_data.get('Serine', 0)), 1)
        value_3.append(serine)
        Lysine= smart_round(float(metabolite_data.get('Lysine', 0)), 1)
        value_3.append(Lysine)
        glutaminic_acid = smart_round(float(metabolite_data.get('Glutamic acid', 0)), 1)
        value_3.append(glutaminic_acid)
        glutamine = smart_round(float(metabolite_data.get('Glutamine', 0)), 1)
        value_3.append(glutamine)
        
        return ref_3, value_3
        
    except Exception as e:
        print(f"Error in processing: {e}")
        # Return rounded default values
        return ref_3, [0.0, 0.0, 0.0]

def get_value_4(metabolite_data):
    """
    Processes the parsed metabolite data to extract specific values and rounds to 1 decimal place
    """
    ref_4 = ['17.4 - 47.4','< 0.97','27.7 - 145.8','28.6 - 82.7','5.68 - 19.88','0.26 - 7.17']
    value_4 = []
    
    try:
        # metionine
        methionine = smart_round(float(metabolite_data.get('Methionine', 0)), 1)
        value_4.append(methionine)
        Methionine_Sulfoxide = smart_round(float(metabolite_data.get('Methionine-Sulfoxide', 2)), 1)
        value_4.append(Methionine_Sulfoxide)
        Taurine = smart_round(float(metabolite_data.get('Taurine', 0)), 1)
        value_4.append(Taurine)
        Betaine = smart_round(float(metabolite_data.get('Betaine', 0)), 1)
        value_4.append(Betaine)
        Choline = smart_round(float(metabolite_data.get('Choline', 0)), 2)
        value_4.append(Choline)
        TMAO = smart_round(float(metabolite_data.get('TMAO', 0)), 2)
        value_4.append(TMAO)
        return ref_4, value_4
        
    except Exception as e:
        print(f"Error in processing: {e}")
        # Return rounded default values
        return ref_4, [0.0, 0.0, 0.0]

def get_value_5(metabolite_data):
    """
    Processes the parsed metabolite data to extract specific values and rounds to 1 decimal place
    """
    ref_5 = ['36.2 - 72.9','1.01 - 2.41','0.14 - 0.67','0.13 - 0.64','< 0.04','0.02 - 0.08']
    value_5 = []
    
    try:
        #Tryptophan
        tryptophan = smart_round(float(metabolite_data.get('Tryptophan', 0)), 1)
        value_5.append(tryptophan)
        kynurenine = smart_round(float(metabolite_data.get('Kynurenine', 0)), 2)
        value_5.append(kynurenine)
        antranillic_acid = smart_round(float(metabolite_data.get('Antranillic acid', 0)), 2)
        value_5.append(antranillic_acid)
        quinolinic_acid = smart_round(float(metabolite_data.get('Quinolinic acid', 0)), 2)
        value_5.append(quinolinic_acid)
        Xanthurenic_acid = smart_round(float(metabolite_data.get('Xanthurenic acid', 0)), 2)
        value_5.append(Xanthurenic_acid)
        Kynurenic_acid = smart_round(float(metabolite_data.get('Kynurenic acid', 0)), 2)
        value_5.append(Kynurenic_acid)
        return ref_5, value_5
        
    except Exception as e:
        print(f"Error in processing: {e}")
        # Return rounded default values
        return ref_5, [0.0, 0.0, 0.0]
    
def get_value_6(metabolite_data):
    """
    Processes the parsed metabolite data to extract specific values and rounds to 1 decimal place
    """
    ref_6 = ['0.02 - 1.45','< 0.09','0.08 - 0.25']
    value_6 = []
    
    try:
        # Serotonine
        serotonine = smart_round(float(metabolite_data.get('Serotonin', 0)), 2)
        value_6.append(serotonine)
        hiaa = smart_round(float(metabolite_data.get('HIAA', 0)), 2)
        value_6.append(hiaa)

        hydroxy_tryptophan = smart_round(float(metabolite_data.get('5-hydroxytryptophan', 0)), 2)
        value_6.append(hydroxy_tryptophan)
        return ref_6, value_6
        
    except Exception as e:
        print(f"Error in processing: {e}")
        
        return ref_6, [0.0, 0.0, 0.0]

def get_value_7(metabolite_data):
    """
    Processes the parsed metabolite data to extract specific values and rounds to 1 decimal place
    """
    ref_7 = ['0.54 - 2.38','0.33 - 1.15','0.01 - 0.06','0.14 - 2.04','< 0.29','< 0.18']
    value_7 = []
    
    try:
        # 3-indolacetic
        indole_acetic_acid = smart_round(float(metabolite_data.get('Indole-3-acetic acid', 0)), 2)
        value_7.append(indole_acetic_acid)
        indole_lactic_acid = smart_round(float(metabolite_data.get('Indole-3-lactic acid', 0)), 3)
        value_7.append(indole_lactic_acid)
        indole_carboxaldehyde = smart_round(float(metabolite_data.get('Indole-3-carboxaldehyde', 0)), 2)
        value_7.append(indole_carboxaldehyde)
        indole_propionic_acid = smart_round(float(metabolite_data.get('Indole-3-propionic acid', 0)), 2)
        value_7.append(indole_propionic_acid)
        indole_3_butyric = smart_round(float(metabolite_data.get('Indole-3-butyric', 0)), 3)
        value_7.append(indole_3_butyric)
        tryptamine = smart_round(float(metabolite_data.get('Tryptamine', 0)), 2)
        value_7.append(tryptamine)
        return ref_7, value_7
        
    except Exception as e:
        print(f"Error in processing: {e}")
        
        return ref_7, [0.0, 0.0, 0.0]

def get_value_8(metabolite_data):
    """
    Processes the parsed metabolite data to extract specific values and rounds to 1 decimal place
    """
    ref_8 = ['106.7 - 358.0','3.16 - 14.09','0.29 - 1.01', '< 0.14','0.28 - 1.04','1.31 - 6.42','45.9 - 164.7','26.5 - 58.3','31.1 - 115.8','15.6 - 33.7','13.8 - 101.3','16.8 - 61.8']
    value_8 = []
    
    try:
        # Proline
        proline = smart_round(float(metabolite_data.get('Proline', 0)), 1)
        value_8.append(proline)
        hydroxyproline = smart_round(float(metabolite_data.get('Hydroxyproline', 0)), 2)
        value_8.append(hydroxyproline)
        adma = smart_round(float(metabolite_data.get('ADMA', 0)), 2)
        value_8.append(adma)
        nmma = smart_round(float(metabolite_data.get('NMMA', 0)), 2)
        value_8.append(nmma)
        sdma = smart_round(float(metabolite_data.get('TotalDMA (SDMA)', 0)), 2)
        value_8.append(sdma)
        homoarginine = smart_round(float(metabolite_data.get('Homoarginine', 0)), 2)
        value_8.append(homoarginine)
        arginine = smart_round(float(metabolite_data.get('Arginine', 0)), 1)
        value_8.append(arginine)
        Citrulline = smart_round(float(metabolite_data.get('Citrulline', 0)), 1)
        value_8.append(Citrulline)
        Orintine = smart_round(float(metabolite_data.get('Ornitine', 0)), 1)
        value_8.append(Orintine)
        asparagine = smart_round(float(metabolite_data.get('Asparagine', 0)), 1)
        value_8.append(asparagine)
        asparagine_acid = smart_round(float(metabolite_data.get('Aspartic acid', 0)), 1)
        value_8.append(asparagine_acid)
        creatine = smart_round(float(metabolite_data.get('Creatinine', 0)), 1)
        value_8.append(creatine)

        return ref_8, value_8
        
    except Exception as e:
        print(f"Error in processing: {e}")
        
        return ref_8, [0.0, 0.0, 0.0]

def get_value_9(metabolite_data):
    """
    Processes the parsed metabolite data to extract specific values and rounds to 1 decimal place
    """
    ref_9 = ['199.7 - 486.5','19.5 - 49.9','3.75 - 12.30']
    value_9 = []
    
    try:
        # Alanine
        alanine = smart_round(float(metabolite_data.get('Alanine', 0)), 1)
        value_9.append(alanine)
        # c0
        c0 = smart_round(float(metabolite_data.get('C0', 0)), 1)
        value_9.append(c0)
        c2 = smart_round(float(metabolite_data.get('C2', 0)), 2)
        value_9.append(c2)
        return ref_9, value_9
        
    except Exception as e:
        print(f"Error in processing: {e}")
        
        return ref_9, [0.0, 0.0, 0.0]

def get_value_10(metabolite_data):
    """
    Processes the parsed metabolite data to extract specific values and rounds to 1 decimal place
    """
    ref_10 = ['0.13 - 0.54','0.06 - 0.31','0.03 - 0.14','< 0.02','< 0.001','< 0.01']
    value_10 = []
    
    try:
        # c3
        c3 = smart_round(float(metabolite_data.get('C3', 0)), 2)
        value_10.append(c3)
        c4 = smart_round(float(metabolite_data.get('C4', 0)), 2)
        value_10.append(c4)
        c5 = smart_round(float(metabolite_data.get('C5', 0)), 2)
        value_10.append(c5)
        c5_1 = smart_round(float(metabolite_data.get('C5-1', 0)), 2)
        value_10.append(c5_1)
        c5_DC = smart_round(float(metabolite_data.get('C5-DC', 0)), 3)
        value_10.append(c5_DC)
        c5_OH = smart_round(float(metabolite_data.get('C5-OH', 0)), 2)
        value_10.append(c5_OH)
        return ref_10, value_10
        
    except Exception as e:
        print(f"Error in processing: {e}")
        
        return ref_10, [0.0, 0.0, 0.0]

def get_value_11(metabolite_data):
    """
    Processes the parsed metabolite data to extract specific values and rounds to 1 decimal place
    """
    ref_11 = ['0.01 - 0.06','< 0.01','0.03 - 0.22','0.01 - 0.06','0.03 - 0.22','0.02 - 0.16','< 0.01','0.01 - 0.07','< 0.03']
    value_11 = []
    
    try:
        # c6
        c6 = smart_round(float(metabolite_data.get('C6', 0)), 2)
        value_11.append(c6)
        c6_DC = smart_round(float(metabolite_data.get('C6-DC', 0)), 3)
        value_11.append(c6_DC)
        c8 = smart_round(float(metabolite_data.get('C8', 0)), 2)
        value_11.append(c8)
        c8_1 = smart_round(float(metabolite_data.get('C8-1', 0)), 2)
        value_11.append(c8_1)
        c10 = smart_round(float(metabolite_data.get('C10', 0)), 2)
        value_11.append(c10)
        c10_1 = smart_round(float(metabolite_data.get('C10-1', 0)), 2)
        value_11.append(c10_1)
        c10_2 = smart_round(float(metabolite_data.get('C10-2', 0)), 2)
        value_11.append(c10_2)
        c12 = smart_round(float(metabolite_data.get('C12', 0)), 2)
        value_11.append(c12)
        c12_1 = smart_round(float(metabolite_data.get('C12-1', 0)), 2)
        value_11.append(c12_1)
        return ref_11, value_11
        
    except Exception as e:
        print(f"Error in processing: {e}")
        
        return ref_11, [0.0, 0.0, 0.0] 

def get_value_12(metabolite_data):
    """
    Processes the parsed metabolite data to extract specific values and rounds to 1 decimal place
    """
    ref_12 = ['0.01 - 0.03','0.01 - 0.12','< 0.06','< 0.02','0.03 - 0.08','< 0.02','< 0.002','0.01 - 0.02','0.02 - 0.05','0.04 - 0.12','< 0.002','0.02 - 0.07','0.001 - 0.003']
    value_12 = []
    
    try:
        # c14
        c14 = smart_round(float(metabolite_data.get('C14', 0)), 2)
        value_12.append(c14)
        c14_1 = smart_round(float(metabolite_data.get('C14-1', 0)), 2)
        value_12.append(c14_1)
        c14_2 = smart_round(float(metabolite_data.get('C14-2', 0)), 2)
        value_12.append(c14_2)
        c14_OH = smart_round(float(metabolite_data.get('C14-OH', 0)), 2)
        value_12.append(c14_OH)
        c16 = smart_round(float(metabolite_data.get('C16', 0)), 2)
        value_12.append(c16)
        c16_1 = smart_round(float(metabolite_data.get('C16-1', 0)), 2)
        value_12.append(c16_1)
        C16_1_OH = smart_round(float(metabolite_data.get('C16-1-OH', 0)), 2)
        value_12.append(C16_1_OH)
        c16_OH = smart_round(float(metabolite_data.get('C16-OH', 0)), 2)
        value_12.append(c16_OH)
        c18 = smart_round(float(metabolite_data.get('C18', 0)), 2)
        value_12.append(c18)
        c18_1 = smart_round(float(metabolite_data.get('C18-1', 0)), 2)
        value_12.append(c18_1)
        c18_1_OH = smart_round(float(metabolite_data.get('C18-1-OH', 0)), 3)
        value_12.append(c18_1_OH)
        c18_2 = smart_round(float(metabolite_data.get('C18-2', 0)), 2)
        value_12.append(c18_2)
        c18_OH = smart_round(float(metabolite_data.get('C18-OH', 0)), 3)
        value_12.append(c18_OH)
        return ref_12, value_12
        
    except Exception as e:
        print(f"Error in processing: {e}")
        
        return ref_12, [0.0, 0.0, 0.0]
    

def get_value_13(metabolite_data):
    """
    Processes the parsed metabolite data to extract specific values and rounds to 1 decimal place
    """
    ref_13 = ['0.09 - 0.25','0.03 - 0.16','0.01 - 0.03']
    value_13 = []
    
    try:
        # Pantotenic acid
        pantotenic_acid = smart_round(float(metabolite_data.get('Pantothenic', 0)), 2)
        value_13.append(pantotenic_acid)
        riboflavin = smart_round(float(metabolite_data.get('Riboflavin', 0)), 2)
        value_13.append(riboflavin)
        melatonine = smart_round(float(metabolite_data.get('Melatonin', 0)), 2)
        value_13.append(melatonine)
        return ref_13, value_13
        
    except Exception as e:
        print(f"Error in processing: {e}")
        
        return ref_13, [0.0, 0.0, 0.0]

def get_value_14(metabolite_data):
    """
    Processes the parsed metabolite data to extract specific values and rounds to 1 decimal place
    """
    ref_14 = ['0.70 - 5.07','0.12 - 0.29', '0.25 - 0.39']
    value_14 = []
    
    try:
        # Uridine
        uridine = smart_round(float(metabolite_data.get('Uridine', 0)), 2)
        value_14.append(uridine)
        adenosine = smart_round(float(metabolite_data.get('Adenosin', 0)), 2)
        value_14.append(adenosine)
        Citidine = smart_round(float(metabolite_data.get('Cytidine', 0)), 2)
        value_14.append(Citidine)
        return ref_14, value_14
        
    except Exception as e:
        print(f"Error in processing: {e}")
        
        return ref_14, [0.0, 0.0, 0.0]


def get_value_15(metabolite_data):
    """
    Processes the parsed metabolite data to extract specific values and rounds to 1 decimal place
    """
    ref_15 = ['0.29 - 0.80','< 0.03']
    value_15 = []
    
    try:
        # Cortisol
        cortisol = smart_round(float(metabolite_data.get('Cortisol', 0)), 2)
        value_15.append(cortisol)
        # Histamine
        histamine = smart_round(float(metabolite_data.get('Histamine', 0)), 2)
        value_15.append(histamine)
        return ref_15, value_15
        
    except Exception as e:
        print(f"Error in processing: {e}")
        
        return ref_15, [0.0, 0.0, 0.0]


def color_text_ref(value: float, ref: str):
    if ' - ' in ref:
        lower, upper = map(float, ref.split(' - '))
        if value > upper:
            return '#dc3545'
        elif value < lower:
            return '#dc3545'
        else:
            return '#404547'
    elif ref.startswith('< '):
        upper = float(ref.split('< ')[1])
        if value > upper:
            return '#dc3545'
        elif value < 0:  # Assuming <45 means 0-45 as per your note
            return '#dc3545'
        else:
            return '#404547'
    else:
        # Handle other cases if needed
        return '#404547'

def heighlight_out_of_range(value: float, ref: str):
    if ' - ' in ref:
        lower, upper = map(float, ref.split(' - '))
        if value > upper:
            return '#f8d7da'
        elif value < lower:
            return '#f8d7da'
        else:
            return 'white'
    elif ref.startswith('< '):
        upper = float(ref.split('< ')[1])
        if value > upper:
            return '#f8d7da'
        elif value < 0:  # Assuming <45 means 0-45 as per your note
            return '#f8d7da'
        else:
            return 'white'
    else:
        # Handle other cases if needed
        return 'white'
    
def need_of_margin(value: float, ref: str):
    if ref.__contains__(' - '):
        if value > float(ref.split(' - ')[1]):
            return '0'
        else:
            return '0px'
    elif value > float(ref.split('< ')[1]):
        return '0'
    else:
        return '0px'


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
    if n <= 0:
        return '#10b981'
    if n <= 10:
        return '#10b962'  # Light green (similar to 9-10)
    elif n <= 20:
        return '#50c150'   # Light yellow (similar to 7-8)
    elif n<= 30:
        return '#9fd047'  # Light orange (similar to 5-6)
    elif n <= 40:
        return  '#feb61d'  # Light orange (similar to 5-6)
    elif n <= 50:
        return  '#fe991d'  # Light orange (similar to 5-6)
    elif n <=60:
        return '#f25708'  # Light orange (similar to 5-6)
    elif n <= 70:
        return "#f23b08"  # Light orange (similar to 5-6)
    elif n <= 80:
        return '#f21e08'  # Light orange (similar to 5-6)
    else:
        return '#c90909' # Orange-red (similar to 3-4)

    

def get_status_level(n):
    if n <= 10:
        return 'Отлично'  # Light green (similar to 9-10)
    elif n <= 20:
        return 'Хорошо'   # Light yellow (similar to 7-8)
    elif n<= 30:
        return 'Хорошо'  # Light orange (similar to 5-6) 
    elif n <= 40:
        return 'Требуется коррекция'  # Light orange (similar to 5-6)
    elif n <= 50:
        return 'Требуется коррекция'  # Light orange (similar to 5-6)
    
    elif n <= 70:
        return 'Серьезные нарушения'  # Light orange (similar to 5-6)
    else:
        return 'Серьезные нарушения' # Orange-red (similar to 3-4)
    
def get_text_from_procent(n):
    if n < 30:
        return 'Замедленный'
    elif n < 60:
        return 'Нормальный'
    elif n < 80:
        return 'Умеренно ускоренный'
    else:
        return 'Сильно ускоренный'



def generate_radial_diagram(df_result, output_path):
    """Generate radial diagram and save to specified path"""
    # Ensure df_result is a DataFrame (not a file path)
    if isinstance(df_result, str):
        df_result = pd.read_excel(df_result)
    
    # Process labels to split long ones into two lines
    def split_label(label):
        """Split label into two lines if total length exceeds 25 characters.
        Words that would push the first line over 25 characters are moved to the second line.
        """
        if len(label) > 25:
            words = label.split()
            first_line = []
            second_line = []
            char_count = 0
            
            for word in words:
                # If adding this word would exceed 25 chars (including spaces), move it to second line
                if char_count + len(word) > 35 and first_line:
                    second_line.append(word)
                else:
                    first_line.append(word)
                    char_count += len(word) + 1  # +1 for space
            
            # Join the lines only if we actually split into two lines
            if second_line:
                return '\n'.join([' '.join(first_line), ' '.join(second_line)])
        
        return label

    labels = [split_label(label) for label in df_result['Группа риска'].tolist()]
    risk_levels = df_result['Риск-скор'].tolist()

    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # Close the circle
    risk_levels += risk_levels[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 6), subplot_kw=dict(polar=True))
        # Remove outer circle border
    ax.spines['polar'].set_visible(False)

    # Updated color scheme as specified
    colors = [
        '#c90909',  # 1 балл
        "#f21e08",  # 2 балла
        "#de3805",  # 3 балла
        '#f25708',  # 4 балла
        '#fe991d',  # 5 баллов
        '#feb61d',  # 6 баллов
        '#9fd047',  # 7 баллов
        '#50c150',  # 8 баллов
        "#10b962",  # 9 баллов
        '#10b981'   # 10 баллов
    ]

    # Fill between levels with the specified colors
    levels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for i in range(len(levels) - 1):
        ax.fill_between(angles, levels[i], levels[i + 1], color=colors[i], alpha=0.3)
    
    # Plot data with blue markers and white borders
    ax.fill(angles, risk_levels, color='#2563eb', alpha=0.25)
    ax.plot(angles, risk_levels, color='#2563eb', linewidth=2, 
            marker='o', markersize=8, markerfacecolor='#2563eb', 
            markeredgecolor='white', markeredgewidth=1.5)
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=12, color='#404547')
    
    # Label adjustments
    for label, angle in zip(ax.get_xticklabels(), angles[:-1]):
        label.set_rotation_mode('anchor')
        if np.pi/2 < angle < 3*np.pi/2:
            rotation = np.degrees(angle) + 90
            ha = 'right'
        else:
            rotation = np.degrees(angle) - 90
            ha = 'left'
        
        label.set_rotation(rotation)
        label.set_ha(ha)
        label.set_va('center')
        ax.plot([angle, angle], [10, 10.5], color='gray', linestyle='-', linewidth=0.5, alpha=0.5)
    
    ax.tick_params(axis='x', zorder=1000, pad=0)
    ax.set_ylim(0, 10.5)

    # Save the figure
    fig.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close(fig)
        
    
def calculate_pointer_position(value: float, ref_range: str):
    try:
        value = float(value)
        
        # Parse reference range
        if '-' in ref_range:
            # Format "23 - 50"
            ref_min, ref_max = map(float, ref_range.split('-'))
        elif ref_range.startswith('<'):
            # Format "<45" means 0-45
            ref_min = 0.0
            ref_max = float(ref_range[1:])
        else:
            # Default case (single value or other format)
            ref_min = float(ref_range)
            ref_max = ref_min * 1.1  # Small range around the value
        
        # Calculate position (0-100)
        if value < ref_min:
            return 0
        elif value > ref_max:
            return 100
        else:
            position = ((value - ref_min) / (ref_max - ref_min)) * 100
            return max(0, min(100, round(position, 2)))  # Clamp and round to 2 decimals
    
    except (ValueError, AttributeError, TypeError):
        # Return middle position if there's any error
        return 50

def Oxidative_Stress_Group(file_path):
    try:
        # Load the risk parameters
        risk_params = pd.read_excel(file_path)
        # Extract df [Группа_риска] = Резистентность к стрессорамand [Категория] = Оксидативный стресс keep all other columns
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Резистентность к стрессорам') & (risk_params['Категория'] == 'Оксидативный стресс')]

        
        # Calculate w_clear_score sum of [Score_Weighted] and w_max_score sum of [Max_score_weighted]
        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    except Exception as e:
        print(f"Error in Inflammation_Group: {e}")
        return 100
    

def Inflammation_and_Microbial_Group(file_path):
    try:
        # Load the risk parameters
        risk_params = pd.read_excel(file_path)
        # Extract df [Группа_риска] = Резистентность к стрессорамand [Категория] = Воспаление и микробный стресс keep all other columns
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Резистентность к стрессорам') & (risk_params['Категория'] == 'Воспаление и микробный стресс')]

        
        # Calculate w_clear_score sum of [Score_Weighted] and w_max_score sum of [Max_score_weighted]
        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    except Exception as e:
        print(f"Error in Inflammation_Group: {e}")
        return 100

def Nitrogen_Toxic_Group(file_path):
    try:
        # Load the risk parameters
        risk_params = pd.read_excel(file_path)
        # Extract df [Группа_риска] = Резистентность к стрессорамand [Категория] = Азотистые токсины keep all other columns
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Резистентность к стрессорам') & (risk_params['Категория'] == 'Азотистые токсины')]

        
        # Calculate w_clear_score sum of [Score_Weighted] and w_max_score sum of [Max_score_weighted]
        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    except Exception as e:
        print(f"Error in Inflammation_Group: {e}")
        return 100

def Lipid_Toxic_Group(file_path):
    try:
        # Load the risk parameters
        risk_params = pd.read_excel(file_path)
        # Extract df [Группа_риска] = Резистентность к стрессорамand [Категория] = Липидные токсины / окс. стресс keep all other columns
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Резистентность к стрессорам') & (risk_params['Категория'] == 'Липидные токсины / окс. стресс')]

        
        # Calculate w_clear_score sum of [Score_Weighted] and w_max_score sum of [Max_score_weighted]
        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    except Exception as e:
        print(f"Error in Inflammation_Group: {e}")
        return 100
 
    
def Energy_Exchange_Group(file_path):
    """Энергетический обмен - Метаболическая адаптация и стрессоустойчивость"""
    try:
        risk_params = pd.read_excel(file_path)
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Метаболическая адаптация и стрессоустойчивость') & 
                                    (risk_params['Категория'] == 'Энергетический обмен')]

        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    
    except Exception as e:
        print(f"Error in Energy_Exchange_Group: {e}")
        return 100

def Neuroadaptation_Group(file_path):
    """Нейро-адаптация - Метаболическая адаптация и стрессоустойчивость"""
    try:
        risk_params = pd.read_excel(file_path)
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Метаболическая адаптация и стрессоустойчивость') & 
                                    (risk_params['Категория'] == 'Нейро-адаптация')]

        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    
    except Exception as e:
        print(f"Error in Neuroadaptation_Group: {e}")
        return 100

def Stress_Aminoacid_Group(file_path):
    """Стресс-аминокислоты - Метаболическая адаптация и стрессоустойчивость"""
    try:
        risk_params = pd.read_excel(file_path)
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Метаболическая адаптация и стрессоустойчивость') & 
                                    (risk_params['Категория'] == 'Стресс-аминокислоты')]

        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    
    except Exception as e:
        print(f"Error in Stress_Aminoacid_Group: {e}")
        return 100

def Mitochondria_Creatinine_Group(file_path):
    """Митохондрии и креатин - Метаболическая адаптация и стрессоустойчивость"""
    try:
        risk_params = pd.read_excel(file_path)
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Метаболическая адаптация и стрессоустойчивость') & 
                                    (risk_params['Категория'] == 'Митохондрии и креатин')]

        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    
    except Exception as e:
        print(f"Error in Mitochondria_Creatinine_Group: {e}")
        return 100

def Glutamate_Exchange_Group(file_path):
    """Глутамат-глутаминовая ось - Метаболическая адаптация и стрессоустойчивость"""
    try:
        risk_params = pd.read_excel(file_path)
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Метаболическая адаптация и стрессоустойчивость') & 
                                    (risk_params['Категория'] == 'Глутамат-глутаминовая ось')]

        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    
    except Exception as e:
        print(f"Error in Glutamate_Exchange_Group: {e}")
        return 100


# 6. Статус микробиоты (8/10)
def Tryptophan_Metabolism_Group(file_path):
    """Метаболизм триптофана - Статус микробиоты"""
    try:
        risk_params = pd.read_excel(file_path)
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Статус микробиоты') & 
                                    (risk_params['Категория'] == 'Метаболизм триптофана')]

        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    
    except Exception as e:
        print(f"Error in Tryptophan_Metabolism_Group: {e}")
        return 100

def Inflammation_and_Immune_Group(file_path):
    """Воспаление и иммунитет - Статус микробиоты"""
    try:
        risk_params = pd.read_excel(file_path)
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Статус микробиоты') & 
                                    (risk_params['Категория'] == 'Воспаление и иммунитет')]

        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    
    except Exception as e:
        print(f"Error in Inflammation_and_Immune_Group: {e}")
        return 100


# 7. Темп биологического старения (7/10)
def Tryptophan_Inflammation_Group(file_path):
    """Триптофан / воспаление - Темп биологического старения"""
    try:
        risk_params = pd.read_excel(file_path)
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Темп биологического старения') & 
                                    (risk_params['Категория'] == 'Триптофан / воспаление')]

        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    
    except Exception as e:
        print(f"Error in Tryptophan_Inflammation_Group: {e}")
        return 100

def Oxidative_Stress_Age_Group(file_path):
    """Оксидативный стресс - Темп биологического старения"""
    try:
        risk_params = pd.read_excel(file_path)
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Темп биологического старения') & 
                                    (risk_params['Категория'] == 'Оксидативный стресс')]

        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    
    except Exception as e:
        print(f"Error in Tryptophan_Inflammation_Group: {e}")
        return 100
    
def Metochondria_Age_Group(file_path):
    """митохондриальные показатели - Темп биологического старения"""
    try:
        risk_params = pd.read_excel(file_path)
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Темп биологического старения') & 
                                    (risk_params['Категория'] == 'Митохондриальные показатели')]

        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    
    except Exception as e:
        print(f"Error in Tryptophan_Inflammation_Group: {e}")
        return 100
    
    
def Oxidative_Stress_Group(file_path):
    """Оксидативный стресс - Темп биологического старения"""
    try:
        risk_params = pd.read_excel(file_path)
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Темп биологического старения') & 
                                    (risk_params['Категория'] == 'Оксидативный стресс')]

        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    
    except Exception as e:
        print(f"Error in Oxidative_Stress_Group: {e}")
        return 100

def Mitochondria_Group(file_path):
    """Митохондрии - Темп биологического старения"""
    try:
        risk_params = pd.read_excel(file_path)
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Темп биологического старения') & 
                                    (risk_params['Категория'] == 'Митохондрии')]

        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    
    except Exception as e:
        print(f"Error in Mitochondria_Group: {e}")
        return 100

def Neuroendocrine_Group(file_path):
    """Нейроэндокринная ось - Темп биологического старения"""
    try:
        risk_params = pd.read_excel(file_path)
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Темп биологического старения') & 
                                    (risk_params['Категория'] == 'Нейроэндокринная ось')]

        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    
    except Exception as e:
        print(f"Error in Neuroendocrine_Group: {e}")
        return 100

def Integrative_Index_Group(file_path):
    """Интегративные индексы - Темп биологического старения"""
    try:
        risk_params = pd.read_excel(file_path)
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Темп биологического старения') & 
                                    (risk_params['Категория'] == 'Интегративные индексы')]

        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    
    except Exception as e:
        print(f"Error in Integrative_Index_Group: {e}")
        return 100


# 8. Воспаление и иммунитет (8/10)
def Ido_Path_Tryptophan_Group(file_path):
    """IDO-путь / триптофан - Воспаление и иммунитет"""
    try:
        risk_params = pd.read_excel(file_path)
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Воспаление и иммунитет') & 
                                    (risk_params['Категория'] == 'IDO-путь / триптофан')]

        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    
    except Exception as e:
        print(f"Error in Ido_Path_Tryptophan_Group: {e}")
        return 100

def Neuromediators_Group(file_path):
    """Нейромедиаторы - Воспаление и иммунитет"""
    try:
        risk_params = pd.read_excel(file_path)
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Воспаление и иммунитет') & 
                                    (risk_params['Категория'] == 'Нейромедиаторы')]

        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    
    except Exception as e:
        print(f"Error in Neuromediators_Group: {e}")
        return 100

def Indols_and_Phenols_Group(file_path):
    """Индолы и фенолы - Воспаление и иммунитет"""
    try:
        risk_params = pd.read_excel(file_path)
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Воспаление и иммунитет') & 
                                    (risk_params['Категория'] == 'Индолы и фенолы')]

        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    
    except Exception as e:
        print(f"Error in Indols_and_Phenols_Group: {e}")
        return 100

def General_Stress_Immune_Group(file_path):
    """Общий стресс / иммунитет - Воспаление и иммунитет"""
    try:
        risk_params = pd.read_excel(file_path)
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Воспаление и иммунитет') & 
                                    (risk_params['Категория'] == 'Общий стресс / иммунитет')]

        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    
    except Exception as e:
        print(f"Error in General_Stress_Immune_Group: {e}")
        return 100

def Complex_Index_Group(file_path):
    """Комплексный индекс - Воспаление и иммунитет"""
    try:
        risk_params = pd.read_excel(file_path)
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Воспаление и иммунитет') & 
                                    (risk_params['Категория'] == 'Комплексный индекс')]

        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    
    except Exception as e:
        print(f"Error in Complex_Index_Group: {e}")
        return 100


# 9. Токсическая нагрузка (7/10)
def Amiac_Detox_Group(file_path):
    """Аммиачная детоксикация - Токсическая нагрузка"""
    try:
        risk_params = pd.read_excel(file_path)
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Метаболическая детоксикация') & 
                                    (risk_params['Категория'] == 'Аммиачная детоксикация')]

        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    
    except Exception as e:
        print(f"Error in Amiac_Detox_Group: {e}")
        return 100
    
# 11. Нутриентный статус (7/10)
def Vitamine_B2_Group(file_path):
    """Витамин B2 (рибофлавин) - Нутриентный статус"""
    try:
        risk_params = pd.read_excel(file_path)
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Витаминный статус') & 
                                    (risk_params['Категория'] == 'Витамин B2 (рибофлавин)')]

        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    
    except Exception as e:
        print(f"Error in Vitamine_B2_Group: {e}")
        return 100

def Vitamine_B5_Group(file_path):
    """Витамин B5 (пантотенат) - Нутриентный статус"""
    try:
        risk_params = pd.read_excel(file_path)
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Витаминный статус') & 
                                    (risk_params['Категория'] == 'Витамин B5 (пантотенат)')]

        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    
    except Exception as e:
        print(f"Error in Vitamine_B5_Group: {e}")
        return 100

def Vitamine_B6_Group(file_path):
    """Витамин B6 - Нутриентный статус"""
    try:
        risk_params = pd.read_excel(file_path)
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Витаминный статус') & 
                                    (risk_params['Категория'] == 'Витамин B6')]

        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    
    except Exception as e:
        print(f"Error in Vitamine_B6_Group: {e}")
        return 100

def Vitamine_B9_B12_Group(file_path):
    """Витамин B9 / B12 - Нутриентный статус"""
    try:
        risk_params = pd.read_excel(file_path)
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Витаминный статус') & 
                                    (risk_params['Категория'] == 'Витамин B9 / B12')]

        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    
    except Exception as e:
        print(f"Error in Vitamine_B9_B12_Group: {e}")
        return 100

def Vitamine_B3_NAD_Group(file_path):
    """Витамин B3 / NAD+ - Нутриентный статус"""
    try:
        risk_params = pd.read_excel(file_path)
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Витаминный статус') & 
                                    (risk_params['Категория'] == 'Витамин B3 / NAD+')]

        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    
    except Exception as e:
        print(f"Error in Vitamine_B3_NAD_Group: {e}")
        return 100
    
# ddddddddddddddddddd
def Serum_Aminoacids_Group(file_path):
    try:
        risk_params = pd.read_excel(file_path)
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Витаминный статус') & 
                                    (risk_params['Категория'] == 'Серосодержащие АК')]

        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    
    except Exception as e:
        print(f"Error in Vitamine_B3_NAD_Group: {e}")
        return 100

def Neurotroph_Reserv_Group(file_path):
    try:
        risk_params = pd.read_excel(file_path)
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Витаминный статус') & 
                                    (risk_params['Категория'] == 'Нейротрофный резерв')]

        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    
    except Exception as e:
        print(f"Error in Vitamine_B3_NAD_Group: {e}")
        return 100

# 10. Здоровье митохондрий (9/10)
def Energy_Exchange_Carnitine_Group(file_path):
    """Энергетический обмен - Здоровье митохондрий"""
    try:
        risk_params = pd.read_excel(file_path)
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Здоровье митохондрий') & 
                                    (risk_params['Категория'] == 'Энергетический обмен (карнитиновый цикл)')]

        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    
    except Exception as e:
        print(f"Error in Energy_Exchange_Carnitine_Group: {e}")
        return 100
    
def Antioxidation_Group(file_path):
    """Антиоксидантная защита - Здоровье митохондрий"""
    try:
        risk_params = pd.read_excel(file_path)
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Здоровье митохондрий') & 
                                    (risk_params['Категория'] == 'Антиоксидантная защита')]

        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
    
    except Exception as e:
        print(f"Error in Energy_Exchange_Carnitine_Group: {e}")
        return 100
    
def Mitochondrial_Group(file_path):
    try:
        # Load the risk parameters
        risk_params = pd.read_excel(file_path)
    
        risk_params = risk_params.loc[(risk_params['Группа_риска'] == 'Здоровье митохондрий') & (risk_params['Категория'] == 'β-окисление / жирные кислоты')]

        
        # Calculate w_clear_score sum of [Score_Weighted] and w_max_score sum of [Max_score_weighted]
        total = risk_params.iloc[0]['Subgroup_score']
        
        if total >= 90:
            return 90
        else:
            return total
        
    except Exception as e:
        print(f"Error in Inflammation_Group: {e}")
        return 100

app = Dash(__name__)


import argparse
import signal
import sys

def shutdown_handler(signum, frame):
    sys.exit(0)

signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--age', required=True)
    parser.add_argument('--gender', required=True)
    parser.add_argument('--date', required=True)
    parser.add_argument('--metabolomic_data', required=True)
    parser.add_argument('--risk_scores', required=True)
    parser.add_argument('--risk_params', required=True)
    args = parser.parse_args()
    # Register shutdown handler
    signal.signal(signal.SIGTERM, shutdown_handler)
    
    try:
        # Update global variables from command line args
        name = args.name
        age = args.age
        gender = args.gender
        date = args.date
        metabolomic_data_path = args.metabolomic_data
        risk_scores_path = args.risk_scores
        risk_params_path = args.risk_params
        
        # Process files with safety checks
        metabolite_data = safe_parse_metabolite_data(metabolomic_data_path)
        
        risk_scores = pd.read_excel(risk_scores_path)
        
        # Generate radial diagram
        radial_path = os.path.join('assets', "radial_diagram.png")
        generate_radial_diagram(risk_scores, radial_path)
        
        # Calculate all values using safe functions
        ref_1, value_1 = get_value_1(metabolite_data)
        ref_2, value_2 = get_value_2(metabolite_data)
        ref_3, value_3 = get_value_3(metabolite_data)
        ref_4, value_4 = get_value_4(metabolite_data)
        ref_5, value_5 = get_value_5(metabolite_data)
        ref_6, value_6 = get_value_6(metabolite_data)
        ref_7, value_7 = get_value_7(metabolite_data)
        ref_8, value_8 = get_value_8(metabolite_data)
        ref_9, value_9 = get_value_9(metabolite_data)
        ref_10, value_10 = get_value_10(metabolite_data)
        ref_11, value_11 = get_value_11(metabolite_data)
        ref_12, value_12 = get_value_12(metabolite_data)
        ref_13, value_13 = get_value_13(metabolite_data)
        ref_14, value_14 = get_value_14(metabolite_data)
        ref_15, value_15 = get_value_15(metabolite_data)
        
        # Состояние сердечно-сосудистой системы
        mitochondrial_score = Mitochondrial_Group(risk_params_path)
        
        # Влияние факторов среды
        oxidative_stress_score = Oxidative_Stress_Group(risk_params_path)
        inflam_and_microbiotic_score = Inflammation_and_Microbial_Group(risk_params_path)
        # aromatic_toxic_score = Aromatic_Toxic_Group(risk_params_path, metabolite_data)
        nitrogen_toxic_score = Nitrogen_Toxic_Group(risk_params_path)
        lipid_toxic_score = Lipid_Toxic_Group(risk_params_path)
        
        
        # Метаболическая адаптация и стрессоустойчивость
        energy_exchange_score = Energy_Exchange_Group(risk_params_path)
        neuroadaptation_score = Neuroadaptation_Group(risk_params_path)
        stress_aminoacid_score = Stress_Aminoacid_Group(risk_params_path)
        metochondria_creatinine_score = Mitochondria_Creatinine_Group(risk_params_path)
        glutamate_exchange_score = Glutamate_Exchange_Group(risk_params_path)
        
        # Статус микробиоты
        tryptophan_metabolism_score = Tryptophan_Metabolism_Group(risk_params_path)
        # microbial_stress_score = Microbial_Stress_Group(risk_params_path, metabolite_data)
        inflam_immune_score = Inflammation_and_Immune_Group(risk_params_path)
        
        
        # Воспаление и иммунитет
        ido_path_tryptophan_score = Ido_Path_Tryptophan_Group(risk_params_path)
        neuromediators_score = Neuromediators_Group(risk_params_path)
        indols_phenols_score = Indols_and_Phenols_Group(risk_params_path)
        general_stress_immune_score = General_Stress_Immune_Group(risk_params_path)
        complex_index = Complex_Index_Group(risk_params_path)
        
        # Метаболическая детоксикация
        amiac_detox_score =  Amiac_Detox_Group(risk_params_path)
        # оксидативная нагрузка уже есть
        # азотистая нагрузка тоже есть
        
        # Здоровье митохондрий
        energy_exchange_carnitine_score = Energy_Exchange_Carnitine_Group(risk_params_path)
        antoxidant_system = Antioxidation_Group(risk_params_path)
        
        # Витаминный статус
        vitamine_b2_score = Vitamine_B2_Group(risk_params_path)
        vitamine_b5_score = Vitamine_B5_Group(risk_params_path)
        vitamine_b6_score = Vitamine_B6_Group(risk_params_path)
        vitamine_b9_b12_score = Vitamine_B9_B12_Group(risk_params_path)
        vitamine_b3_nad_score = Vitamine_B3_NAD_Group(risk_params_path)
        serum_aminoacids_score = Serum_Aminoacids_Group(risk_params_path)
        # energy exchange
        neurotroph_reserv_score = Neurotroph_Reserv_Group(risk_params_path)
        
        
        liver_score = int(round(risk_scores.loc[risk_scores["Группа риска"] == "Состояние функции печени", "Риск-скор"].values[0], 0))
        oncology_score = int(round(risk_scores.loc[risk_scores["Группа риска"] == "Оценка пролиферативных процессов", "Риск-скор"].values[0], 0))
        cardiovascular_score = int(round(risk_scores.loc[risk_scores["Группа риска"] == "Состояние сердечно-сосудистой системы", "Риск-скор"].values[0], 0))
        pulmonary_score = int(round(risk_scores.loc[risk_scores["Группа риска"] == "Состояние дыхательной системы", "Риск-скор"].values[0], 0))
        arthritis_score = int(round(risk_scores.loc[risk_scores["Группа риска"] == "Состояние иммуного метаболического баланса", "Риск-скор"].values[0], 0))
        
        vascular_data = [
                {
                    "name": "Аргинин/ADMA",
                    "value": smart_round(metabolite_data['Arg/ADMA'], 2),
                    "norm": '33.93 - 290.07',
                    "description": "Отражает баланс между доступным для синтеза оксида азота (NO) аргинином и ингибитором синтеза NO – асимметричным диметиларгинином (ADMA).",
                },
                {
                    "name": "(Аргинин + Гомоаргинин) / ADMA",
                    "value": smart_round(metabolite_data['(Arg+HomoArg)/ADMA'], 2),
                    "norm": '37.49 - 298.4',
                    "description": "Отражает общий баланс сосудорасширяющих (вазопротективных) и сосудосуживающих (вазопатогенных) факторов, связанных с синтезом оксида азота (NO) и эндотелиальной функцией.",
                },
                {
                    "name": "GABR = Аргинин / (Орнитин + Цитруллин)",
                    "value": smart_round(metabolite_data['GABR'], 2),
                    "norm": '0.29 - 1.53',
                    "description": "Отражает активность и баланс обменных процессов в цикле мочевины и доступность аргинина как субстрата для синтеза оксида азота (NO).",
                },
                {
                    "name": "ADMA / (Аденозин + Аргинин)",
                    "value": smart_round(metabolite_data['ADMA/(Adenosin+Arginine)'], 3),
                    "norm": '0.001 - 0.011',
                    "description": "Отражает баланс между сосудосуживающими и воспалительными влияниями (связанными с ADMA) и сосудорасширяющими, защитными эффектами, обусловленными аденозином и аргинином.",
                },
                {
                    "name": "ADMA / Аргинин",
                    "value":  smart_round(1 / metabolite_data['Arg/ADMA'], 3),
                    "norm": '0.001 - 0.011',
                    "description": "Отражает степень метилирования аргинина, приводящего к образованию асимметричного диметиларгинина (ADMA), в сравнении с доступностью аргинина.",
                },
                {
                    "name": "SDMA / Аргинин",
                    "value":  smart_round(metabolite_data['Symmetrical Arg Methylation'], 3),
                    "norm": '0.001 - 0.011',
                    "description": "Отражает степень метилирования аргинина, приводящего к образованию симметричного диметиларгинина (SDMA), в сравнении с доступностью аргинина.",
                },
                {
                    "name": "Сумма диметилированных производных аргинина (ADMA+SDMA)",
                    "value":  smart_round(metabolite_data['Sum of Dimethylated Arg'], 2),
                    "norm": '0.79 - 1.83',
                    "description": "Отражает общий уровень метилированных производных аргинина, связанных с сосудистым воспалением, эндотелиальной дисфункцией и состоянием почечной фильтрации.",
                },
            ]
        
        inflammation_data = [
            {
                "name": "Кинуренин / Триптофан (Kyn/Trp)",
                "value": smart_round(metabolite_data['Kynurenine / Trp'], 3),
                "norm": "0.015 - 0.048",
                "description": "Отражает активность кинуренинового пути обмена триптофана, тесно связанного с воспалением, состоянием иммунной системы и оксидативным стрессом."
            },
            {
                "name": "Триптофан / Кинуренин (Trp/Kyn)",
                "value": smart_round(1 / metabolite_data['Kynurenine / Trp'], 2),
                "norm": "15.00 - 48.80",
                "description": "Является обратным показателем Kyn/Trp и отражает доступность триптофана относительно его воспалительного метаболита кинуренина. Он характеризует запас триптофана и интенсивность его потребления через кинурениновый путь при воспалении и иммунной активации."
            },
            {
                "name": "Trp/(Kyn+QA)",
                "value": smart_round(metabolite_data['Trp/(Kyn+QA)'], 2),
                "norm": "13.29 - 38.78",
                "description": "Это соотношение концентрации триптофана к сумме его метаболитов (кинуренина и хинолиновой кислоты). Он является важным маркером воспалительного и нейротоксического стресса, отражая баланс между доступным триптофаном и продуктами воспалительного катаболизма (психоэмоц. статус)."
            },
            {
                "name": "Кинуренин / Хинолиновая кислота (Kyn/QА)",
                "value": smart_round(metabolite_data['Kyn/Quin'], 2),
                "norm": "0.98 - 7.90",
                "description": "Отражает баланс между промежуточными метаболитами кинуренинового пути: относительно нейтральным по действию кинуренином и нейротоксичным метаболитом хинолиновой кислотой (QА). Этот показатель важен для оценки уровня воспаления, нейротоксичности и оксидативного стресса."
            },
            {
                "name": "Серотонин / Триптофан (Ser/Trp)",
                "value": smart_round(metabolite_data['Serotonin / Trp'], 2),
                "norm": "< 0.03",
                "description": "Отражает эффективность превращения аминокислоты триптофана в нейромедиатор серотонин (5-HT), тем самым характеризуя функциональное состояние серотонинергической системы и баланс эмоционального и психического статуса."
            },
            {
                "name": "Триптамин / Индол-3-уксусная кислота (ТА/IAA)",
                "value": smart_round(metabolite_data['Tryptamine / IAA'], 2),
                "norm": "< 0.13",
                "description": "Отражает баланс в микробном метаболизме триптофана в кишечнике и характеризует состояние кишечной микробиоты и кишечного барьера."
            },
            {
                "name": "TMAO Synthesis = TMAO / (Betaine+C0+Choline)",
                "value": smart_round(metabolite_data['TMAO Synthesis'], 4),
                "norm": "0.0007 - 0.0713",
                "description": "Отражает интенсивность образования триметиламин-N-оксида (TMAO) из его предшественников (бетаина, холина и карнитина), характеризуя активность кишечной микробиоты и риск воспаления и атеросклероза."
            }
        ]

        methylation_data = [
            {
                "name": "Бетаин/Холин (Bet/Chl)",
                "value": smart_round(metabolite_data['Betaine/choline'], 2),
                "norm": "1.14 - 7.57",
                "description": "Отражает активность обмена холина и степень его конверсии в бетаин, характеризуя функциональное состояние печени, эффективность процессов метилирования и риск развития жировой болезни печени (стеатоза)."
            },
            {
                "name": "Диметилглицин / Холин (DMG/Chl)",
                "value": smart_round(metabolite_data['DMG / Choline'], 3),
                "norm": "0.005 - 0.060",
                "description": "Отражает активность пути метилирования, эффективность обмена холина и функционирование печени."
            },
            {
                "name": "Cумма концентраций метионина и таурина (∑(Met + Tau))",
                "value": smart_round(metabolite_data['Methionine + Taurine'], 2),
                "norm": "58.22 - 180.08",
                "description": "Отражает совокупный запас метаболитов, участвующих в антиоксидантной защите, детоксикации, метилировании и регуляции клеточного метаболизма."
            },
            {
                "name": "Met Oxidation = MetSO / Met",
                "value": smart_round(metabolite_data['Met Oxidation'], 4),
                "norm": "< 0.0319",
                "description": "Отражает степень окисления метионина до его окисленного метаболита (метионин-сульфоксида), являясь прямым маркером оксидативного стресса и антиоксидантной защиты организма."
            }
        ]

        energy_metabolism_data = [
            {
                "name": "Глутамин/Глутамат (Gln/Glu)",
                "value": smart_round(metabolite_data['Glutaminase Activity'], 2),
                "norm": "0.44 - 3.66",
                "description": "Отражает баланс между аминокислотами, участвующими в азотном обмене, регуляции энергетического метаболизма и нейротрансмиттерной активности."
            },
            {
                "name": "Пролин / Цитруллин (Pro/Cit)",
                "value": smart_round(metabolite_data['Ratio of Pro to Cit'], 2),
                "norm": "1.87 - 9.09",
                "description": "Отражает баланс аминокислотного обмена, связанного с циклом мочевины, синтезом аргинина и состоянием энергетического и сосудистого метаболизма организма."
            },
            {
                "name": "Цитруллин / Орнитин (Cit/Orn)",
                "value": smart_round(metabolite_data['Cit Synthesis'], 2),
                "norm": "0.18 - 0.97",
                "description": "Отражает эффективность процесса синтеза цитруллина из орнитина в рамках цикла мочевины, а также функциональное состояние печени, сосудистого здоровья и обмена азота."
            },
            {
                "name": "BCAA",
                "value": smart_round(metabolite_data['BCAA'], 2),
                "norm": "299.69 - 531.01",
                "description": "Отражает общий уровень трёх аминокислот: валина (Val), лейцина (Leu) и изолейцина (Ile). Эти аминокислоты важны для оценки энергетического метаболизма, мышечного и печёночного обмена, риска развития метаболического синдрома, диабета и сердечно-сосудистых заболеваний."
            },
            {
                "name": "Индекс Фишера (BCAA/AAAs)",
                "value": smart_round(metabolite_data['BCAA/AAA'], 2),
                "norm": "1.84 - 4.31",
                "description": "Индекс Фишера, отношение аминокислот с разветвлённой цепью к ароматическим аминокислотам - отражает баланс между группами аминокислот и используется для оценки функционального состояния печени, метаболического статуса и риска печёночной энцефалопатии."
            },
            {
                "name": "Фенилаланин / Тирозин (Phe/Tyr)",
                "value": smart_round(metabolite_data['Phe/Tyr'], 2),
                "norm": "0.42 - 1.58",
                "description": "Отражает активность фермента фенилаланин-гидроксилазы, участвующего в превращении фенилаланина в тирозин, и является маркером состояния функции печени и процессов метаболизма аминокислот."
            },
            {
                "name": "Глицин / Серин (Gly/Ser)",
                "value": smart_round(metabolite_data['Glycine/Serine'], 2),
                "norm": "0.59 - 2.72",
                "description": "Отражает баланс между двумя важными аминокислотами, участвующими в процессах метилирования, антиоксидантной защиты, регуляции воспаления и клеточного метаболизма."
            },
            {
                "name": "GSG Index = (Glu/(Ser+Gly))",
                "value": smart_round(metabolite_data['GSG Index'], 4),
                "norm": "0.0844 - 0.66",
                "description": "отражает баланс между возбуждающей нейромедиаторной активностью и антиоксидантной, противовоспалительной защитой организма."
            }
        ]

        mitochondrial_data = [
            {
                "name": "Cоотношение гидрокси- ацилкарнитинов к общим ацилкарнитинам (AC-OHs/ACs)",
                "value": smart_round(metabolite_data['Ratio of AC-OHs to ACs'], 4),
                "norm": "0.0004 - 0.0013",
                "description": "Отражает эффективность β-окисления жирных кислот в митохондриях и характеризует митохондриальную функцию и энергетический обмен организма."
            },
            {
                "name": "Cоотношение среднецепочечных к длинноцепочечным ацилкарнитинам (ССК/СДК)",
                "value": smart_round(metabolite_data['Ratio of Medium-Chain to Long-Chain ACs'], 2),
                "norm": "0.75 - 1.79",
                "description": "Отражает эффективность β-окисления жирных кислот разной длины цепи в митохондриях, а также способность организма эффективно использовать жирные кислоты в качестве источника энергии."
            },
            {
                "name": "Cумма длинноцепочечных ацилкарнитинов (СДК)",
                "value": smart_round(metabolite_data['СДК'], 2),
                "norm": "0.28 - 0.45",
                "description": "отражает общий уровень длинноцепочечных ацилкарнитинов (С14–С18), которые являются промежуточными метаболитами β-окисления жирных кислот в митохондриях."
            },
            {
                "name": "Cумма среднецепочечных ацилкарнитинов (ССК)",
                "value": smart_round(metabolite_data['ССК'], 2),
                "norm": "0.31 - 0.62",
                "description": "отражает общий уровень среднецепочечных ацилкарнитинов (С6–С12), которые являются промежуточными метаболитами β-окисления жирных кислот средней длины в митохондриях."
            },
            {
                "name": "Cумма короткоцепочечных ацилкарнитинов (СКК)",
                "value": smart_round(metabolite_data['СКК'], 2),
                "norm": "4.37 - 12.93",
                "description": "Отражает общий уровень короткоцепочечных ацилкарнитинов (С2–С5), которые являются промежуточными метаболитами β-окисления короткоцепочечных жирных кислот и аминокислотного обмена в митохондриях."
            },
            {
                "name": "C0/(C16+C18)",
                "value": smart_round(metabolite_data['C0/(C16+C18)'], 2),
                "norm": "171.58 - 603.84",
                "description": "Отражает баланс между свободным карнитином и длинноцепочечными ацилкарнитинами, характеризуя способность митохондрий эффективно транспортировать и окислять длинноцепочечные жирные кислоты."
            },
            {
                "name": "(C16+C18-1)/C2",
                # вопрос
                "value": smart_round(metabolite_data['CPT-2 Deficiency (NBS)'], 4),
                "norm": "0.0041 - 0.0182",
                "description": "Отражает баланс между накоплением длинноцепочечных жирных кислот и эффективностью финальной стадии их окисления до ацетилкарнитина (C2), характеризуя общую эффективность митохондриального β-окисления жирных кислот."
            },
            {
                "name": "С2/С0",
                "value": smart_round(metabolite_data['С2/С0'], 2),
                "norm": "0.07 - 0.39",
                "description": "Отражает баланс между ацетилированной формой карнитина (ацетилкарнитином), образующейся в результате энергетического обмена, и свободным карнитином, необходимым для транспорта жирных кислот в митохондрии."
            }
        ]
        
        mytochondrial_data_2 = [
            {
                "name": "Cоотношение короткоцепочечных к длинноцепочечным ацилкарнитинам (СКК/СДК)",
                "value": smart_round(metabolite_data['Ratio of Short-Chain to Long-Chain ACs'], 2),
                "norm": "10.72 - 36.56",
                "description": "Отражает баланс между короткоцепочечными и длинноцепочечными ацилкарнитинами, характеризуя соотношение активности окисления короткоцепочечных жирных кислот и аминокислот к активности окисления длинноцепочечных жирных кислот."
            },
            {
                "name": "Cоотношение короткоцепочечных к среднецепочечным ацилкарнитинам (СКК/ССК)",
                "value": smart_round(metabolite_data['Ratio of Short-Chain to Medium-Chain ACs'], 2),
                "norm": "7.44 - 29.81",
                "description": "Отражает баланс между короткоцепочечными и среднецепочечными ацилкарнитинами и характеризует эффективность митохондриального окисления жирных кислот разной длины цепи, а также баланс аминокислотного обмена."
            },
            {
                "name": "Общая сумма ацилкарнитинов (∑AСs)",
                "value": smart_round(metabolite_data['Sum of ACs'], 2),
                "norm": "5.20 - 13.77",
                "description": "Отражает общий уровень ацилкарнитинов различной длины цепи (коротко-, средне-, длинноцепочечные), являясь интегральным маркером состояния митохондриального β-окисления жирных кислот и аминокислотного обмена."
            },
            {
                "name": "Сумма ацилкарнитинов и свободного карнитина (∑AСs) + С0)",
                "value": smart_round(metabolite_data['Sum of ACs + С0'], 2),
                "norm": "28.39 - 59.97",
                "description": "Отражает общий пул карнитина в организме, включая как свободную форму карнитина (С0), так и все связанные формы (ацилкарнитины различной длины цепи). Является интегральным маркером состояния карнитинового обмена, митохондриальной функции и энергетического метаболизма."
            },
            {
                "name": "Отношение общей суммы ацилкарнитинов к свободному карнитину (∑ACs/C0)",
                "value":  smart_round(metabolite_data['Sum of ACs/C0'], 2),
                "norm": "0.10 - 0.45",
                "description": "Отражает баланс между связанными формами карнитина (ацилкарнитины) и свободным карнитином (С0), являясь важным интегральным индикатором митохондриальной функции, карнитинового обмена и общего энергетического статуса организма."
            }]
        
        fig_phenylalanine_metabolism = plot_metabolite_z_scores(
        metabolite_concentrations={
                "Фенилаланин": metabolite_data["Phenylalanine"],
                "Тирозин": metabolite_data["Tyrosin"],
                "Сумма Leu-Ile": metabolite_data["Summ Leu-Ile"],
                "Валин": metabolite_data["Valine"],
                "BCAA": metabolite_data["BCAA"],
                "BCAA/AAA": metabolite_data["BCAA/AAA"],
                "Phe / Tyr": metabolite_data["Phe/Tyr"],
                "Val / C4": metabolite_data["Val/C4"],
                "(Leu+Ile)/(C3+С5+С5-1+C5-DC)": metabolite_data["(Leu+IsL)/(C3+С5+С5-1+C5-DC)"],
            },
            group_title="Метаболизм фенилаланина"
        )
        
        fig_histidine_metabolism = plot_metabolite_z_scores(
            metabolite_concentrations={
                "Гистидин": metabolite_data["Histidine"],
                "Метилгистидин": metabolite_data["Methylhistidine"],
                "Треонин": metabolite_data["Threonine"],
                "Глицин": metabolite_data["Glycine"],
                "DMG": metabolite_data["DMG"],
                "Серин": metabolite_data["Serine"],
                "Лизин": metabolite_data["Lysine"], 
                "Глутамат": metabolite_data["Glutamic acid"],
                "Глутамин": metabolite_data["Glutamine"],
                "Глутамин / Глутамат": metabolite_data["Glutamine/Glutamate"],
                "Глицин / Серин": metabolite_data["Glycine/Serine"],
                "Индекс GSG": metabolite_data["GSG Index"],
                "Карнозин": metabolite_data["Carnosine"],
            },
            group_title="Метаболизм гистидина"
        )
        
        # Methionine Metabolism
        fig_methionine_metabolism = plot_metabolite_z_scores(
            metabolite_concentrations={
                "Метионин": metabolite_data["Methionine"],
                "Метионин сульфоксид": metabolite_data["Methionine-Sulfoxide"],
                "Таурин": metabolite_data["Taurine"],
                "Бетаин": metabolite_data["Betaine"],
                "Холин": metabolite_data["Choline"],
                "TMAO": metabolite_data["TMAO"],
                "Бетаин / Холин": metabolite_data["Betaine/choline"],
                "Метионин + Таурин": metabolite_data["Methionine + Taurine"],
                "Окисление метионина": metabolite_data["Met Oxidation"],
                "Синтез TMAO": metabolite_data["TMAO Synthesis"],
                "DMG / Холин": metabolite_data["DMG / Choline"],
            },
            group_title="Метаболизм метионина"
        )

        # Kynurenine Pathway
        fig_kynurenine_pathway = plot_metabolite_z_scores(
            metabolite_concentrations={
                "Триптофан": metabolite_data["Tryptophan"],
                "Кинуренин": metabolite_data["Kynurenine"],
                "Антранилловая кислота": metabolite_data["Antranillic acid"],
                "Хинолиновая кислота": metabolite_data["Quinolinic acid"],
                "Ксантуреновая кислота": metabolite_data["Xanthurenic acid"],
                "Кинуреновая кислота": metabolite_data["Kynurenic acid"],
                "Kyn / Trp": metabolite_data["Kynurenine / Trp"],
                "Trp / (Kyn+QA)": metabolite_data["Trp/(Kyn+QA)"],
                "Kyn / Quin": metabolite_data["Kyn/Quin"],
            },
            group_title="Кинурениновый путь"
        )

        # Serotonin Pathway
        fig_serotonin_pathway = plot_metabolite_z_scores(
            metabolite_concentrations={
                "Серотонин": metabolite_data["Serotonin"],
                "HIAA": metabolite_data["HIAA"],
                "5-гидрокситриптофан": metabolite_data["5-hydroxytryptophan"],
                "Ser / Trp": metabolite_data["Serotonin / Trp"],
            },
            group_title="Серотониновый путь"
        )

        # Indole Pathway
        fig_indole_pathway = plot_metabolite_z_scores(
            metabolite_concentrations={
                "3-индолуксусная кислота": metabolite_data["Indole-3-acetic acid"],
                "3-индолмолочная кислота": metabolite_data["Indole-3-lactic acid"],
                "3-индолкарбоксальдегид": metabolite_data["Indole-3-carboxaldehyde"],
                "3-индолпропионовая кислота": metabolite_data["Indole-3-propionic acid"],
                "3-индолмасляная": metabolite_data["Indole-3-butyric"],
                "Триптамин": metabolite_data["Tryptamine"],
                "TA / IAA": metabolite_data["Tryptamine / IAA"],
            },
            group_title="Индоловый путь"
        )

        # Arginine Metabolism
        fig_arginine_metabolism = plot_metabolite_z_scores(
            metabolite_concentrations={
                "Пролин": metabolite_data["Proline"],
                "Гидроксипролин": metabolite_data["Hydroxyproline"],
                "ADMA": metabolite_data["ADMA"],
                "NMMA": metabolite_data["NMMA"],
                "SDMA": metabolite_data["TotalDMA (SDMA)"],
                "Гомоаргинин": metabolite_data["Homoarginine"],
                "Аргинин": metabolite_data["Arginine"],
                "Цитруллин": metabolite_data["Citrulline"],
                "Орнитин": metabolite_data["Ornitine"],
                "Аспарагин": metabolite_data["Asparagine"],
                "Аспарагиновая кислота": metabolite_data["Aspartic acid"],
                "Креатинин": metabolite_data["Creatinine"],
                "Arg / ADMA": metabolite_data["Arg/ADMA"],
                "(Arg + HomoArg)/ADMA": metabolite_data["(Arg+HomoArg)/ADMA"],
                "Arg/Orn+Cit": metabolite_data["Arg/Orn+Cit"],
                "ADMA/(Adenosin + Arg)": metabolite_data["ADMA/(Adenosin+Arginine)"],
                "SDMA / Arg": metabolite_data["Symmetrical Arg Methylation"],
                "SDMA + ADMA": metabolite_data["Sum of Dimethylated Arg"],
                "Pro / Cit": metabolite_data["Ratio of Pro to Cit"],
                "Синтез Cit": metabolite_data["Cit Synthesis"],
            },
            group_title="Метаболизм аргинина"
        )

        # Acylcarnitine Metabolism (ratios)
        fig_acylcarnitine_ratios = plot_metabolite_z_scores(
            metabolite_concentrations={
                "Аланин": metabolite_data["Alanine"],
                "C0": metabolite_data["C0"],
                "AC-OHs / ACs": metabolite_data["Ratio of AC-OHs to ACs"],
                "СДК": metabolite_data["СДК"],
                "ССК": metabolite_data["ССК"],
                "СКК": metabolite_data["СКК"],
                "C0/(C16+C18)": metabolite_data["C0/(C16+C18)"],
                "(C16+C18-1)/C2": metabolite_data["CPT-2 Deficiency (NBS)"],
                "С2/С0": metabolite_data["С2/С0"],
                "СКК/СДК": metabolite_data["Ratio of Short-Chain to Long-Chain ACs"],
                "ССК/СДК": metabolite_data["Ratio of Medium-Chain to Long-Chain ACs"],
                "СКК/ССК": metabolite_data["Ratio of Short-Chain to Medium-Chain ACs"],
                "Сумма ACs": metabolite_data["Sum of ACs"],
                "Сумма ACs + С0": metabolite_data["Sum of ACs + С0"],
                "Сумма ACs/C0": metabolite_data["Sum of ACs/C0"],
            },
            group_title="Метаболизм ацилкарнитинов (соотношения)"
        )

        # Short-chain Acylcarnitines
        fig_short_chain_acyl = plot_metabolite_z_scores(
            metabolite_concentrations={
                "C2": metabolite_data["C2"],
                "C3": metabolite_data["C3"],
                "C4": metabolite_data["C4"],
                "C5": metabolite_data["C5"],
                "C5-1": metabolite_data["C5-1"],
                "C5-DC": metabolite_data["C5-DC"],
                "C5-OH": metabolite_data["C5-OH"],
            },
            group_title="Короткоцепочечные ацилкарнитины"
        )

        # Medium-chain Acylcarnitines
        fig_medium_chain_acyl = plot_metabolite_z_scores(
            metabolite_concentrations={
                "C6": metabolite_data["C6"],
                "C6-DC": metabolite_data["C6-DC"],
                "C8": metabolite_data["C8"],
                "C8-1": metabolite_data["C8-1"],
                "C10": metabolite_data["C10"],
                "C10-1": metabolite_data["C10-1"],
                "C10-2": metabolite_data["C10-2"],
                "C12": metabolite_data["C12"],
                "C12-1": metabolite_data["C12-1"],
            },
            group_title="Среднецепочечные ацилкарнитины"
        )

        # Long-chain Acylcarnitines
        fig_long_chain_acyl = plot_metabolite_z_scores(
            metabolite_concentrations={
                "C14": metabolite_data["C14"],
                "C14-1": metabolite_data["C14-1"],
                "C14-2": metabolite_data["C14-2"],
                "C14-OH": metabolite_data["C14-OH"],
                "C16": metabolite_data["C16"],
                "C16-1": metabolite_data["C16-1"],
                "C16-1-OH": metabolite_data["C16-1-OH"],
                "C16-OH": metabolite_data["C16-OH"],
                "C18": metabolite_data["C18"],
                "C18-1": metabolite_data["C18-1"],
                "C18-1-OH": metabolite_data["C18-1-OH"],
                "C18-2": metabolite_data["C18-2"],
                "C18-OH": metabolite_data["C18-OH"],
            },
            group_title="Длинноцепочечные ацилкарнитины"
        )

        # # Other Metabolites
        fig_other_metabolites = plot_metabolite_z_scores(
            metabolite_concentrations={
                "Пантотеновая кислота": metabolite_data["Pantothenic"],
                "Рибофлавин": metabolite_data["Riboflavin"],
                "Мелатонин": metabolite_data["Melatonin"],
                "Уридин": metabolite_data["Uridine"],
                "Аденозин": metabolite_data["Adenosin"],
                "Цитидин": metabolite_data["Cytidine"],
                "Кортизол": metabolite_data["Cortisol"],
                "Гистамин": metabolite_data["Histamine"],
            },
            group_title="Другие метаболиты"
        )
        
        def create_layout():
            """Your complete existing layout using all the variables"""
            return html.Div([
            # 1 страница
            html.Div([
                html.Div([
                    html.Img(src=app.get_asset_url('logo-sechenov.png'), style={'width':'100%','object-fit':'containt'})
                ],style={'width':'25%','height':'auto', 'margin':'0px', 'display':'flex', 'justify-content':'left', 'align-items':'center'}),
                html.Div([
                    html.Img(src=app.get_asset_url('logo_inst_tox.png'), style={'width':'100%','object-fit':'containt'})
                ],style={'width':'20%','height':'auto', 'margin':'0px', 'display':'flex', 'justify-content':'left', 'align-items':'center'}),
                                
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
                    ],style={'margin-top':'10px','margin-left':'35px','color':'black','font-family':'Calibri','font-size':'15px'}),
                    
                ],style={'width':'60%','height':'100px', 'color':'white','margin':'0px','background-image':'url("/assets/rHeader_2.png")','background-repeat':'no-repeat','background-size':'100%','background-position':'center'}),
            ], style={'display':'flex', 'justify-content':'right','width':'100%','height':'100px','margin-bottom':'10px'}),
            html.Div([
                html.H2(children='Панорамный метаболомный обзор', style={'textAlign':'center','margin':'0px'}),]
                     , style={'width':'100%','background-color':'#2563eb','border-radius':'5px 5px 0px 0px',"padding":'5px', 'color':'white','font-family':'Calibri','margin':'0px'}),

            html.Img(
                    src=app.get_asset_url('radial_diagram.png'),
                    style={
                        'height': '390px',
                        'width': 'auto',  # This maintains aspect ratio
                        'max-width': '100%',  # Ensures it doesn't overflow container
                        'object-fit': 'contain',  # Prevents distortion
                        'margin-top': '12px',
                        'margin-bottom': '2px',
                        'display': 'block',  # Ensures proper margin handling
                        'margin-left': 'auto',
                        'margin-right': 'auto'  # Centers the image
                    }
                ),
            #  Make table with columns Балл and Интерпретация
                        html.Div(
    style={
        'fontFamily': 'Calibri',
        'width': 'fit-content', 'height': 'fit-content',
        'margin': '0 auto',
        'borderRadius': '5px',
        'overflow': 'hidden'
    },
    children=[
        # Row 1
        html.Div(
            style={
                'display': 'flex',
                'marginBottom': '2px'
            },
            children=[
                html.Span(
                    "9-10",
                    style={
                        'backgroundColor': "#10b9815b",
                        'border': '2px solid #12a070',
                        'borderRadius': '3px',
                        'padding': '0px 10px',
                        'fontSize': '0.7rem',
                        'fontWeight': 'bold',
                        'color': "#12a070",
                        'minWidth': '50px',
                        'textAlign': 'center'
                    }
                ),
                html.Span(
                    "Метаболческая ось в хорошем или оптимальном состоянии",
                    style={
                        'borderLeft': 'none',
                        'padding': '0px 10px',
                        'fontSize': '0.7rem',
                        'color': "#404547",
                        'flexGrow': '1'
                    }
                )
            ]
        ),
        # Row 2
        html.Div(
            style={
                'display': 'flex',
                'marginBottom': '2px'
            },
            children=[
                html.Span(
                    "7-8",
                    style={
                        'backgroundColor': "#a0d04772",
                        'border': '2px solid #79a822',
                        'borderRadius': '3px',
                        'padding': '0px 10px',
                        'fontSize': '0.7rem',
                        'fontWeight': 'bold',
                        'color': "#79a822",
                        'minWidth': '50px',
                        'textAlign': 'center'
                    }
                ),
                html.Span(
                    "Незначительные отклонения, компенсаторные механизмы работают",
                    style={
                        'borderLeft': 'none',
                        'padding': '0px 10px',
                        'fontSize': '0.7rem',
                        'color': "#404547",
                        'flexGrow': '1'
                    }
                )
            ]
        ),
        # Row 3
        html.Div(
            style={
                'display': 'flex',
                'marginBottom': '2px'
            },
            children=[
                html.Span(
                    "5-6",
                    style={
                        'backgroundColor': 'rgba(255,225,175,255)',
                        'border': '2px solid #ff8c00',
                        'borderRadius': '3px',
                        'padding': '0px 10px',
                        'fontSize': '0.7rem',
                        'fontWeight': 'bold',
                        'color': "#e07d04",
                        'minWidth': '50px',
                        'textAlign': 'center'
                    }
                ),
                html.Span(
                    "Умеренные нарушения — не критично, но уже требует коррекции",
                    style={
                        'borderLeft': 'none',
                        'padding': '0px 10px',
                        'fontSize': '0.7rem',
                        'color': "#404547",
                        'flexGrow': '1'
                    }
                )
            ]
        ),
        # Row 4
        html.Div(
            style={
                'display': 'flex',
                'marginBottom': '2px'
            },
            children=[
                html.Span(
                    "3-4",
                    style={
                        'backgroundColor': 'rgb(234, 102, 25, 0.3)',
                        'border': '2px solid #e67c30',
                        'borderRadius': '3px',
                        'padding': '0px 10px',
                        'fontSize': '0.7rem',
                        'fontWeight': 'bold',
                        'color': "#c7631b",
                        'minWidth': '50px',
                        'textAlign': 'center'
                    }
                ),
                html.Span(
                    "Существенные изменения — снижен резерв, хроническая нагрузка",
                    style={
                        'borderLeft': 'none',
                        'padding': '0px 10px',
                        'fontSize': '0.7rem',
                        'color': "#404547",
                        'flexGrow': '1'
                    }
                )
            ]
        ),
        # Row 5
        html.Div(
            style={
                'display': 'flex'
            },
            children=[
                html.Span(
                    "1-2",
                    style={
                        'backgroundColor': 'rgb(234, 25, 25, 0.3)',
                        'border': '2px solid #d9534f',
                        'borderRadius': '3px',
                        'padding': '0px 10px',
                        'fontSize': '0.7rem',
                        'fontWeight': 'bold',
                        'color': "#b63e3a",
                        'minWidth': '50px',
                        'textAlign': 'center'
                    }
                ),
                html.Span(
                    "Выраженные патологии, декомпенсация, высокий риск",
                    style={
                        'borderLeft': 'none',
                        'padding': '0px 10px',
                        'fontSize': '0.7rem',
                        'color': "#2C2C2C",
                        'flexGrow': '1'
                    }
                )
            ]
        )
    ]
),
            # Plot risk_scores table
            html.Div([
                html.Div([
                    html.Div([
                        html.P('1. Метаболическая детоксикация', style={'margin': '0px', 'margin-bottom': '1px', 'font-weight': 'bold', 'color': '#404547'}),
                        html.Div([
                            html.Div([
                                html.Div([], style={
                                    'width': f"{risk_scores.loc[risk_scores['Группа риска'] == 'Метаболическая детоксикация', 'Риск-скор'].values[0] * 10}%",
                                    'background-color': get_color_under_normal_dist(
                                        100-(risk_scores.loc[risk_scores['Группа риска'] == 'Метаболическая детоксикация', 'Риск-скор'].values[0] * 10)
                                    ),
                                    'border-radius': '2px',
                                    'height': '13px',
                                    'line-height': 'normal',
                                    'display': 'inline-block',
                                    'vertical-align': 'center',
                                }),
                            ], style={'display': 'flex', 'align-self': 'center','width': '70px', 'height': '13px','line-height': 'normal', 'border-radius': '2px','background-color':  'lightgrey', 'margin-left':'5px', 'margin-right':'5px'}),
                            html.B(
                                f"{risk_scores.loc[risk_scores['Группа риска'] == 'Метаболическая детоксикация', 'Риск-скор'].values[0]} из 10",
                                style={'margin': '0px', 'color': '#404547'}
                            )
                        ], style ={'display': 'flex', 'flex-direction': 'row', 'flex-wrap': 'nowrap'})
                    ],  style={
                        'color': 'black',
                        'font-family': 'Calibri',
                        'font-size': '16px',
                        'margin': '0px',
                        'display': 'flex',
                        'justify-content': 'space-between',
                        'margin-bottom': '0px',
                        'margin-top': '10px'
                    }),
                    
                    html.Div([], style={
                        'width': "100%",
                        'background-color': "#2563eb",
                        'height': '2px',
                        'line-height': 'normal',
                        'display': 'inline-block',
                        'vertical-align': 'center',
                        'margin-bottom':'2px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 - amiac_detox_score}%',
                                'background-color': get_color_under_normal_dist(amiac_detox_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center',
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px', 'margin-right': '5px'}),
                        html.Div([
                            html.P('Аммиачная детоксикация', style={
                                'margin': '0px',
                                'font-size': '14px',
                                'font-family': 'Calibri',
                                'height': '18px',
                                'margin-left': '3px'
                            })
                        ], style={'width': '75%'}),
                    ], style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'width': '100%',
                        'height': '18px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 - oxidative_stress_score}%',
                                'background-color': get_color_under_normal_dist(oxidative_stress_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center',
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px', 'margin-right': '5px'}),
                        html.Div([
                            html.P('Оксидативная нагрузка', style={
                                'margin': '0px',
                                'font-size': '14px',
                                'font-family': 'Calibri',
                                'height': '18px',
                                'margin-left': '3px'
                            })
                        ], style={'width': '75%'}),
                    ], style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'width': '100%',
                        'height': '18px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 -  nitrogen_toxic_score}%',
                                'background-color': get_color_under_normal_dist(nitrogen_toxic_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px', 'margin-right': '5px'}),
                        html.Div([
                            html.P('Азотистые токсины', style={
                                'margin': '0px',
                                'font-size': '14px',
                                'font-family': 'Calibri',
                                'height': '18px',
                                'margin-left': '3px'
                            })
                        ], style={'width': '75%'}),
                    ], style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'width': '100%',
                        'height': '18px'
                    }),
                    
                    html.Div([
                        html.P('3. Воспаление и иммунитет', style={'margin': '0px', 'margin-bottom': '1px', 'color': '#404547'}),
                        html.Div([
                            html.Div([
                                html.Div([], style={
                                    'width': f"{risk_scores.loc[risk_scores['Группа риска'] == 'Воспаление и иммунитет', 'Риск-скор'].values[0] * 10}%",
                                    'background-color': get_color_under_normal_dist(
                                        100-(risk_scores.loc[risk_scores['Группа риска'] == 'Воспаление и иммунитет', 'Риск-скор'].values[0] * 10)
                                    ),
                                    'border-radius': '2px',
                                    'height': '13px',
                                    'line-height': 'normal',
                                    'display': 'inline-block',
                                    'vertical-align': 'center',
                                }),
                            ], style={'display': 'flex', 'align-self': 'center','width': '70px', 'height': '13px','line-height': 'normal', 'border-radius': '2px','background-color':  'lightgrey', 'margin-left':'5px', 'margin-right':'5px'}),
                            html.B(
                                f"{risk_scores.loc[risk_scores['Группа риска'] == 'Воспаление и иммунитет', 'Риск-скор'].values[0]} из 10",
                                style={'margin': '0px', 'color': '#404547'}
                            )
                        ], style ={'display': 'flex', 'flex-direction': 'row', 'flex-wrap': 'nowrap'})
                    ],  style={
                        'color': 'black',
                        'font-family': 'Calibri',
                        'font-weight': 'bold',
                        'font-size': '16px',
                        'margin': '0px',
                        'display': 'flex',
                        'justify-content': 'space-between',
                        'margin-bottom': '0px',
                        'margin-top': '30px'
                    }),
                    
                    html.Div([], style={
                        'width': "100%",
                        'background-color': "#2563eb",
                        'height': '2px',
                        'line-height': 'normal',
                        'display': 'inline-block',
                        'vertical-align': 'center',
                        'margin-bottom':'2px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 -  ido_path_tryptophan_score}%',
                                'background-color': get_color_under_normal_dist(ido_path_tryptophan_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px', 'margin-right': '5px'}),
                        html.Div([
                            html.P('IDO-путь / триптофан', style={
                                'margin': '0px',
                                'font-size': '14px',
                                'font-family': 'Calibri',
                                'height': '18px',
                                'margin-left': '3px'
                            })
                        ], style={'width': '75%'}),
                    ], style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'width': '100%',
                        'height': '18px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 -  neuromediators_score}%',
                                'background-color': get_color_under_normal_dist(neuromediators_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px', 'margin-right': '5px'}),
                        html.Div([
                            html.P('Нейромедиаторы', style={
                                'margin': '0px',
                                'font-size': '14px',
                                'font-family': 'Calibri',
                                'height': '18px',
                                'margin-left': '3px'
                            })
                        ], style={'width': '75%'}),
                    ], style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'width': '100%',
                        'height': '18px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 - indols_phenols_score}%',
                                'background-color': get_color_under_normal_dist(indols_phenols_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px', 'margin-right': '5px'}),
                        html.Div([
                            html.P('Индолы и фенолы', style={
                                'margin': '0px',
                                'font-size': '14px',
                                'font-family': 'Calibri',
                                'height': '18px',
                                'margin-left': '3px'
                            })
                        ], style={'width': '75%'}),
                    ], style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'width': '100%',
                        'height': '18px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 - general_stress_immune_score}%',
                                'background-color': get_color_under_normal_dist(general_stress_immune_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px', 'margin-right': '5px'}),
                        html.Div([
                            html.P('Общий стресс / иммунитет', style={
                                'margin': '0px',
                                'font-size': '14px',
                                'font-family': 'Calibri',
                                'height': '18px',
                                'margin-left': '3px'
                            })
                        ], style={'width': '75%'}),
                    ], style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'width': '100%',
                        'height': '18px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 -  complex_index}%',
                                'background-color': get_color_under_normal_dist(complex_index),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px', 'margin-right': '5px'}),
                        html.Div([
                            html.P('Комплексный индекс', style={
                                'margin': '0px',
                                'font-size': '14px',
                                'font-family': 'Calibri',
                                'height': '18px',
                                'margin-left': '3px'
                            })
                        ], style={'width': '75%'}),
                    ], style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'width': '100%',
                        'height': '18px'
                    }),
                    
                ], style={'width': '48%', 'height': 'fit-content'}),
                
            # колонка 222222222222222222222222222222222
            
            html.Div([
                    html.Div([
                        html.P('2. Здоровье митохондрий', style={'margin': '0px', 'margin-bottom': '1px','font-weight': 'bold', 'color': '#404547'}),
                        html.Div([
                            html.Div([
                                html.Div([], style={
                                    'width': f"{risk_scores.loc[risk_scores['Группа риска'] == 'Здоровье митохондрий', 'Риск-скор'].values[0] * 10}%",
                                    'background-color': get_color_under_normal_dist(
                                        100-(risk_scores.loc[risk_scores['Группа риска'] == 'Здоровье митохондрий', 'Риск-скор'].values[0] * 10)
                                    ),
                                    'border-radius': '2px',
                                    'height': '13px',
                                    'line-height': 'normal',
                                    'display': 'inline-block',
                                    'vertical-align': 'center',
                                }),
                            ], style={'display': 'flex', 'align-self': 'center','width': '70px', 'height': '13px','line-height': 'normal', 'border-radius': '2px','background-color':  'lightgrey', 'margin-left':'5px', 'margin-right':'5px'}),
                            html.B(
                                f"{risk_scores.loc[risk_scores['Группа риска'] == 'Здоровье митохондрий', 'Риск-скор'].values[0]} из 10",
                                style={'margin': '0px', 'color': '#404547'}
                            )
                        ], style ={'display': 'flex', 'flex-direction': 'row', 'flex-wrap': 'nowrap'})
                    ],  style={
                        'color': 'black',
                        'font-family': 'Calibri',
                        'font-size': '16px',
                        'margin': '0px',
                        'display': 'flex',
                        'justify-content': 'space-between',
                        'margin-bottom': '0px',
                        'margin-top': '10px'
                    }),
                    
                    html.Div([], style={
                        'width': "100%",
                        'background-color': "#2563eb",
                        'height': '2px',
                        'line-height': 'normal',
                        'display': 'inline-block',
                        'vertical-align': 'center',
                        'margin-bottom':'2px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 - energy_exchange_carnitine_score}%',
                                'background-color': get_color_under_normal_dist(energy_exchange_carnitine_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px', 'margin-right': '5px'}),
                        html.Div([
                            html.P('Энергетический обмен', style={
                                'margin': '0px',
                                'font-size': '14px',
                                'font-family': 'Calibri',
                                'height': '18px',
                                'margin-left': '3px'
                            })
                        ], style={'width': '75%'}),
                    ], style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'width': '100%',
                        'height': '18px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 -  mitochondrial_score}%',
                                'background-color': get_color_under_normal_dist(mitochondrial_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px', 'margin-right': '5px'}),
                        html.Div([
                            html.P('β-окисление / жирные кислоты', style={
                                'margin': '0px',
                                'font-size': '14px',
                                'font-family': 'Calibri',
                                'height': '18px',
                                'margin-left': '3px'
                            })
                        ], style={'width': '75%'}),
                    ], style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'width': '100%',
                        'height': '18px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 -  antoxidant_system}%',
                                'background-color': get_color_under_normal_dist(antoxidant_system),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px', 'margin-right': '5px'}),
                        html.Div([
                            html.P('Антиоксидантная защита', style={
                                'margin': '0px',
                                'font-size': '14px',
                                'font-family': 'Calibri',
                                'height': '18px',
                                'margin-left': '3px'
                            })
                        ], style={'width': '75%'}),
                    ], style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'width': '100%',
                        'height': '18px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 -   complex_index}%',
                                'background-color': get_color_under_normal_dist(complex_index),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px', 'margin-right': '5px'}),
                        html.Div([
                            html.P('Митохондриальная нейросвязь', style={
                                'margin': '0px',
                                'font-size': '14px',
                                'font-family': 'Calibri',
                                'height': '18px',
                                'margin-left': '3px'
                            })
                        ], style={'width': '75%'}),
                    ], style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'width': '100%',
                        'height': '18px'
                    }),
                     html.Div([
                         
                        html.Div([
                        html.P('4.', style={'margin': '0px', 'margin-bottom': '1px', 'font-weight': 'bold', 'margin-right': '5px', 'color': '#404547'} ),
                        html.P('Метаболическая адаптация и стрессоустойчивость', style={'margin': '0px', 'margin-bottom': '1px', 'width':'200px', 'font-weight': 'bold', 'color': '#404547'}),
                        ], style={'display': 'flex', 'justify-content': 'left', 'width': 'auto', 'height': '18px'}),
                        
                        html.Div([
                            html.Div([
                                html.Div([], style={
                                    'width': f"{risk_scores.loc[risk_scores['Группа риска'] == 'Метаболическая адаптация и стрессоустойчивость', 'Риск-скор'].values[0] * 10}%",
                                    'background-color': get_color_under_normal_dist(
                                        100-(risk_scores.loc[risk_scores['Группа риска'] == 'Метаболическая адаптация и стрессоустойчивость', 'Риск-скор'].values[0] * 10)
                                    ),
                                    'border-radius': '2px',
                                    'height': '13px',
                                    'line-height': 'normal',
                                    'display': 'inline-block',
                                    'vertical-align': 'center',
                                }),
                            ], style={'display': 'flex', 'align-self': 'center','width': '70px', 'height': '13px','line-height': 'normal', 'border-radius': '2px','background-color':  'lightgrey', 'margin-left':'5px', 'margin-right':'5px'}),
                            html.B(
                                f"{risk_scores.loc[risk_scores['Группа риска'] == 'Метаболическая адаптация и стрессоустойчивость', 'Риск-скор'].values[0]} из 10",
                                style={'margin': '0px', 'color': '#404547'}
                            )
                        ], style ={'display': 'flex', 'flex-direction': 'row', 'flex-wrap': 'nowrap', 'align-items': 'center'})
                    ],  style={
                        'color': 'black',
                        'font-family': 'Calibri',
                        'font-size': '16px',
                        'margin': '0px',
                        'display': 'flex',
                        'justify-content': 'space-between',
                        'margin-bottom': '15px',
                        'margin-top': '10px'
                    }),
                    
                    
                    html.Div([], style={
                        'width': "100%",
                        'background-color': "#2563eb",
                        'height': '2px',
                        'line-height': 'normal',
                        'display': 'inline-block',
                        'vertical-align': 'center',
                        'margin-bottom':'2px'
                    }),
                    
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 - energy_exchange_score}%',
                                'background-color': get_color_under_normal_dist(energy_exchange_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px', 'margin-right': '5px'}),
                        html.Div([
                            html.P('Энергетический обмен', style={
                                'margin': '0px',
                                'font-size': '14px',
                                'font-family': 'Calibri',
                                'height': '18px',
                                'margin-left': '3px'
                            })
                        ], style={'width': '75%'}),
                    ], style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'width': '100%',
                        'height': '18px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 -  neuroadaptation_score}%',
                                'background-color': get_color_under_normal_dist(neuroadaptation_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px', 'margin-right': '5px'}),
                        html.Div([
                            html.P('Нейро-адаптация', style={
                                'margin': '0px',
                                'font-size': '14px',
                                'font-family': 'Calibri',
                                'height': '18px',
                                'margin-left': '3px'
                            })
                        ], style={'width': '75%'}),
                    ], style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'width': '100%',
                        'height': '18px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 -  stress_aminoacid_score}%',
                                'background-color': get_color_under_normal_dist(stress_aminoacid_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px', 'margin-right': '5px'}),
                        html.Div([
                            html.P('Стресс-аминокислоты', style={
                                'margin': '0px',
                                'font-size': '14px',
                                'font-family': 'Calibri',
                                'height': '18px',
                                'margin-left': '3px'
                            })
                        ], style={'width': '75%'}),
                    ], style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'width': '100%',
                        'height': '18px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 -  metochondria_creatinine_score}%',
                                'background-color': get_color_under_normal_dist(metochondria_creatinine_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px', 'margin-right': '5px'}),
                        html.Div([
                            html.P('Митохондрии и креатин', style={
                                'margin': '0px',
                                'font-size': '14px',
                                'font-family': 'Calibri',
                                'height': '18px',
                                'margin-left': '3px'
                            })
                        ], style={'width': '75%'}),
                    ], style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'width': '100%',
                        'height': '18px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 -  glutamate_exchange_score}%',
                                'background-color': get_color_under_normal_dist(glutamate_exchange_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px', 'margin-right': '5px'}),
                        html.Div([
                            html.P('Глутамат-глутаминовая ось', style={
                                'margin': '0px',
                                'font-size': '14px',
                                'font-family': 'Calibri',
                                'height': '18px',
                                'margin-left': '3px'
                            })
                        ], style={'width': '75%'}),
                    ], style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'width': '100%',
                        'height': '18px'
                    }),
                    
                ], style={'width': '48%', 'height': 'fit-content'}),
            
            ], style={
                'display': 'flex',
                'justify-content': 'space-between',
                'height': 'fit-content',
                'margin-top': '5px'}),
            
            # Plot risk_scores table
            html.Div([
                html.Div([
                    
                    html.Div([
                        html.P('5. Витаминный статус', style={'margin': '0px', 'margin-bottom': '1px', 'font-weight': 'bold', 'color': '#404547'}),
                        html.Div([
                            html.Div([
                                html.Div([], style={
                                    'width': f"{risk_scores.loc[risk_scores['Группа риска'] == 'Витаминный статус', 'Риск-скор'].values[0] * 10}%",
                                    'background-color': get_color_under_normal_dist(
                                        100-(risk_scores.loc[risk_scores['Группа риска'] == 'Витаминный статус', 'Риск-скор'].values[0] * 10)
                                    ),
                                    'border-radius': '2px',
                                    'height': '13px',
                                    'line-height': 'normal',
                                    'display': 'inline-block',
                                    'vertical-align': 'center',
                                }),
                            ], style={'display': 'flex', 'align-self': 'center','width': '70px', 'height': '13px','line-height': 'normal', 'border-radius': '2px','background-color':  'lightgrey', 'margin-left':'5px', 'margin-right':'5px'}),
                            html.B(
                                f"{risk_scores.loc[risk_scores['Группа риска'] == 'Витаминный статус', 'Риск-скор'].values[0]} из 10",
                                style={'margin': '0px', 'color': '#404547'}
                            )
                        ], style ={'display': 'flex', 'flex-direction': 'row', 'flex-wrap': 'nowrap'})
                    ],  style={
                        'color': 'black',
                        'font-family': 'Calibri',
                        'font-size': '16px',
                        'margin': '0px',
                        'display': 'flex',
                        'justify-content': 'space-between',
                        'margin-bottom': '0px',
                        'margin-top': '10px'
                    }),
                    
                    html.Div([], style={
                        'width': "100%",
                        'background-color': "#2563eb",
                        'height': '2px',
                        'line-height': 'normal',
                        'display': 'inline-block',
                        'vertical-align': 'center',
                        'margin-bottom':'2px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 -  vitamine_b2_score}%',
                                'background-color': get_color_under_normal_dist(vitamine_b2_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px', 'margin-right': '5px'}),
                        html.Div([
                            html.P('Витамин B2 (рибофлавин)', style={
                                'margin': '0px',
                                'font-size': '14px',
                                'font-family': 'Calibri',
                                'height': '18px',
                                'margin-left': '3px'
                            })
                        ], style={'width': '75%'}),
                    ], style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'width': '100%',
                        'height': '18px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 -  vitamine_b5_score}%',
                                'background-color': get_color_under_normal_dist(vitamine_b5_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px', 'margin-right': '5px'}),
                        html.Div([
                            html.P('Витамин B5 (пантотенат)', style={
                                'margin': '0px',
                                'font-size': '14px',
                                'font-family': 'Calibri',
                                'height': '18px',
                                'margin-left': '3px'
                            })
                        ], style={'width': '75%'}),
                    ], style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'width': '100%',
                        'height': '18px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 -  vitamine_b6_score}%',
                                'background-color': get_color_under_normal_dist(vitamine_b6_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px', 'margin-right': '5px'}),
                        html.Div([
                            html.P('Витамин B6', style={
                                'margin': '0px',
                                'font-size': '14px',
                                'font-family': 'Calibri',
                                'height': '18px',
                                'margin-left': '3px'
                            })
                        ], style={'width': '75%'}),
                    ], style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'width': '100%',
                        'height': '18px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 -  vitamine_b9_b12_score}%',
                                'background-color': get_color_under_normal_dist(vitamine_b9_b12_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px', 'margin-right': '5px'}),
                        html.Div([
                            html.P('Витамин B9 / B12', style={
                                'margin': '0px',
                                'font-size': '14px',
                                'font-family': 'Calibri',
                                'height': '18px',
                                'margin-left': '3px'
                            })
                        ], style={'width': '75%'}),
                    ], style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'width': '100%',
                        'height': '18px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 -  vitamine_b3_nad_score}%',
                                'background-color': get_color_under_normal_dist(vitamine_b3_nad_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px', 'margin-right': '5px'}),
                        html.Div([
                            html.P('Витамин B3 / NAD+', style={
                                'margin': '0px',
                                'font-size': '14px',
                                'font-family': 'Calibri',
                                'height': '18px',
                                'margin-left': '3px'
                            })
                        ], style={'width': '75%'}),
                    ], style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'width': '100%',
                        'height': '18px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 -  serum_aminoacids_score}%',
                                'background-color': get_color_under_normal_dist(serum_aminoacids_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px', 'margin-right': '5px'}),
                        html.Div([
                            html.P('Серосодержащие аминокислоты', style={
                                'margin': '0px',
                                'font-size': '14px',
                                'font-family': 'Calibri',
                                'height': '18px',
                                'margin-left': '3px'
                            })
                        ], style={'width': '75%'}),
                    ], style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'width': '100%',
                        'height': '18px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 - energy_exchange_score}%',
                                'background-color': get_color_under_normal_dist(energy_exchange_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px', 'margin-right': '5px'}),
                        html.Div([
                            html.P('Энергетический баланс', style={
                                'margin': '0px',
                                'font-size': '14px',
                                'font-family': 'Calibri',
                                'height': '18px',
                                'margin-left': '3px'
                            })
                        ], style={'width': '75%'}),
                    ], style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'width': '100%',
                        'height': '18px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 -  neurotroph_reserv_score}%',
                                'background-color': get_color_under_normal_dist(neurotroph_reserv_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px', 'margin-right': '5px'}),
                        html.Div([
                            html.P('Нейротрофный резерв', style={
                                'margin': '0px',
                                'font-size': '14px',
                                'font-family': 'Calibri',
                                'height': '18px',
                                'margin-left': '3px'
                            })
                        ], style={'width': '75%'}),
                    ], style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'width': '100%',
                        'height': '18px'
                    }),
                    
                    
                ], style={'width': '48%', 'height': 'fit-content'}),
                
            # колонка 222222222222222222222222222222222
            
            html.Div([
                    html.Div([
                        html.P('6. Статус микробиоты', style={'margin': '0px', 'margin-bottom': '1px', 'font-weight': 'bold', 'color': '#404547'}),
                        html.Div([
                            html.Div([
                                html.Div([], style={
                                    'width': f"{risk_scores.loc[risk_scores['Группа риска'] == 'Статус микробиоты', 'Риск-скор'].values[0] * 10}%",
                                    'background-color': get_color_under_normal_dist(
                                        100-(risk_scores.loc[risk_scores['Группа риска'] == 'Статус микробиоты', 'Риск-скор'].values[0] * 10)
                                    ),
                                    'border-radius': '2px',
                                    'height': '13px',
                                    'line-height': 'normal',
                                    'display': 'inline-block',
                                    'vertical-align': 'center',
                                }),
                            ], style={'display': 'flex', 'align-self': 'center','width': '70px', 'height': '13px','line-height': 'normal', 'border-radius': '2px','background-color':  'lightgrey', 'margin-left':'5px', 'margin-right':'5px'}),
                            html.B(
                                f"{risk_scores.loc[risk_scores['Группа риска'] == 'Статус микробиоты', 'Риск-скор'].values[0]} из 10",
                                style={'margin': '0px', 'color': '#404547'}
                            )
                        ], style ={'display': 'flex', 'flex-direction': 'row', 'flex-wrap': 'nowrap'})
                    ],  style={
                        'color': 'black',
                        'font-family': 'Calibri',
                        'font-size': '16px',
                        'margin': '0px',
                        'display': 'flex',
                        'justify-content': 'space-between',
                        'margin-bottom': '0px',
                        'margin-top': '10px',
                    }),
                    
                    html.Div([], style={
                        'width': "100%",
                        'background-color': "#2563eb",
                        'height': '2px',
                        'line-height': 'normal',
                        'display': 'inline-block',
                        'vertical-align': 'center',
                        'margin-bottom':'2px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 - tryptophan_metabolism_score}%',
                                'background-color': get_color_under_normal_dist(tryptophan_metabolism_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px', 'margin-right': '5px'}),
                        html.Div([
                            html.P('Метаболизм триптофана', style={
                                'margin': '0px',
                                'font-size': '14px',
                                'font-family': 'Calibri',
                                'height': '18px',
                                'margin-left': '3px'
                            })
                        ], style={'width': '75%'}),
                    ], style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'width': '100%',
                        'height': '18px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 -  inflam_immune_score}%',
                                'background-color': get_color_under_normal_dist(inflam_immune_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px', 'margin-right': '5px'}),
                        html.Div([
                            html.P('Воспаление и иммунитет', style={
                                'margin': '0px',
                                'font-size': '14px',
                                'font-family': 'Calibri',
                                'height': '18px',
                                'margin-left': '3px'
                            })
                        ], style={'width': '75%'}),
                    ], style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'width': '100%',
                        'height': '10px'
                    }),
                    
                html.Div([
                        html.P('7. Резистентность к стрессорам', style={'margin': '0px', 'margin-bottom': '1px', 'font-weight': 'bold', 'color': '#404547'}),
                        html.Div([
                            html.Div([
                                html.Div([], style={
                                    'width': f"{risk_scores.loc[risk_scores['Группа риска'] == 'Резистентность к стрессорам', 'Риск-скор'].values[0] * 10}%",
                                    'background-color': get_color_under_normal_dist(
                                        100-(risk_scores.loc[risk_scores['Группа риска'] == 'Резистентность к стрессорам', 'Риск-скор'].values[0] * 10)
                                    ),
                                    'border-radius': '2px',
                                    'height': '13px',
                                    'line-height': 'normal',
                                    'display': 'inline-block',
                                    'vertical-align': 'center',
                                }),
                            ], style={'display': 'flex', 'align-self': 'center','width': '70px', 'height': '13px','line-height': 'normal', 'border-radius': '2px','background-color':  'lightgrey', 'margin-left':'5px', 'margin-right':'5px'}),
                            html.B(
                                f"{risk_scores.loc[risk_scores['Группа риска'] == 'Резистентность к стрессорам', 'Риск-скор'].values[0]} из 10",
                                style={'margin': '0px', 'color': '#404547'}
                            )
                        ], style ={'display': 'flex', 'flex-direction': 'row', 'flex-wrap': 'nowrap'})
                    ], style={
                        'color': 'black',
                        'font-family': 'Calibri',
                        'font-size': '16px',
                        'margin': '0px',
                        'display': 'flex',
                        'justify-content': 'space-between',
                        'margin-bottom': '0px',
                        'margin-top': '12px'
                    }),
                    
                    
                    html.Div([], style={
                        'width': "100%",
                        'background-color': "#2563eb",
                        'height': '2px',
                        'line-height': 'normal',
                        'display': 'inline-block',
                        'vertical-align': 'center',
                        'margin-bottom':'2px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 - oxidative_stress_score}%',
                                'background-color': get_color_under_normal_dist(oxidative_stress_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px', 'margin-right': '5px'}),
                        html.Div([
                            html.P('Оксидативный стресс', style={
                                'margin': '0px',
                                'font-size': '14px',
                                'font-family': 'Calibri',
                                'height': '18px',
                                'margin-left': '3px'
                            })
                        ], style={'width': '75%'}),
                    ], style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'width': '100%',
                        'height': '18px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 -  inflam_and_microbiotic_score}%',
                                'background-color': get_color_under_normal_dist(inflam_and_microbiotic_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px', 'margin-right': '5px'}),
                        html.Div([
                            html.P('Воспаление и микробный стресс', style={
                                'margin': '0px',
                                'font-size': '14px',
                                'font-family': 'Calibri',
                                'height': '18px',
                                'margin-left': '3px'
                            })
                        ], style={'width': '75%'}),
                    ], style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'width': '100%',
                        'height': '18px'
                    }),
                    
                    # html.Div([
                    #     html.Div([
                    #         html.Div([], style={
                    #             'width': f'{100 -  aromatic_toxic_score}%',
                    #             'background-color': get_color_under_normal_dist(aromatic_toxic_score),
                    #             'border-radius': '5px',
                    #             'height': '10px',
                    #             'line-height': 'normal',
                    #             'display': 'inline-block',
                    #             'vertical-align': 'center'
                    #         }),
                    #     ], style={'width': '23%', 'height': '18px', 'line-height': '18px', 'margin-right': '5px'}),
                    #     html.Div([
                    #         html.P('Ароматические токсины', style={
                    #             'margin': '0px',
                    #             'font-size': '14px',
                    #             'font-family': 'Calibri',
                    #             'height': '18px',
                    #             'margin-left': '3px'
                    #         })
                    #     ], style={'width': '75%'}),
                    # ], style={
                    #     'display': 'flex',
                    #     'justify-content': 'left',
                    #     'width': '100%',
                    #     'height': '18px'
                    # }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 -  nitrogen_toxic_score}%',
                                'background-color': get_color_under_normal_dist(nitrogen_toxic_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px', 'margin-right': '5px'}),
                        html.Div([
                            html.P('Азотистые токсины', style={
                                'margin': '0px',
                                'font-size': '14px',
                                'font-family': 'Calibri',
                                'height': '18px',
                                'margin-left': '3px'
                            })
                        ], style={'width': '75%'}),
                    ], style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'width': '100%',
                        'height': '18px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 -   lipid_toxic_score}%',
                                'background-color': get_color_under_normal_dist(lipid_toxic_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px', 'margin-right': '5px'}),
                        html.Div([
                            html.P('Липидные токсины и β-окисление', style={
                                'margin': '0px',
                                'font-size': '14px',
                                'font-family': 'Calibri',
                                'height': '18px',
                                'margin-left': '3px'
                            })
                        ], style={'width': '75%'}),
                    ], style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'width': '100%',
                        'height': '18px'
                    }),
                
                
                                            
                    
                ], style={'width': '48%', 'height': 'fit-content'}),
            
            
            
            
            ], style={
                'display': 'flex',
                'justify-content': 'space-between',
                'height': 'fit-content',
                'margin-top': '5px'}),
            
            
            
            # Подвал
            html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
                   style={'page-break-after': 'always','color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"left",'font-style':'italic','margin-top':'10px'}),
            
            html.Div([
                html.Div([
                    html.B(f"Дата: {date}",style={'margin':'0px','font-size':'18px','font-family':'Calibri'}),
                    html.Div([
                        html.B(f'Пациент: {name}',style={'margin':'0px','font-size':'18px','font-family':'Calibri'}),
                    ],style={'margin-top':'10px'}),
                ], style={'width':'33.3%'}),
                html.Div([
                    html.B("MetaboScan-Test01",style={'margin':'0px','font-size':'18px','font-family':'Calibri','color':'#FFFFFF'}),
                ], style={'width':'33.3%','text-align':'center'}),
                html.Div([
                    html.Img(src=app.get_asset_url('logo.jpg'),style={'height':'54px','float':'right'}),
                ], style={'width':'33.3%'}),
            ], style={'display':'flex', 'justify-content':'space-between','width':'100%','height':'54px','color':'#2563eb'}),


 html.Div([
            # ADD info icon
            
            html.Img(src=app.get_asset_url('info_icon.png'), style={'width':'20px','height':'20px','margin-right':'15px'}),
            
            html.Div('Данные по оценке состояния организма получены из экспериментальных данных на образцах из биобанка Центра биофармацевтического анализа и метаболомных исследований Сеченовского университета.',
                    style={'color':'black','font-family':'Calibri','font-size':'16px','text-align':"left", 'margin': '0px !important'}),
            ], style={'display': 'flex','margin-top':'10px','margin-bottom':'10px', 'flex-direction': 'row','align-items': 'center', 'width':'fit-content', "borderRadius": "0.5rem", 'padding': '5px 7px 5px 15px', 'border': '2px solid rgb(255, 184, 113)', 'background-color': '#fffede'}),
 
html.Div(
    style={
        "width": "800px",
        "margin": "0 auto",
"marginTop": "10px",
        "fontFamily": "Calibri, Arial, sans-serif",
        "display": "flex",
        "flexWrap": "wrap",
        "gap": "1rem"
    },
    children=[
        # First Card (50%)
        html.Div(
            style={
                "flex": "0 0 calc(50% - 0.5rem)",
                "backgroundColor": "white",
                "border": "1px solid #e5e7eb",
                "borderRadius": "0.5rem",
                "padding": "0.25rem 1rem 0.75rem 1rem",
                "boxSizing": "border-box"
            },
            children=[
                html.Div(
                    style={
                        "display": "flex",
                        "flexWrap": "nowrap",
                        "gap": "0.75rem",
                        "alignItems": "flex-start"
                    },
                    children=[
                        # Left Section
                        html.Div(
                            style={
                                "flex": "0 0 30%",
                                "display": "flex",
                                "flexDirection": "column",
                                "alignItems": "center"
                            },
                            children=[
                                html.H2(
                                    style={
                                        "fontSize": "0.9rem",
                                        "fontWeight": "bold",
                                        "color": "#111827",
                                        "lineHeight": "1.25",
                                        "marginBottom": "0.75rem",
                                        "marginLeft": "0.5rem",
                                        "alignSelf": "flex-start"
                                    },
                                    children=[
                                        "Состояние",
                                        html.Br(),
                                        "сердечно-сосудистой",
                                        html.Br(),
                                        "системы"
                                    ]
                                ),
                                # Score Circle
                                html.Div(
                                    style={
                                        "position": "relative",
                                        "width": "70px",
                                        "height": "70px",
                                        "marginBottom": "0.25rem"
                                    },
                                    children=[
                                        dcc.Graph(
                                            figure={
                                                "data": [
                                                    {
                                                        "type": "pie",
                                                        "values": [cardiovascular_score, 10-cardiovascular_score],
                                                        "hole": 0.8,
                                                        "marker": {
                                                            "colors": [
                                                                get_color_under_normal_dist(100 - cardiovascular_score * 10),  # Dynamic color
                                                                "#e5e7eb"  # Background color
                                                            ]
                                                        },
                                                        "rotation": 90,
                                                        "direction": "clockwise",
                                                        "showlegend": False,
                                                        "textinfo": "none",
                                                        "hoverinfo": "none"
                                                    }
                                                ],
                                                "layout": {
                                                    "width": 70,
                                                    "height": 70,
                                                    "margin": {"l": 0, "r": 0, "b": 0, "t": 0},
                                                    "paper_bgcolor": "rgba(0,0,0,0)",
                                                    "plot_bgcolor": "rgba(0,0,0,0)"
                                                }
                                            },
                                            config={"staticPlot": True},
                                            style={"position": "absolute", "zIndex": 1}
                                        ),
                                        html.Div(
                                            style={
                                                "position": "absolute",
                                                "top": "50%",
                                                "left": "50%",
                                                "transform": "translate(-50%, -50%)",
                                                "textAlign": "center",
                                                "zIndex": 2,
                                                "width": "100%"
                                            },
                                            children=[
                                                html.Div(
                                                    f"{cardiovascular_score}",
                                                    style={
                                                        "fontSize": "1.4rem",
                                                        "fontWeight": "bold",
                                                        "color": "#111827",
                                                        "lineHeight": "1"
                                                    }
                                                ),
                                                html.Div(
                                                    "/10",
                                                    style={
                                                        "fontSize": "0.7rem",
                                                        "color": "#6b7280",
                                                        "lineHeight": "1"
                                                    }
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                html.Div(
                                    get_status_level(100 - cardiovascular_score * 10),
                                    style={
                                        "color": get_color_under_normal_dist(100 - cardiovascular_score * 10),
                                        "fontWeight": "600",
                                        "fontSize": "0.9rem",
                                        "textAlign": "center",
                                        "width": "100%",
                                        "margin": "0",
                                        "padding": "0",
                                        "lineHeight": "1"
                                    }
                                )
                            ]
                        ),
                        # Right Section
                        html.Div(
                            style={
                                "flex": "1",
                                "paddingTop": "0.5rem"
                            },
                            children=[
                                html.H3(
                                    style={
                                        "fontSize": "0.8rem",
                                        "fontWeight": "600",
                                        "color": "#111827",
                                        "marginBottom": "0.5rem"
                                    },
                                    children="Отражает метаболическую нагрузку на сердце и сосуды"
                                ),
                                html.P(
                                    style={
                                        "color": "#374151",
                                        "fontSize": "0.75rem",
                                        "lineHeight": "1.4",
                                        "marginBottom": "0.75rem"
                                    },
                                    children=[
                                        "Оценка данного параметра основана на анализе реальных образцов ",
                                        "плазмы крови пациентов без признаков ССЗ и пациентов с ",
                                        "различными формами сердечно-сосудистых нарушений."
                                    ]
                                ),
                                # Metrics
                                html.Div(
                                    style={
                                        "display": "flex",
                                        "gap": "0.75rem",
                                        "flexWrap": "wrap",
                                        "marginTop": "0.25rem"
                                    },
                                    children=[
                                        html.Div(
                                            [
                                                html.Span("Acc: "),
                                                html.Span("93,7%", style={"fontWeight": "bold"})
                                            ],
                                            style={"fontSize": "0.75rem", "color": "#111827"}
                                        ),
                                        html.Div(
                                            [
                                                html.Span("Se: "),
                                                html.Span("94,4%", style={"fontWeight": "bold"})
                                            ],
                                            style={"fontSize": "0.75rem", "color": "#111827"}
                                        ),
                                        html.Div(
                                            [
                                                html.Span("Sp: "),
                                                html.Span("89,7%", style={"fontWeight": "bold"})
                                            ],
                                            style={"fontSize": "0.75rem", "color": "#111827"}
                                        ),
                                        html.Div(
                                            [
                                                html.Span("+PV: "),
                                                html.Span("98,2%", style={"fontWeight": "bold"})
                                            ],
                                            style={"fontSize": "0.75rem", "color": "#111827"}
                                        ),
                                        html.Div(
                                            [
                                                html.Span("-PV: "),
                                                html.Span("73,2%", style={"fontWeight": "bold"})
                                            ],
                                            style={"fontSize": "0.75rem", "color": "#111827"}
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
        # Second Card (50%)
        html.Div(
            style={
                "flex": "0 0 calc(50% - 0.5rem)",
                "backgroundColor": "white",
                "border": "1px solid #e5e7eb",
                "borderRadius": "0.5rem",
                "padding": "0.25rem 1rem 0.75rem 1rem",
                "boxSizing": "border-box"
            },
            children=[
                html.Div(
                    style={
                        "display": "flex",
                        "flexWrap": "nowrap",
                        "gap": "1rem",
                        "alignItems": "flex-start"
                    },
                    children=[
                        # Left Section
                        html.Div(
                            style={
                                "flex": "0 0 30%",
                                "display": "flex",
                                "flexDirection": "column",
                                "alignItems": "center"
                            },
                            children=[
                                html.H2(
                                    style={
                                        "fontSize": "0.9rem",
                                        "fontWeight": "bold",
                                        "color": "#111827",
                                        "lineHeight": "1.25",
                                        "marginBottom": "0.75rem",
                                        "marginLeft": "0.25rem",
                                        "alignSelf": "flex-start"
                                    },
                                    children=[
                                        "Оценка",
                                        html.Br(),
                                        "пролиферативных",
                                        html.Br(),
                                        "процессов"
                                    ]
                                ),
                                # Score Circle
                                html.Div(
                                    style={
                                        "position": "relative",
                                        "width": "70px",
                                        "height": "70px",
                                        "marginBottom": "0.25rem"
                                    },
                                    children=[
                                        dcc.Graph(
                                                figure={
                                                    "data": [
                                                        {
                                                            "type": "pie",
                                                            "values": [oncology_score, 10-oncology_score],
                                                            "hole": 0.8,
                                                            "marker": {
                                                                "colors": [
                                                                    get_color_under_normal_dist(100 - oncology_score * 10),  # Dynamic color
                                                                    "#e5e7eb"  # Background color
                                                                ]
                                                            },
                                                            "rotation": 90,
                                                            "direction": "clockwise",
                                                            "showlegend": False,
                                                            "textinfo": "none",
                                                            "hoverinfo": "none"
                                                        }
                                                    ],
                                                    "layout": {
                                                        "width": 70,
                                                        "height": 70,
                                                        "margin": {"l": 0, "r": 0, "b": 0, "t": 0},
                                                        "paper_bgcolor": "rgba(0,0,0,0)",
                                                        "plot_bgcolor": "rgba(0,0,0,0)"
                                                    }
                                                },
                                                config={"staticPlot": True},
                                                style={"position": "absolute", "zIndex": 1}
                                            ),
                                            html.Div(
                                                style={
                                                    "position": "absolute",
                                                    "top": "50%",
                                                    "left": "50%",
                                                    "transform": "translate(-50%, -50%)",
                                                    "textAlign": "center",
                                                    "zIndex": 2,
                                                    "width": "100%"
                                                },
                                                children=[
                                                    html.Div(
                                                        f"{oncology_score}",
                                                        style={
                                                            "fontSize": "1.4rem",
                                                            "fontWeight": "bold",
                                                            "color": "#111827",
                                                            "lineHeight": "1"
                                                        }
                                                    ),
                                                    html.Div(
                                                        "/10",
                                                        style={
                                                            "fontSize": "0.7rem",
                                                            "color": "#6b7280",
                                                            "lineHeight": "1"
                                                        }
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                html.Div(
                                    get_status_level(100 - oncology_score * 10),
                                    style={
                                        "color": get_color_under_normal_dist(100 - oncology_score * 10),
                                        "fontWeight": "600",
                                        "fontSize": "0.9rem",
                                        "textAlign": "center",
                                        "width": "100%",
                                        "margin": "0",
                                        "padding": "0",
                                        "lineHeight": "1"
                                    }
                                )
                            ]
                        ),
                        # Right Section
                        html.Div(
                            style={
                                "flex": "1",
                                "paddingTop": "0.5rem"
                            },
                            children=[
                                html.H3(
                                    style={
                                        "fontSize": "0.8rem",
                                        "fontWeight": "600",
                                        "color": "#111827",
                                        "marginBottom": "0.5rem"
                                    },
                                    children="Характеризует метаболическую сбалансированность процессов клеточного обновления, деления и апоптоза."
                                ),
                                html.P(
                                    style={
                                        "color": "#374151",
                                        "fontSize": "0.75rem",
                                        "lineHeight": "1.4",
                                        "marginBottom": "0.75rem"
                                    },
                                    children=[
                                        "Оценка данного параметра основана на анализе плазмы крови пациентов без признаков ",
                                        "онкологических заболеваний и пациентов с различными формами опухолевых процессов, а ",
                                        "именно рак легкого, рак простаты, рак прямой кишки, рак молочной железы и гематологические злокачественные заболевания: лимфомы и множественная миелома."
                                    ]
                                ),
                                # Metrics
                                html.Div(
                                    style={
                                        "display": "flex",
                                        "gap": "0.75rem",
                                        "flexWrap": "wrap",
                                        "marginTop": "0.25rem"
                                    },
                                    children=[
                                        html.Div(
                                            [
                                                html.Span("Acc: "),
                                                html.Span("92,1%", style={"fontWeight": "bold"})
                                            ],
                                            style={"fontSize": "0.75rem", "color": "#111827"}
                                        ),
                                        html.Div(
                                            [
                                                html.Span("Se: "),
                                                html.Span("90,5%", style={"fontWeight": "bold"})
                                            ],
                                            style={"fontSize": "0.75rem", "color": "#111827"}
                                        ),
                                        html.Div(
                                            [
                                                html.Span("Sp: "),
                                                html.Span("89,2%", style={"fontWeight": "bold"})
                                            ],
                                            style={"fontSize": "0.75rem", "color": "#111827"}
                                        ),
                                        html.Div(
                                            [
                                                html.Span("+PV: "),
                                                html.Span("91,8%", style={"fontWeight": "bold"})
                                            ],
                                            style={"fontSize": "0.75rem", "color": "#111827"}
                                        ),
                                        html.Div(
                                            [
                                                html.Span("-PV: "),
                                                html.Span("86,1%", style={"fontWeight": "bold"})
                                            ],
                                            style={"fontSize": "0.75rem", "color": "#111827"}
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
),html.Div(
    style={
        "width": "800px",
        "margin": "0 auto",
"marginTop": "10px",
        "fontFamily": "Calibri, Arial, sans-serif",
        "display": "flex",
        "flexWrap": "wrap",
        "gap": "1rem"
    },
    children=[
        # First Card (50%)
        html.Div(
            style={
                "flex": "0 0 calc(50% - 0.5rem)",
                "backgroundColor": "white",
                "border": "1px solid #e5e7eb",
                "borderRadius": "0.5rem",
                "padding": "0.25rem 1rem 0.75rem 1rem",
                "boxSizing": "border-box"
            },
            children=[
                html.Div(
                    style={
                        "display": "flex",
                        "flexWrap": "nowrap",
                        "gap": "0.75rem",
                        "alignItems": "flex-start"
                    },
                    children=[
                        # Left Section
                        html.Div(
                            style={
                                "flex": "0 0 30%",
                                "display": "flex",
                                "flexDirection": "column",
                                "alignItems": "center"
                            },
                            children=[
                                html.H2(
                                    style={
                                        "fontSize": "0.9rem",
                                        "fontWeight": "bold",
                                        "color": "#111827",
                                        "lineHeight": "1.25",
                                        "marginBottom": "0.75rem",
                                        "marginLeft": "0.5rem",
                                        "alignSelf": "flex-start"
                                    },
                                    children=[
                                        "Состояние",
                                        html.Br(),
                                        "функции печени",
                                    ]
                                ),
                                

                                html.Div(
                                        style={
                                            "position": "relative",
                                            "width": "70px",
                                            "height": "70px",
                                            "marginBottom": "0.25rem"
                                        },
                                        children=[
                                            dcc.Graph(
                                                figure={
                                                    "data": [
                                                        {
                                                            "type": "pie",
                                                            "values": [liver_score, 10-liver_score],
                                                            "hole": 0.8,
                                                            "marker": {
                                                                "colors": [
                                                                    get_color_under_normal_dist(100 - liver_score * 10),  # Dynamic color
                                                                    "#e5e7eb"  # Background color
                                                                ]
                                                            },
                                                            "rotation": 90,
                                                            "direction": "clockwise",
                                                            "showlegend": False,
                                                            "textinfo": "none",
                                                            "hoverinfo": "none"
                                                        }
                                                    ],
                                                    "layout": {
                                                        "width": 70,
                                                        "height": 70,
                                                        "margin": {"l": 0, "r": 0, "b": 0, "t": 0},
                                                        "paper_bgcolor": "rgba(0,0,0,0)",
                                                        "plot_bgcolor": "rgba(0,0,0,0)"
                                                    }
                                                },
                                                config={"staticPlot": True},
                                                style={"position": "absolute", "zIndex": 1}
                                            ),
                                            html.Div(
                                                style={
                                                    "position": "absolute",
                                                    "top": "50%",
                                                    "left": "50%",
                                                    "transform": "translate(-50%, -50%)",
                                                    "textAlign": "center",
                                                    "zIndex": 2,
                                                    "width": "100%"
                                                },
                                                children=[
                                                    html.Div(
                                                        f"{liver_score}",
                                                        style={
                                                            "fontSize": "1.4rem",
                                                            "fontWeight": "bold",
                                                            "color": "#111827",
                                                            "lineHeight": "1"
                                                        }
                                                    ),
                                                    html.Div(
                                                        "/10",
                                                        style={
                                                            "fontSize": "0.7rem",
                                                            "color": "#6b7280",
                                                            "lineHeight": "1"
                                                        }
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                html.Div(
                                    get_status_level(100 - liver_score * 10),
                                    style={
                                        "color": get_color_under_normal_dist(100 - liver_score * 10),
                                        "fontWeight": "600",
                                        "fontSize": "0.9rem",
                                        "textAlign": "center",
                                        "width": "100%",
                                        "margin": "0",
                                        "padding": "0",
                                        "lineHeight": "1"
                                    }
                                )
                            ]
                        ),
                        # Right Section
                        html.Div(
                            style={
                                "flex": "1",
                                "paddingTop": "0.5rem"
                            },
                            children=[
                                html.H3(
                                    style={
                                        "fontSize": "0.8rem",
                                        "fontWeight": "600",
                                        "color": "#111827",
                                        "marginBottom": "0.5rem"
                                    },
                                    children="Оценивает вовлеченность печени в обменные и детоксикационные процессы организма"
                                ),
                                html.P(
                                    style={
                                        "color": "#374151",
                                        "fontSize": "0.75rem",
                                        "lineHeight": "1.4",
                                        "marginBottom": "0.75rem"
                                    },
                                    children=[
                                        "Оценка данного параметра основана на анализе плазмы крови пациентов без признаков ",
                                        "заболеваний печени и пациентов с различными нарушениями гепатобилиарной функции, ",
                                        "включая неалкогольную жировую болезнь печени (НАЖБП), хронический гепатит, алкогольное ",
                                        "поражение печени и цирроз."
                                    ]
                                ),
                                # Metrics
                                html.Div(
                                    style={
                                        "display": "flex",
                                        "gap": "0.75rem",
                                        "flexWrap": "wrap",
                                        "marginTop": "0.25rem"
                                    },
                                    children=[
                                        html.Div(
                                            [
                                                html.Span("Acc: "),
                                                html.Span("91,8%", style={"fontWeight": "bold"})
                                            ],
                                            style={"fontSize": "0.75rem", "color": "#111827"}
                                        ),
                                        html.Div(
                                            [
                                                html.Span("Se: "),
                                                html.Span("90,7%", style={"fontWeight": "bold"})
                                            ],
                                            style={"fontSize": "0.75rem", "color": "#111827"}
                                        ),
                                        html.Div(
                                            [
                                                html.Span("Sp: "),
                                                html.Span("87,9%", style={"fontWeight": "bold"})
                                            ],
                                            style={"fontSize": "0.75rem", "color": "#111827"}
                                        ),
                                        html.Div(
                                            [
                                                html.Span("+PV: "),
                                                html.Span("92,1%", style={"fontWeight": "bold"})
                                            ],
                                            style={"fontSize": "0.75rem", "color": "#111827"}
                                        ),
                                        html.Div(
                                            [
                                                html.Span("-PV: "),
                                                html.Span("85,4%", style={"fontWeight": "bold"})
                                            ],
                                            style={"fontSize": "0.75rem", "color": "#111827"}
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
        # Second Card (50%)
        html.Div(
            style={
                "flex": "0 0 calc(50% - 0.5rem)",
                "backgroundColor": "white",
                "border": "1px solid #e5e7eb",
                "borderRadius": "0.5rem",
                "padding": "0.25rem 1rem 0.75rem 1rem",
                "boxSizing": "border-box"
            },
            children=[
                html.Div(
                    style={
                        "display": "flex",
                        "flexWrap": "nowrap",
                        "gap": "1rem",
                        "alignItems": "flex-start"
                    },
                    children=[
                        # Left Section
                        html.Div(
                            style={
                                "flex": "0 0 30%",
                                "display": "flex",
                                "flexDirection": "column",
                                "alignItems": "center"
                            },
                            children=[
                                html.H2(
                                    style={
                                        "fontSize": "0.9rem",
                                        "fontWeight": "bold",
                                        "color": "#111827",
                                        "lineHeight": "1.25",
                                        "marginBottom": "0.75rem",
                                        "marginLeft": "0.25rem",
                                        "alignSelf": "flex-start"
                                    },
                                    children=[
                                        "Состояние",
                                        html.Br(),
                                        "дыхательной",
                                        html.Br(),
                                        "системы"
                                    ]
                                ),
                                # Score Circle
                               html.Div(
                                        style={
                                            "position": "relative",
                                            "width": "70px",
                                            "height": "70px",
                                            "marginBottom": "0.25rem"
                                        },
                                        children=[
                                            dcc.Graph(
                                                figure={
                                                    "data": [
                                                        {
                                                            "type": "pie",
                                                            "values": [pulmonary_score, 10-pulmonary_score],
                                                            "hole": 0.8,
                                                            "marker": {
                                                                "colors": [
                                                                    get_color_under_normal_dist(100 - pulmonary_score * 10),  # Dynamic color
                                                                    "#e5e7eb"  # Background color
                                                                ]
                                                            },
                                                            "rotation": 90,
                                                            "direction": "clockwise",
                                                            "showlegend": False,
                                                            "textinfo": "none",
                                                            "hoverinfo": "none"
                                                        }
                                                    ],
                                                    "layout": {
                                                        "width": 70,
                                                        "height": 70,
                                                        "margin": {"l": 0, "r": 0, "b": 0, "t": 0},
                                                        "paper_bgcolor": "rgba(0,0,0,0)",
                                                        "plot_bgcolor": "rgba(0,0,0,0)"
                                                    }
                                                },
                                                config={"staticPlot": True},
                                                style={"position": "absolute", "zIndex": 1}
                                            ),
                                            html.Div(
                                                style={
                                                    "position": "absolute",
                                                    "top": "50%",
                                                    "left": "50%",
                                                    "transform": "translate(-50%, -50%)",
                                                    "textAlign": "center",
                                                    "zIndex": 2,
                                                    "width": "100%"
                                                },
                                                children=[
                                                    html.Div(
                                                        f"{pulmonary_score}",
                                                        style={
                                                            "fontSize": "1.4rem",
                                                            "fontWeight": "bold",
                                                            "color": "#111827",
                                                            "lineHeight": "1"
                                                        }
                                                    ),
                                                    html.Div(
                                                        "/10",
                                                        style={
                                                            "fontSize": "0.7rem",
                                                            "color": "#6b7280",
                                                            "lineHeight": "1"
                                                        }
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                html.Div(
                                    get_status_level(100 - pulmonary_score * 10),
                                    style={
                                        "color": get_color_under_normal_dist(100 - pulmonary_score * 10),
                                        "fontWeight": "600",
                                        "fontSize": "0.9rem",
                                        "textAlign": "center",
                                        "width": "100%",
                                        "margin": "0",
                                        "padding": "0",
                                        "lineHeight": "1"
                                    }
                                )
                            ]
                        ),
                        # Right Section
                        html.Div(
                            style={
                                "flex": "1",
                                "paddingTop": "0.5rem"
                            },
                            children=[
                                html.H3(
                                    style={
                                        "fontSize": "0.8rem",
                                        "fontWeight": "600",
                                        "color": "#111827",
                                        "marginBottom": "0.5rem"
                                    },
                                    children="Показывает метаболическую адаптацию дыхательной системы к физиологическим нагрузкам и внешним факторам"
                                ),
                                html.P(
                                    style={
                                        "color": "#374151",
                                        "fontSize": "0.75rem",
                                        "lineHeight": "1.4",
                                        "marginBottom": "0.75rem"
                                    },
                                    children=[
                                        "Оценка данного параметра основана на анализе плазмы крови пациентов без признаков легочной дисфункции и пациентов с хроническими заболеваниями ",
                                        "дыхательных путей, включая бронхиальную астму, хроническую обструктивную болезнь ",
                                        "легких (ХОБЛ), постковидный синдром и легочный фиброз."
                                    ]
                                ),
                                # Metrics
                                html.Div(
                                    style={
                                        "display": "flex",
                                        "gap": "0.75rem",
                                        "flexWrap": "wrap",
                                        "marginTop": "0.25rem"
                                    },
                                    children=[
                                        html.Div(
                                            [
                                                html.Span("Acc: "),
                                                html.Span("90,4%", style={"fontWeight": "bold"})
                                            ],
                                            style={"fontSize": "0.75rem", "color": "#111827"}
                                        ),
                                        html.Div(
                                            [
                                                html.Span("Se: "),
                                                html.Span("88,9%", style={"fontWeight": "bold"})
                                            ],
                                            style={"fontSize": "0.75rem", "color": "#111827"}
                                        ),
                                        html.Div(
                                            [
                                                html.Span("Sp: "),
                                                html.Span("86,2%", style={"fontWeight": "bold"})
                                            ],
                                            style={"fontSize": "0.75rem", "color": "#111827"}
                                        ),
                                        html.Div(
                                            [
                                                html.Span("+PV: "),
                                                html.Span("89,7%", style={"fontWeight": "bold"})
                                            ],
                                            style={"fontSize": "0.75rem", "color": "#111827"}
                                        ),
                                        html.Div(
                                            [
                                                html.Span("-PV: "),
                                                html.Span("84,5%", style={"fontWeight": "bold"})
                                            ],
                                            style={"fontSize": "0.75rem", "color": "#111827"}
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
),
html.Div(
    style={
        "width": "800px",
        "margin": "0 auto",
        "marginTop": "10px",
        "fontFamily": "Calibri, Arial, sans-serif",
        "display": "flex",
        "flexWrap": "wrap",
        "gap": "1rem"
    },
    children=[
#         # First Card (50%)
#         html.Div(
#             style={
#                 "flex": "0 0 calc(50% - 0.5rem)",
#                 "backgroundColor": "white",
#                 "border": "1px solid #e5e7eb",
#                 "borderRadius": "0.5rem",
#                 "padding": "0.25rem 1rem 0.75rem 1rem",
#                 "boxSizing": "border-box"
#             },
#             children=[
#                 html.Div(
#                     style={
#                         "display": "flex",
#                         "flexWrap": "nowrap",
#                         "gap": "0.75rem",
#                         "alignItems": "flex-start"
#                     },
#                     children=[
#                         # Left Section
#                         html.Div(
#                             style={
#                                 "flex": "0 0 30%",
#                                 "display": "flex",
#                                 "flexDirection": "column",
#                                 "alignItems": "center"
#                             },
#                             children=[
#                                 html.H2(
#                                     style={
#                                         "fontSize": "0.9rem",
#                                         "fontWeight": "bold",
#                                         "color": "#111827",
#                                         "lineHeight": "1.25",
#                                         "marginBottom": "0.75rem",
#                                         "marginLeft": "0.5rem",
#                                         "alignSelf": "flex-start"
#                                     },
#                                     children=[
#                                         "Состояние",
#                                         html.Br(),
#                                         "углеводного",
#                                         html.Br(),
#                                         "обмена"
#                                     ]
#                                 ),
#                                 # Score Circle
#                                 html.Div(
#                                         style={
#                                             "position": "relative",
#                                             "width": "70px",
#                                             "height": "70px",
#                                             "marginBottom": "0.25rem"
#                                         },
#                                         children=[
#                                             dcc.Graph(
#                                                 figure={
#                                                     "data": [
#                                                         {
#                                                             "type": "pie",
#                                                             "values": [arthritis_score, 10-arthritis_score],
#                                                             "hole": 0.8,
#                                                             "marker": {
#                                                                 "colors": [
#                                                                     get_color_under_normal_dist(100 - arthritis_score * 10),  # Dynamic color
#                                                                     "#e5e7eb"  # Background color
#                                                                 ]
#                                                             },
#                                                             "rotation": 90,
#                                                             "direction": "clockwise",
#                                                             "showlegend": False,
#                                                             "textinfo": "none",
#                                                             "hoverinfo": "none"
#                                                         }
#                                                     ],
#                                                     "layout": {
#                                                         "width": 70,
#                                                         "height": 70,
#                                                         "margin": {"l": 0, "r": 0, "b": 0, "t": 0},
#                                                         "paper_bgcolor": "rgba(0,0,0,0)",
#                                                         "plot_bgcolor": "rgba(0,0,0,0)"
#                                                     }
#                                                 },
#                                                 config={"staticPlot": True},
#                                                 style={"position": "absolute", "zIndex": 1}
#                                             ),
#                                             html.Div(
#                                                 style={
#                                                     "position": "absolute",
#                                                     "top": "50%",
#                                                     "left": "50%",
#                                                     "transform": "translate(-50%, -50%)",
#                                                     "textAlign": "center",
#                                                     "zIndex": 2,
#                                                     "width": "100%"
#                                                 },
#                                                 children=[
#                                                     html.Div(
#                                                         f"{arthritis_score}",
#                                                         style={
#                                                             "fontSize": "1.4rem",
#                                                             "fontWeight": "bold",
#                                                             "color": "#111827",
#                                                             "lineHeight": "1"
#                                                         }
#                                                     ),
#                                                     html.Div(
#                                                         "/10",
#                                                         style={
#                                                             "fontSize": "0.7rem",
#                                                             "color": "#6b7280",
#                                                             "lineHeight": "1"
#                                                         }
#                                                     )
#                                                 ]
#                                             )
#                                         ]
#                                     ),
#                                 html.Div(
#                                     'НЕ ПОДЕЛЮЧЕНА',
#                                     style={
#                                         "color": get_color_under_normal_dist(100 - arthritis_score * 10),
#                                         "fontWeight": "600",
#                                         "fontSize": "0.9rem",
#                                         "textAlign": "center",
#                                         "width": "100%",
#                                         "margin": "0",
#                                         "padding": "0",
#                                         "lineHeight": "1"
#                                     }
#                                 )
#                             ]
#                         ),
#                         # Right Section
#                         html.Div(
#                             style={
#                                 "flex": "1",
#                                 "paddingTop": "0.5rem"
#                             },
#                             children=[
#                                 html.H3(
#                                     style={
#                                         "fontSize": "0.8rem",
#                                         "fontWeight": "600",
#                                         "color": "#111827",
#                                         "marginBottom": "0.5rem"
#                                     },
#                                     children="Отражает регуляцию глюкозного обмена и метаболическую адаптацию организма к колебаниям уровня сахара"
#                                 ),
#                                 html.P(
#                                     style={
#                                         "color": "#374151",
#                                         "fontSize": "0.75rem",
#                                         "lineHeight": "1.4",
#                                         "marginBottom": "0.75rem"
#                                     },
#                                     children=[
#                                         "Оценка данного параметра основана на анализе плазмы крови пациентов без признаков нарушений углеводного обмена и пациентов с подтвержденными нарушениями ",
#                                         "толерантности к глюкозе, инсулинорезистентностью и сахарным диабетом 2 типа."
#                                     ]
#                                 ),
#                                 # Metrics
#                                 html.Div(
#                                     style={
#                                         "display": "flex",
#                                         "gap": "0.75rem",
#                                         "flexWrap": "wrap",
#                                         "marginTop": "0.25rem"
#                                     },
#                                     children=[
#                                         html.Div(
#                                             [
#                                                 html.Span("Acc: "),
#                                                 html.Span("92,5%", style={"fontWeight": "bold"})
#                                             ],
#                                             style={"fontSize": "0.75rem", "color": "#111827"}
#                                         ),
#                                         html.Div(
#                                             [
#                                                 html.Span("Se: "),
#                                                 html.Span("90,1%", style={"fontWeight": "bold"})
#                                             ],
#                                             style={"fontSize": "0.75rem", "color": "#111827"}
#                                         ),
#                                         html.Div(
#                                             [
#                                                 html.Span("Sp: "),
#                                                 html.Span("88,3%", style={"fontWeight": "bold"})
#                                             ],
#                                             style={"fontSize": "0.75rem", "color": "#111827"}
#                                         ),
#                                         html.Div(
#                                             [
#                                                 html.Span("+PV: "),
#                                                 html.Span("91,4%", style={"fontWeight": "bold"})
#                                             ],
#                                             style={"fontSize": "0.75rem", "color": "#111827"}
#                                         ),
#                                         html.Div(
#                                             [
#                                                 html.Span("-PV: "),
#                                                 html.Span("86,7%", style={"fontWeight": "bold"})
#                                             ],
#                                             style={"fontSize": "0.75rem", "color": "#111827"}
#                                         )
#                                     ]
#                                 )
#                             ]
#                         )
#                     ]
#                 )
#             ]
#         ),
        # Second Card (50%)
        html.Div(
            style={
                "flex": "0 0 calc(50% - 0.5rem)",
                "backgroundColor": "white",
                "border": "1px solid #e5e7eb",
                "borderRadius": "0.5rem",
                "padding": "0.25rem 1rem 0.75rem 1rem",
                "boxSizing": "border-box"
            },
            children=[
                html.Div(
                    style={
                        "display": "flex",
                        "flexWrap": "nowrap",
                        "gap": "1rem",
                        "alignItems": "flex-start"
                    },
                    children=[
                        # Left Section
                        html.Div(
                            style={
                                "flex": "0 0 30%",
                                "display": "flex",
                                "flexDirection": "column",
                                "alignItems": "center"
                            },
                            children=[
                                html.H2(
                                    style={
                                        "fontSize": "0.9rem",
                                        "fontWeight": "bold",
                                        "color": "#111827",
                                        "lineHeight": "1.25",
                                        "marginBottom": "0.75rem",
                                        "marginLeft": "0.25rem",
                                        "alignSelf": "flex-start"
                                    },
                                    children=[
                                        "Состояние",
                                        html.Br(),
                                        "иммунного",
                                        html.Br(),
                                        "метаболического",
                                        html.Br(),
                                        "баланса"
                                    ]
                                ),
                                # Score Circle
                                 html.Div(
                                        style={
                                            "position": "relative",
                                            "width": "70px",
                                            "height": "70px",
                                            "marginBottom": "0.25rem"
                                        },
                                        children=[
                                            dcc.Graph(
                                                figure={
                                                    "data": [
                                                        {
                                                            "type": "pie",
                                                            "values": [arthritis_score, 10-arthritis_score],
                                                            "hole": 0.8,
                                                            "marker": {
                                                                "colors": [
                                                                    get_color_under_normal_dist(100 - arthritis_score * 10),  # Dynamic color
                                                                    "#e5e7eb"  # Background color
                                                                ]
                                                            },
                                                            "rotation": 90,
                                                            "direction": "clockwise",
                                                            "showlegend": False,
                                                            "textinfo": "none",
                                                            "hoverinfo": "none"
                                                        }
                                                    ],
                                                    "layout": {
                                                        "width": 70,
                                                        "height": 70,
                                                        "margin": {"l": 0, "r": 0, "b": 0, "t": 0},
                                                        "paper_bgcolor": "rgba(0,0,0,0)",
                                                        "plot_bgcolor": "rgba(0,0,0,0)"
                                                    }
                                                },
                                                config={"staticPlot": True},
                                                style={"position": "absolute", "zIndex": 1}
                                            ),
                                            html.Div(
                                                style={
                                                    "position": "absolute",
                                                    "top": "50%",
                                                    "left": "50%",
                                                    "transform": "translate(-50%, -50%)",
                                                    "textAlign": "center",
                                                    "zIndex": 2,
                                                    "width": "100%"
                                                },
                                                children=[
                                                    html.Div(
                                                        f"{arthritis_score}",
                                                        style={
                                                            "fontSize": "1.4rem",
                                                            "fontWeight": "bold",
                                                            "color": "#111827",
                                                            "lineHeight": "1"
                                                        }
                                                    ),
                                                    html.Div(
                                                        "/10",
                                                        style={
                                                            "fontSize": "0.7rem",
                                                            "color": "#6b7280",
                                                            "lineHeight": "1"
                                                        }
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                html.Div(
                                    get_status_level(100 - arthritis_score * 10),
                                    style={
                                        "color": get_color_under_normal_dist(100 - arthritis_score * 10),
                                        "fontWeight": "600",
                                        "fontSize": "0.9rem",
                                        "textAlign": "center",
                                        "width": "100%",
                                        "margin": "0",
                                        "padding": "0",
                                        "lineHeight": "1"
                                    }
                                )
                            ]
                        ),
                        # Right Section
                        html.Div(
                            style={
                                "flex": "1",
                                "paddingTop": "0.5rem"
                            },
                            children=[
                                html.H3(
                                    style={
                                        "fontSize": "0.8rem",
                                        "fontWeight": "600",
                                        "color": "#111827",
                                        "marginBottom": "0.5rem"
                                    },
                                    children="Отражает метаболические отклонения, связанные с хронической активацией иммунной системы и воспалением"
                                ),
                                html.P(
                                    style={
                                        "color": "#374151",
                                        "fontSize": "0.75rem",
                                        "lineHeight": "1.4",
                                        "marginBottom": "0.75rem"
                                    },
                                    children=[
                                        "Оценка данного параметра основана на анализе плазмы крови пациентов без признаков аутоиммунных ",
                                        "расстройств и пациентов с установленным диагнозом ревматоидного ",
                                        "артрита различной степени активности."
                                    ]
                                ),
                                # Metrics
                                html.Div(
                                    style={
                                        "display": "flex",
                                        "gap": "0.75rem",
                                        "flexWrap": "wrap",
                                        "marginTop": "0.25rem"
                                    },
                                    children=[
                                        html.Div(
                                            [
                                                html.Span("Acc: "),
                                                html.Span("93,7%", style={"fontWeight": "bold"})
                                            ],
                                            style={"fontSize": "0.75rem", "color": "#111827"}
                                        ),
                                        html.Div(
                                            [
                                                html.Span("Se: "),
                                                html.Span("94,4%", style={"fontWeight": "bold"})
                                            ],
                                            style={"fontSize": "0.75rem", "color": "#111827"}
                                        ),
                                        html.Div(
                                            [
                                                html.Span("Sp: "),
                                                html.Span("89,7%", style={"fontWeight": "bold"})
                                            ],
                                            style={"fontSize": "0.75rem", "color": "#111827"}
                                        ),
                                        html.Div(
                                            [
                                                html.Span("+PV: "),
                                                html.Span("98,2%", style={"fontWeight": "bold"})
                                            ],
                                            style={"fontSize": "0.75rem", "color": "#111827"}
                                        ),
                                        html.Div(
                                            [
                                                html.Span("-PV: "),
                                                html.Span("73,2%", style={"fontWeight": "bold"})
                                            ],
                                            style={"fontSize": "0.75rem", "color": "#111827"}
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
),
            html.Div([
                    html.Div([
                        html.Table([
                            # Row 1
                            html.Tr([
                                html.Td([html.B("Acc: "), html.Span('Точность (диагностическая ценность метода)')]),
                            ]),
                            # Row 2
                            html.Tr([
                                html.Td([html.B("Se: "), html.Span('Чувствительность (вероятность истинного "положительного теста")')]),
                            ]),
                            # Row 3
                            html.Tr([
                                html.Td([html.B("Sp: "), html.Span('Специфичность (вероятность истинного "отрицательного теста")')]),
                            ]),
                            # Row 4
                            html.Tr([
                                html.Td([html.B("+PV: "), html.Span('Точность положительного предсказания (вероятность того, что заболевание присутствует, когда тест положительный)')]),
                            ]),
                            # Row 5
                            html.Tr([
                                html.Td([html.B("-PV: "), html.Span('Точность отрицательного предсказания (вероятность того, что заболевание отсутствует, когда тест отрицательный)')]),
                            ]),
                        ], style={'width': '100%', 'border-collapse': 'collapse'}),
                    ], style={
                        'margin-bottom': '5px',
                        'font-family': 'Calibri',
                        'font-size': '12px',
                        'color': '#404547'
                    }),
                ], style={
                    'display': 'flex',
                    
                    'margin-top': '20px',
                    'margin-bottom': '5px',
                    'flex-direction': 'row',
                    'align-items': 'center',
                    'width': '95%',
                    "borderRadius": "0.5rem",
                    'padding': '3px  15px',
                    'border': '2px solid rgba(51, 131, 223, 0.6)',
                    'background-color': "#eff9ff"
                }),
            html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
                   style={'page-break-after': 'always','color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"left",'font-style':'italic','margin-top':'30px'}),
            # Страница 1.1
            
            # 2 страница
            html.Div([],style={'height':'8mm','width':'100%'}),
                html.Div([
                    html.Div([
                        html.B(f"Дата: {date}",style={'margin':'0px','font-size':'18px','font-family':'Calibri'}),
                        html.Div([
                            html.B(f'Пациент: {name}',style={'margin':'0px','font-size':'18px','font-family':'Calibri'}),
                        ],style={'margin-top':'10px'}),
                    ], style={'width':'33.3%'}),
                    html.Div([
                        html.B("MetaboScan-Test01",style={'margin':'0px','font-size':'18px','font-family':'Calibri','color':'#FFFFFF'}),
                    ], style={'width':'33.3%','text-align':'center'}),
                    html.Div([
                        html.Img(src=app.get_asset_url('logo.jpg'),style={'height':'54px','float':'right'}),
                    ], style={'width':'33.3%'}),
                ], style={'display':'flex', 'justify-content':'space-between','width':'100%','height':'54px','color':'#2563eb'}),    
                html.Div([
                html.H3(children='1. Аминокислоты', style={'textAlign':'left','margin':'0px','line-height':'normal','display':'inline-block','vertical-align':'center'}),]
                    , style={'width':'100%','background-color':'#2563eb','border-radius':'5px 5px 0px 0px', 'color':'white','font-family':'Calibri','margin':'0px','height':'35px','line-height':'35px','text-align':'center','margin-top':'5px'}),
                html.Div([
                    html.Div([
                    html.Div([
                        html.Div([html.B('Метаболизм фенилаланина',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'16px','font-family':'Calibri','color':'#2563eb','line-height':'40px'}),
                        
                    
                        html.Div([html.Div('Результат',style={'display':'inline-block', 'fontSize': '14px', 'color': '#4D5052', 'fontWeight': '500'})],style={'width':'7%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center'}),
                       html.Div([
                            html.Div([
                                html.Span('20%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('40%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('60%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('80%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                            ], style={
                                'width': '100%',
                                'display': 'flex',
                                'justify-content': 'space-between',
                                'font-family': 'Calibri',
                                'color': '#4D5052',
                                'font-size': '13px',
                                'padding': '4px 8px',
                            })
                        ], style={
                            'width': '27%',
                            'margin': '0px'
                        }),
                        html.Div([html.Div('Норма, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'#4D5052','text-align':'center'}),
                    ], style={'width':'100%','display':'flex','alignItems':'center','justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Фенилаланин (Phe)',style={'height':'20px'}),html.P('Незаменимая глюко-, кетогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_1[0]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_1[0],ref_1[0])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_1[0],ref_1[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_1[0],ref_1[0])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_1[0], ref_1[0])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_1[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Тирозин (Tyr)',style={'height':'20px'}),html.P('Заменимая глюко-, кетогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_1[1]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_1[1],ref_1[1])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_1[1],ref_1[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_1[1],ref_1[1])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_1[1], ref_1[1])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_1[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.B('Лейцин + Изолейцин (Leu+Ile)', style={'height': '20px'}),
                                    html.P('Незаменимая глюко-, кетогенная аминокислота', 
                                        style={'height': '20px', 'font-size': '12px', 'font-family': 'Calibri', 
                                                'color': '#2563eb', 'margin': '0px', 'margin-left': '5px', 
                                                'line-height': '0.9em'})
                                ], style={'width': '39%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': 'black', 'margin-top': '5px'}),
                                
                                html.Div([
                                    html.Div([
                                        html.Div([
                                           
                                            html.B(f'{value_2[0]}', 
                                                style={'text-align': 'right', 'width': '50%', 'background-color':f'{heighlight_out_of_range(value_2[0],ref_2[0])}', 'padding': '3px 8px', 'borderRadius': '12px'})
                                        ], style={'width': '100%', 'display': 'flex', 'justify-content': 'center', 
                                                'margin-top': f'{need_of_margin(value_2[0],ref_2[0])}'})
                                    ], style={'height': '20px', 'line-height': 'normal', 'display': 'inline-block', 
                                            'vertical-align': 'center', 'width': '100%'})
                                ], style={'width': '8%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': f'{color_text_ref(value_2[0],ref_2[0])}', 
                                        'line-height': '53px'}),
                                
                            html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_2[1], ref_2[1])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                
                                html.Div([
                                    html.P(f'{ref_2[0]}', 
                                        style={'height': '20px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center', 'margin': '0'})
                                ], style={'width': '21%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': 'black', 'text-align': 'center', 
                                        'line-height': '53px'}),
                            ], style={'width': '99.2%', 'display': 'flex', 'justify-content': 'space-between',
                                    'height': '53px', 'margin-left': '5px'}),
                        ], style={'margin': '0px', 'margin-left': '20px'}),
                    ], style={'margin': '0px', 'background-color': '#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Валин (Val)',style={'height':'20px'}),html.P('Незаменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_2[1]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_2[1],ref_2[1])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_2[1],ref_2[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_2[1],ref_2[1])}','line-height':'53px'}),
                                # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_2[1], ref_2[1])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_2[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    
                    html.Div([
                    html.Div([
                        html.Div([html.B('Метаболизм гистидина',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'16px','font-family':'Calibri','color':'#2563eb','line-height':'40px'}),
                        html.Div([html.Div('Результат',style={'display':'inline-block', 'fontSize': '14px', 'color': '#4D5052', 'fontWeight': '500'})],style={'width':'7%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center'}),
                       html.Div([
                            html.Div([
                                html.Span('20%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('40%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('60%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('80%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                            ], style={
                                'width': '100%',
                                'display': 'flex',
                                'justify-content': 'space-between',
                                'font-family': 'Calibri',
                                'color': '#4D5052',
                                'font-size': '13px',
                                'padding': '4px 8px',
                            })
                        ], style={
                            'width': '27%',
                            'margin': '0px'
                        }),
                        html.Div([html.Div('Норма, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'#4D5052','text-align':'center'}),
                    ], style={'width':'100%','display':'flex','alignItems':'center','justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Гистидин (His)',style={'height':'20px'}),html.P('Незаменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_3[0]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_3[0],ref_3[0])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_3[0],ref_3[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_3[0],ref_3[0])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_3[0], ref_3[0])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_3[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Метилгистидин (MH)',style={'height':'20px'}),html.P('Метаболит карнозина',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_3[1]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_3[1],ref_3[1])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_3[1],ref_3[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_3[1],ref_3[1])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_3[1], ref_3[1])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_3[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Треонин (Thr)',style={'height':'20px'}),html.P('Незаменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_3[2]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_3[2],ref_3[2])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_3[2],ref_3[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_3[2],ref_3[2])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_3[2], ref_3[2])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_3[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Карнозин (Car)',style={'height':'20px'}),html.P('Дипептид, состоящий из аланина и гистидина',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_3[3]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_3[3],ref_3[3])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_3[3],ref_3[3])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_3[3],ref_3[3])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress_left.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_3[3], ref_3[3])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_3[3]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Глицин (Gly)',style={'height':'20px'}),html.P('Заменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_3[4]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_3[4],ref_3[4])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_3[4],ref_3[4])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_3[4],ref_3[4])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_3[4], ref_3[4])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_3[4]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Диметилглицин (DMG)',style={'height':'20px'}),html.P('Промежуточный продукт синтеза глицина',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_3[5]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_3[5],ref_3[5])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_3[5],ref_3[5])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_3[5],ref_3[5])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_3[5], ref_3[5])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_3[5]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Серин (Ser)',style={'height':'20px'}),html.P('Заменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_3[6]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_3[6],ref_3[6])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_3[6],ref_3[6])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_3[6],ref_3[6])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_3[6], ref_3[6])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_3[6]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Лизин (Lys)',style={'height':'20px'}),html.P('Незаменимая кетогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_3[7]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_3[7],ref_3[7])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_3[7],ref_3[7])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_3[7],ref_3[7])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_3[7], ref_3[7])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_3[7]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Глутаминовая кислота (Glu)',style={'height':'20px'}),html.P('Заменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_3[8]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_3[8],ref_3[8])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_3[8],ref_3[8])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_3[8],ref_3[8])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_3[8], ref_3[8])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_3[8]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Глутамин (Gln)',style={'height':'20px'}),html.P('Заменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_3[9]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_3[9],ref_3[9])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_3[9],ref_3[9])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_3[9],ref_3[9])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_3[9], ref_3[9])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_3[9]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    
                                        html.Div([
                    html.Div([
                        html.Div([html.B('Метаболизм метионина',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'16px','font-family':'Calibri','color':'#2563eb','line-height':'40px'}),
                        html.Div([html.Div('Результат',style={'display':'inline-block', 'fontSize': '14px', 'color': '#4D5052', 'fontWeight': '500'})],style={'width':'7%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center'}),
                       html.Div([
                            html.Div([
                                html.Span('20%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('40%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('60%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('80%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                            ], style={
                                'width': '100%',
                                'display': 'flex',
                                'justify-content': 'space-between',
                                'font-family': 'Calibri',
                                'color': '#4D5052',
                                'font-size': '13px',
                                'padding': '4px 8px',
                            })
                        ], style={
                            'width': '27%',
                            'margin': '0px'
                        }),
                        html.Div([html.Div('Норма, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'#4D5052','text-align':'center'}),
                    ], style={'width':'100%','display':'flex','alignItems':'center','justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Метионин (Met)',style={'height':'20px'}),html.P('Незаменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_4[0]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_4[0],ref_4[0])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_4[0],ref_4[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_4[0],ref_4[0])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_4[0],ref_4[0])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_4[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Метионин сульфоксид (MetSO)',style={'height':'20px'}),html.P('Продукт окисления метионина',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_4[1]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_4[1],ref_4[1])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_4[1],ref_4[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_4[1],ref_4[1])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress_left.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_4[1],ref_4[1])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_4[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    
                ], style={'margin':'0px'}),
                html.Div([
                    html.Div([
                        html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
                            style={'color':'black', 'font-family':'Calibri', 'font-size':'14px', 
                                    'margin':'0px', 'text-align':"left", 'font-style':'italic',
                                    'margin-top':'5px', 'width':'85%'}),
                        html.P('|1',
                            style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"right",'font-style':'italic','margin-top':'5px','width':'10%','margin-top':'15px'}),
                    ], style={'display':'flex', 'justify-content':'space-between', 'width':'100%', 
                            'position': 'absolute', 'left': '0', 'padding': '0'})
                ], style={'position': 'relative', 'height': '60px', 'width': '100%', 'margin-top': '55px'}),
            
            
            
            # 3 страница
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
                        html.B("MetaboScan-Test01",style={'margin':'0px','font-size':'18px','font-family':'Calibri','color':'#FFFFFF'}),
                    ], style={'width':'33.3%','text-align':'center'}),
                    html.Div([
                        html.Img(src=app.get_asset_url('logo.jpg'),style={'height':'53px','float':'right'}),
                    ], style={'width':'33.3%'}),
                ], style={'display':'flex', 'justify-content':'space-between','width':'100%','height':'53px','color':'#2563eb'}),    
                
                html.Div([
                    
                    html.Div([
                    html.Div([
                        html.Div([html.B('Метаболизм метионина',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'16px','font-family':'Calibri','color':'#2563eb','line-height':'40px'}),
                        html.Div([html.Div('Результат',style={'display':'inline-block', 'fontSize': '14px', 'color': '#4D5052', 'fontWeight': '500'})],style={'width':'7%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center'}),
                       html.Div([
                            html.Div([
                                html.Span('20%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('40%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('60%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('80%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                            ], style={
                                'width': '100%',
                                'display': 'flex',
                                'justify-content': 'space-between',
                                'font-family': 'Calibri',
                                'color': '#4D5052',
                                'font-size': '13px',
                                'padding': '4px 8px',
                            })
                        ], style={
                            'width': '27%',
                            'margin': '0px'
                        }),
                        html.Div([html.Div('Норма, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'#4D5052','text-align':'center'}),
                    ], style={'width':'100%','display':'flex','alignItems':'center','justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Таурин (Tau)',style={'height':'20px'}),html.P('Заменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_4[2]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_4[2],ref_4[2])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_4[2],ref_4[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_4[2],ref_4[2])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_4[2],ref_4[2])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_4[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Бетаин (Bet)',style={'height':'20px'}),html.P('Продукт метаболизма холина',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_4[3]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_4[3],ref_4[3])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_4[3],ref_4[3])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_4[3],ref_4[3])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_4[3],ref_4[3])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_4[3]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Холин (Chl)',style={'height':'20px'}),html.P('Компонент мембран клеток, источник ацетилхолина',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_4[4]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_4[4],ref_4[4])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_4[4],ref_4[4])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_4[4],ref_4[4])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_4[4],ref_4[4])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_4[4]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Триметиламин-N-оксид (TMAO)',style={'height':'20px'}),html.P('Продукт метаболизма холина, бетаина и др. бактериями ЖКТ',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_4[5]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_4[5],ref_4[5])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_4[5],ref_4[5])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_4[5],ref_4[5])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_4[5],ref_4[5])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_4[5]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    
                    html.Div([
                html.H3(children='2. Метаболизм триптофана', style={'textAlign':'center','margin':'0px','line-height':'normal','display':'inline-block','vertical-align':'center'}),]
                    , style={'width':'100%','background-color':'#2563eb','border-radius':'5px 5px 0px 0px', 'color':'white','font-family':'Calibri','margin':'0px','height':'35px','line-height':'35px','text-align':'center','margin-top':'5px'}),
                    html.Div([
                    html.Div([
                        html.Div([html.B('Кинурениновый путь',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'16px','font-family':'Calibri','color':'#2563eb','line-height':'40px'}),
                        html.Div([html.Div('Результат',style={'display':'inline-block', 'fontSize': '14px', 'color': '#4D5052', 'fontWeight': '500'})],style={'width':'7%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center'}),
                       html.Div([
                            html.Div([
                                html.Span('20%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('40%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('60%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('80%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                            ], style={
                                'width': '100%',
                                'display': 'flex',
                                'justify-content': 'space-between',
                                'font-family': 'Calibri',
                                'color': '#4D5052',
                                'font-size': '13px',
                                'padding': '4px 8px',
                            })
                        ], style={
                            'width': '27%',
                            'margin': '0px'
                        }),
                        html.Div([html.Div('Норма, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'#4D5052','text-align':'center'}),
                    ], style={'width':'100%','display':'flex','alignItems':'center','justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Триптофан (Trp)',style={'height':'20px'}),html.P('Незаменимая глюко-, кетогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_5[0]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_5[0],ref_5[0])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_5[0],ref_5[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_5[0],ref_5[0])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_5[0],ref_5[0])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_5[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Кинуренин (Kyn)',style={'height':'20px'}),html.P('Продукт метаболизма триптофана по кинурениновому пути',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_5[1]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_5[1],ref_5[1])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_5[1],ref_5[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_5[1],ref_5[1])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_5[1],ref_5[1])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_5[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Антраниловая кислота (Ant)',style={'height':'20px'}),html.P('Продукт метаболизма кинуренина',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_5[2]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_5[2],ref_5[2])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_5[2],ref_5[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_5[2],ref_5[2])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_5[2],ref_5[2])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_5[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Хинолиновая кислота (QA)',style={'height':'20px'}),html.P('Продукт метаболизма 3-гидроксиантраниловой кислоты',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_5[3]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_5[3],ref_5[3])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_5[3],ref_5[3])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_5[3],ref_5[3])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_5[3],ref_5[3])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_5[3]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                                html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Ксантуреновая кислота (Xnt)',style={'height':'20px'}),html.P('Продукт метаболизма кинуренина',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_5[4]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_5[4],ref_5[4])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_5[4],ref_5[4])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_5[4],ref_5[4])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress_left.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_5[4],ref_5[4])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_5[4]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                                
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Кинуреновая кислота (Kyna)',style={'height':'20px'}),html.P('Продукт метаболизма кинуренина',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_5[5]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_5[5],ref_5[5])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_5[5],ref_5[5])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_5[5],ref_5[5])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_5[5],ref_5[5])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_5[5]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                   
                    html.Div([
                    html.Div([
                        html.Div([html.B('Серотониновый путь',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'16px','font-family':'Calibri','color':'#2563eb','line-height':'40px'}),
                        html.Div([html.Div('Результат',style={'display':'inline-block', 'fontSize': '14px', 'color': '#4D5052', 'fontWeight': '500'})],style={'width':'7%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center'}),
                       html.Div([
                            html.Div([
                                html.Span('20%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('40%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('60%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('80%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                            ], style={
                                'width': '100%',
                                'display': 'flex',
                                'justify-content': 'space-between',
                                'font-family': 'Calibri',
                                'color': '#4D5052',
                                'font-size': '13px',
                                'padding': '4px 8px',
                            })
                        ], style={
                            'width': '27%',
                            'margin': '0px'
                        }),
                        html.Div([html.Div('Норма, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'#4D5052','text-align':'center'}),
                    ], style={'width':'100%','display':'flex','alignItems':'center','justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Серотонин (Ser)',style={'height':'20px'}),html.P('Нейромедиатор',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_6[0]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_6[0],ref_6[0])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_6[0],ref_6[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_6[0],ref_6[0])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_6[0],ref_6[0])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_6[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('5-Гидроксииндолуксусная кислота (5-HIAA)',style={'height':'20px'}),html.P('Метаболит серотонина',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_6[1]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_6[1],ref_6[1])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_6[1],ref_6[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_6[1],ref_6[1])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress_left.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_6[1],ref_6[1])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_6[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                   
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('5-Гидрокситриптофан (5-HTP)',style={'height':'20px'}),html.P('Прекурсор серотонина',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_6[2]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_6[2],ref_6[2])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_6[2],ref_6[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_6[2],ref_6[2])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_6[2],ref_6[2])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_6[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    
                    html.Div([
                    html.Div([
                        html.Div([html.B('Индоловый путь',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'16px','font-family':'Calibri','color':'#2563eb','line-height':'40px'}),
                        html.Div([html.Div('Результат',style={'display':'inline-block', 'fontSize': '14px', 'color': '#4D5052', 'fontWeight': '500'})],style={'width':'7%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center'}),
                       html.Div([
                            html.Div([
                                html.Span('20%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('40%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('60%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('80%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                            ], style={
                                'width': '100%',
                                'display': 'flex',
                                'justify-content': 'space-between',
                                'font-family': 'Calibri',
                                'color': '#4D5052',
                                'font-size': '13px',
                                'padding': '4px 8px',
                            })
                        ], style={
                            'width': '27%',
                            'margin': '0px'
                        }),
                        html.Div([html.Div('Норма, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'#4D5052','text-align':'center'}),
                    ], style={'width':'100%','display':'flex','alignItems':'center','justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('3-Индолуксусная кислота (IAA)',style={'height':'20px'}),html.P('Продукт катаболизма триптофана кишечной микробиотой',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_7[0]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_7[0],ref_7[0])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_7[0],ref_7[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_7[0],ref_7[0])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_7[0],ref_7[0])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_7[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('3-Индолмолочная кислота (ILA)',style={'height':'20px'}),html.P('Продукт катаболизма триптофана кишечной микробиотой',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_7[1]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_7[1],ref_7[1])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_7[1],ref_7[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_7[1],ref_7[1])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_7[1],ref_7[1])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_7[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    
                ], style={'margin':'0px'}),
            ]),
            html.Div([
                html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
                style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"left",'font-style':'italic','margin-top':'5px','width':'85%'}),
                html.P('|2',
                    style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"right",'font-style':'italic','margin-top':'5px','width':'10%','margin-top':'15px'}),
            ], style={'page-break-after': 'always','margin':'0px','display':'flex','justify-content':'space-between','width':'100%','margin-top':'50px'}),
            
            #4 страница
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
                        html.B("MetaboScan-Test01",style={'margin':'0px','font-size':'18px','font-family':'Calibri','color':'#FFFFFF'}),
                    ], style={'width':'33.3%','text-align':'center'}),
                    html.Div([
                        html.Img(src=app.get_asset_url('logo.jpg'),style={'height':'53px','float':'right'}),
                    ], style={'width':'33.3%'}),
                ], style={'display':'flex', 'justify-content':'space-between','width':'100%','height':'53px','color':'#2563eb'}),    
                
                html.Div([
                    
                    html.Div([
                    html.Div([
                        html.Div([html.B('Индоловый путь',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'16px','font-family':'Calibri','color':'#2563eb','line-height':'40px'}),
                        html.Div([html.Div('Результат',style={'display':'inline-block', 'fontSize': '14px', 'color': '#4D5052', 'fontWeight': '500'})],style={'width':'7%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center'}),
                       html.Div([
                            html.Div([
                                html.Span('20%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('40%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('60%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('80%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                            ], style={
                                'width': '100%',
                                'display': 'flex',
                                'justify-content': 'space-between',
                                'font-family': 'Calibri',
                                'color': '#4D5052',
                                'font-size': '13px',
                                'padding': '4px 8px',
                            })
                        ], style={
                            'width': '27%',
                            'margin': '0px'
                        }),
                        html.Div([html.Div('Норма, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'#4D5052','text-align':'center'}),
                    ], style={'width':'100%','display':'flex','alignItems':'center','justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('3-Индолкарбоксальдегид (ICAA)',style={'height':'20px'}),html.P('Продукт катаболизма триптофана кишечной микробиотой',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_7[2]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_7[2],ref_7[2])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_7[2],ref_7[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_7[2],ref_7[2])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_7[2],ref_7[2])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_7[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('3-Индолпропионовая кислота (IPA)',style={'height':'20px'}),html.P('Продукт катаболизма триптофана кишечной микробиотой',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_7[3]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_7[3],ref_7[3])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_7[3],ref_7[3])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_7[3],ref_7[3])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_7[3],ref_7[3])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_7[3]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('3-Индолмасляная кислота (IBA)',style={'height':'20px'}),html.P('Продукт катаболизма триптофана кишечной микробиотой',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_7[4]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_7[4],ref_7[4])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_7[4],ref_7[4])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_7[4],ref_7[4])}','line-height':'53px'}),
                                # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress_left.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_7[4],ref_7[4])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_7[4]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Триптамин (TA)',style={'height':'20px'}),html.P('Продукт катаболизма триптофана кишечной микробиотой, прекурсор для нейромедиаторов',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_7[5]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_7[5],ref_7[5])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_7[5],ref_7[5])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_7[5],ref_7[5])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress_left.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_7[5],ref_7[5])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_7[5]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    
                    html.Div([
                html.H3(children='3. Метаболизм аргинина', style={'textAlign':'center','margin':'0px','line-height':'normal','display':'inline-block','vertical-align':'center'}),]
                    , style={'width':'100%','background-color':'#2563eb','border-radius':'5px 5px 0px 0px', 'color':'white','font-family':'Calibri','margin':'0px','height':'35px','line-height':'35px','text-align':'center','margin-top':'5px'}),
                    html.Div([
                    html.Div([
                        html.Div([html.B('Метаболизм аргинина',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'16px','font-family':'Calibri','color':'#2563eb','line-height':'40px'}),
                        html.Div([html.Div('Результат',style={'display':'inline-block', 'fontSize': '14px', 'color': '#4D5052', 'fontWeight': '500'})],style={'width':'7%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center'}),
                       html.Div([
                            html.Div([
                                html.Span('20%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('40%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('60%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('80%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                            ], style={
                                'width': '100%',
                                'display': 'flex',
                                'justify-content': 'space-between',
                                'font-family': 'Calibri',
                                'color': '#4D5052',
                                'font-size': '13px',
                                'padding': '4px 8px',
                            })
                        ], style={
                            'width': '27%',
                            'margin': '0px'
                        }),
                        html.Div([html.Div('Норма, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'#4D5052','text-align':'center'}),
                    ], style={'width':'100%','display':'flex','alignItems':'center','justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Пролин (Pro)',style={'height':'20px'}),html.P('Заменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_8[0]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_8[0],ref_8[0])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_8[0],ref_8[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_8[0],ref_8[0])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_8[0],ref_8[0])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_8[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Гидроксипролин (Hyp)',style={'height':'20px'}),html.P('Источник коллагена',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_8[1]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_8[1],ref_8[1])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_8[1],ref_8[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_8[1],ref_8[1])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_8[1],ref_8[1])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_8[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Асимметричный диметиларгинин (ADMA)',style={'height':'20px'}),html.P('Эндогенный ингибитор синтазы оксида азота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_8[2]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_8[2],ref_8[2])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_8[2],ref_8[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_8[2],ref_8[2])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_8[2],ref_8[2])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_8[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    

                        html.Div([
                            html.Div([
                                html.Div([html.B('Монометиларгинин (MMA)',style={'height':'20px'}),html.P('Эндогенный ингибитор синтазы оксида азота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_8[3]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_8[3],ref_8[3])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_8[3],ref_8[3])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_8[3],ref_8[3])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress_left.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_8[3],ref_8[3])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_8[3]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Симметричный диметиларгинин (SDMA)',style={'height':'20px'}),html.P('Продукт метаболизма аргинина, выводится с почками',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_8[4]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_8[4],ref_8[4])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_8[4],ref_8[4])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_8[4],ref_8[4])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_8[4],ref_8[4])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_8[4]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Гомоаргинин (HomoArg)',style={'height':'20px'}),html.P('Субстрат для синтазы оксида азота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_8[5]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_8[5],ref_8[5])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_8[5],ref_8[5])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_8[5],ref_8[5])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_8[5],ref_8[5])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_8[5]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Аргинин (Arg)',style={'height':'20px'}),html.P('Незаменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_8[6]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_8[6],ref_8[6])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_8[6],ref_8[6])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_8[6],ref_8[6])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_8[6],ref_8[6])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_8[6]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Цитруллин (Cit)',style={'height':'20px'}),html.P('Метаболит цикла мочевины',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_8[7]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_8[7],ref_8[7])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_8[7],ref_8[7])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_8[7],ref_8[7])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_8[7],ref_8[7])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_8[7]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Орнитин (Orn)',style={'height':'20px'}),html.P('Метаболит цикла мочевины',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_8[8]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_8[8],ref_8[8])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_8[8],ref_8[8])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_8[8],ref_8[8])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_8[8],ref_8[8])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_8[8]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Аспарагин (Asn)',style={'height':'20px'}),html.P('Заменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_8[9]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_8[9],ref_8[9])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_8[9],ref_8[9])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_8[9],ref_8[9])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_8[9],ref_8[9])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_8[9]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Аспарагиновая кислота (Asp)',style={'height':'20px'}),html.P('Заменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_8[10]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_8[10],ref_8[10])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_8[10],ref_8[10])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_8[10],ref_8[10])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_8[10],ref_8[10])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_8[10]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Креатинин (Cr)',style={'height':'20px'}),html.P('Продукт метаболизма аргинина',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_8[11]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_8[11],ref_8[11])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_8[11],ref_8[11])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_8[11],ref_8[11])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_8[11],ref_8[11])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_8[11]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    
                ], style={'margin':'0px'}),
            ]),
            html.Div([
                html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
                style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"left",'font-style':'italic','margin-top':'5px','width':'85%'}),
                html.P('|3',
                    style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"right",'font-style':'italic','margin-top':'5px','width':'10%','margin-top':'15px'}),
            ], style={'page-break-after': 'always','margin':'0px','display':'flex','justify-content':'space-between','width':'100%','margin-top':'95px'}),
            
            # 5 страница
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
                        html.B("MetaboScan-Test01",style={'margin':'0px','font-size':'18px','font-family':'Calibri','color':'#FFFFFF'}),
                    ], style={'width':'33.3%','text-align':'center'}),
                    html.Div([
                        html.Img(src=app.get_asset_url('logo.jpg'),style={'height':'53px','float':'right'}),
                    ], style={'width':'33.3%'}),
                ], style={'display':'flex', 'justify-content':'space-between','width':'100%','height':'53px','color':'#2563eb'}),    
                
                html.Div([

                    html.Div([
                html.H3(children='4. Метаболизм жирных кислот', style={'textAlign':'center','margin':'0px','line-height':'normal','display':'inline-block','vertical-align':'center'}),]
                    , style={'width':'100%','background-color':'#2563eb','border-radius':'5px 5px 0px 0px', 'color':'white','font-family':'Calibri','margin':'0px','height':'35px','line-height':'35px','text-align':'center','margin-top':'5px'}),
                    html.Div([
                    html.Div([
                        html.Div([html.B('Метаболизм ацилкарнитинов',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'16px','font-family':'Calibri','color':'#2563eb','line-height':'40px'}),
                        html.Div([html.Div('Результат',style={'display':'inline-block', 'fontSize': '14px', 'color': '#4D5052', 'fontWeight': '500'})],style={'width':'7%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center'}),
                       html.Div([
                            html.Div([
                                html.Span('20%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('40%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('60%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('80%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                            ], style={
                                'width': '100%',
                                'display': 'flex',
                                'justify-content': 'space-between',
                                'font-family': 'Calibri',
                                'color': '#4D5052',
                                'font-size': '13px',
                                'padding': '4px 8px',
                            })
                        ], style={
                            'width': '27%',
                            'margin': '0px'
                        }),
                        html.Div([html.Div('Норма, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'#4D5052','text-align':'center'}),
                    ], style={'width':'100%','display':'flex','alignItems':'center','justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Аланин (Ala)',style={'height':'20px'}),html.P('Заменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_9[0]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_9[0],ref_9[0])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_9[0],ref_9[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_9[0],ref_9[0])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_9[0],ref_9[0])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_9[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Карнитин (C0)',style={'height':'20px'}),html.P('Основа для ацилкарнитинов, транспорт жирных кислот',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_9[1]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_9[1],ref_9[1])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':'12px'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_9[1],ref_9[1])}','line-height':'45px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_9[1],ref_9[1])}%',
                                                'top': '4px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '45px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_9[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'45px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'45px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Ацетилкарнитин (C2)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_9[2]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_9[2],ref_9[2])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':'12px'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_9[2],ref_9[2])}','line-height':'45px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_9[2],ref_9[2])}%',
                                                'top': '4px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '45px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_9[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'45px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'45px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    
                    html.Div([
                    html.Div([
                        html.Div([html.B('Короткоцепочечные ацилкарнитины',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'16px','font-family':'Calibri','color':'#2563eb','line-height':'40px'}),
                        html.Div([html.Div('Результат',style={'display':'inline-block', 'fontSize': '14px', 'color': '#4D5052', 'fontWeight': '500'})],style={'width':'7%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center'}),
                       html.Div([
                            html.Div([
                                html.Span('20%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('40%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('60%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('80%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                            ], style={
                                'width': '100%',
                                'display': 'flex',
                                'justify-content': 'space-between',
                                'font-family': 'Calibri',
                                'color': '#4D5052',
                                'font-size': '13px',
                                'padding': '4px 8px',
                            })
                        ], style={
                            'width': '27%',
                            'margin': '0px'
                        }),
                        html.Div([html.Div('Норма, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'#4D5052','text-align':'center'}),
                    ], style={'width':'100%','display':'flex','alignItems':'center','justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Пропионилкарнитин (С3)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_10[0]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_10[0],ref_10[0])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':'12px'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_10[0],ref_10[0])}','line-height':'45px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_10[0],ref_10[0])}%',
                                                'top': '4px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '45px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_10[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'45px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'45px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),

                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Бутирилкарнитин (C4)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_10[1]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_10[1],ref_10[1])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':'12px'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_10[1],ref_10[1])}','line-height':'45px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_10[1],ref_10[1])}%',
                                                'top': '4px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '45px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_10[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'45px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'45px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Изовалерилкарнитин (С5)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_10[2]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_10[2],ref_10[2])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':'12px'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_10[2],ref_10[2])}','line-height':'45px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_10[2],ref_10[2])}%',
                                                'top': '4px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '45px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_10[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'45px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'45px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Тиглилкарнитин (C5-1)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_10[3]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_10[3],ref_10[3])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':'12px'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_10[3],ref_10[3])}','line-height':'45px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress_left.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_10[3],ref_10[3])}%',
                                                'top': '4px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '45px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_10[3]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'45px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'45px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Глутарилкарнитин (C5-DC)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_10[4]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_10[4],ref_10[4])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':'12px'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_10[4],ref_10[4])}','line-height':'45px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress_left.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_10[4],ref_10[4])}%',
                                                'top': '4px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '45px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_10[4]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'45px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'45px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Гидроксиизовалерилкарнитин (C5-OH)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_10[5]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_10[5],ref_10[5])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':'12px'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_10[5],ref_10[5])}','line-height':'45px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress_left.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_10[5],ref_10[5])}%',
                                                'top': '4px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '45px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_10[5]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'45px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'45px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    
                    html.Div([
                    html.Div([
                        html.Div([html.B('Среднецепочечные ацилкарнитины',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'16px','font-family':'Calibri','color':'#2563eb','line-height':'40px'}),
                        html.Div([html.Div('Результат',style={'display':'inline-block', 'fontSize': '14px', 'color': '#4D5052', 'fontWeight': '500'})],style={'width':'7%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center'}),
                       html.Div([
                            html.Div([
                                html.Span('20%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('40%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('60%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('80%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                            ], style={
                                'width': '100%',
                                'display': 'flex',
                                'justify-content': 'space-between',
                                'font-family': 'Calibri',
                                'color': '#4D5052',
                                'font-size': '13px',
                                'padding': '4px 8px',
                            })
                        ], style={
                            'width': '27%',
                            'margin': '0px'
                        }),
                        html.Div([html.Div('Норма, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'#4D5052','text-align':'center'}),
                    ], style={'width':'100%','display':'flex','alignItems':'center','justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Гексаноилкарнитин (C6)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_11[0]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_11[0],ref_11[0])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':'12px'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_11[0],ref_11[0])}','line-height':'45px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_11[0],ref_11[0])}%',
                                                'top': '4px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '45px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_11[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'45px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'45px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Адипоилкарнитин (C6-DC)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_11[1]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_11[1],ref_11[1])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':'12px'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_11[1],ref_11[1])}','line-height':'45px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress_left.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_11[1],ref_11[1])}%',
                                                'top': '4px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '45px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_11[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'45px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'45px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Октаноилкарнитин (C8)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_11[2]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_11[2],ref_11[2])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':'12px'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_11[2],ref_11[2])}','line-height':'45px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_11[2],ref_11[2])}%',
                                                'top': '4px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '45px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_11[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'45px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'45px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Октеноилкарнитин (C8-1)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_11[3]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_11[3],ref_11[3])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':'12px'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_11[3],ref_11[3])}','line-height':'45px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_11[3],ref_11[3])}%',
                                                'top': '4px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '45px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_11[3]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'45px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'45px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Деканоилкарнитин (C10)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_11[4]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_11[4],ref_11[4])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':'12px'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_11[4],ref_11[4])}','line-height':'45px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_11[4],ref_11[4])}%',
                                                'top': '4px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '45px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_11[4]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'45px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'45px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Деценоилкарнитин (C10-1)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_11[5]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_11[5],ref_11[5])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':'12px'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_11[5],ref_11[5])}','line-height':'45px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_11[5],ref_11[5])}%',
                                                'top': '4px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '45px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_11[5]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'45px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'45px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Декадиеноилкарнитин (C10-2)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_11[6]}',style={'text-align':'center','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':'12px'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_11[6],ref_11[6])}','line-height':'45px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress_left.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_11[6],ref_11[6])}%',
                                                'top': '4px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '45px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_11[6]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'45px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'45px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Додеканоилкарнитин (C12)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_11[7]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_11[7],ref_11[7])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':'12px'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_11[7],ref_11[7])}','line-height':'45px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_11[7],ref_11[7])}%',
                                                'top': '4px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '45px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_11[7]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'45px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'45px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Додеценоилкарнитин (C12-1)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_11[8]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_11[8],ref_11[8])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':'12px'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_11[8],ref_11[8])}','line-height':'45px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress_left.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_11[8],ref_11[8])}%',
                                                'top': '4px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '45px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_11[8]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'45px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'45px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'45px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    
                ], style={'margin':'0px'}),
            ]),
            html.Div([
                html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
                style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"left",'font-style':'italic','margin-top':'5px','width':'85%'}),
                html.P('|4',
                    style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"right",'font-style':'italic','margin-top':'5px','width':'10%','margin-top':'15px'}),
            ], style={'page-break-after': 'always','margin':'0px','display':'flex','justify-content':'space-between','width':'100%','margin-top':'85px'}),
            
            # 6 страница
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
                        html.B("MetaboScan-Test01",style={'margin':'0px','font-size':'18px','font-family':'Calibri','color':'#FFFFFF'}),
                    ], style={'width':'33.3%','text-align':'center'}),
                    html.Div([
                        html.Img(src=app.get_asset_url('logo.jpg'),style={'height':'54px','float':'right'}),
                    ], style={'width':'33.3%'}),
                ], style={'display':'flex', 'justify-content':'space-between','width':'100%','height':'54px','color':'#2563eb'}),    
                html.Div([
                    
                    html.Div([
                    html.Div([
                        html.Div([html.B('Длинноцепочечные ацилкарнитины',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'16px','font-family':'Calibri','color':'#2563eb','line-height':'40px'}),
                        html.Div([html.Div('Результат',style={'display':'inline-block', 'fontSize': '14px', 'color': '#4D5052', 'fontWeight': '500'})],style={'width':'7%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center'}),
                       html.Div([
                            html.Div([
                                html.Span('20%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('40%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('60%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('80%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                            ], style={
                                'width': '100%',
                                'display': 'flex',
                                'justify-content': 'space-between',
                                'font-family': 'Calibri',
                                'color': '#4D5052',
                                'font-size': '13px',
                                'padding': '4px 8px',
                            })
                        ], style={
                            'width': '27%',
                            'margin': '0px'
                        }),
                        html.Div([html.Div('Норма, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'#4D5052','text-align':'center'}),
                    ], style={'width':'100%','display':'flex','alignItems':'center','justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Тетрадеканоилкарнитин (C14)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_12[0]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_12[0],ref_12[0])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_12[0],ref_12[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_12[0],ref_12[0])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_12[0],ref_12[0])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_12[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Тетрадеценоилкарнитин (С14-1)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_12[1]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_12[1],ref_12[1])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_12[1],ref_12[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_12[1],ref_12[1])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_12[1],ref_12[1])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_12[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Тетрадекадиеноилкарнитин (C14-2)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_12[2]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_12[2],ref_12[2])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_12[2],ref_12[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_12[2],ref_12[2])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress_left.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_12[2],ref_12[2])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_12[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Гидрокситетрадеканоилкарнитин (C14-OH)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_12[3]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_12[3],ref_12[3])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_12[3],ref_12[3])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_12[3],ref_12[3])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress_left.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_12[3],ref_12[3])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_12[3]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Пальмитоилкарнитин (C16)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_12[4]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_12[4],ref_12[4])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_12[4],ref_12[4])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_12[4],ref_12[4])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_12[4],ref_12[4])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_12[4]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Гексадецениолкарнитин (C16-1)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_12[5]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_12[5],ref_12[5])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_12[5],ref_12[5])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_12[5],ref_12[5])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_12[5],ref_12[5])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_12[5]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Гидроксигексадецениолкарнитин (C16-1-OH)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_12[6]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_12[6],ref_12[6])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_12[6],ref_12[6])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_12[6],ref_12[6])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_12[6],ref_12[6])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_12[6]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Гидроксигексадеканоилкарнитин (C16-OH)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_12[7]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_12[7],ref_12[7])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_12[7],ref_12[7])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_12[7],ref_12[7])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_12[7],ref_12[7])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_12[7]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Стеароилкарнитин (С18)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_12[8]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_12[8],ref_12[8])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_12[8],ref_12[8])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_12[8],ref_12[8])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_12[8],ref_12[8])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_12[8]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Олеоилкарнитин (C18-1)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_12[9]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_12[9],ref_12[9])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_12[9],ref_12[9])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_12[9],ref_12[9])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_12[9],ref_12[9])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_12[9]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Гидроксиоктадеценоилкарнитин (C18-1-OH)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_12[10]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_12[10],ref_12[10])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_12[10],ref_12[10])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_12[10],ref_12[10])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress_left.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_12[10],ref_12[10])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_12[10]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Линолеоилкарнитин (C18-2)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_12[11]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_12[11],ref_12[11])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_12[11],ref_12[11])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_12[11],ref_12[11])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_12[11],ref_12[11])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_12[11]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Гидроксиоктадеканоилкарнитин (C18-OH)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_12[12]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_12[12],ref_12[12])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_12[12],ref_12[12])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_12[12],ref_12[12])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_12[12],ref_12[12])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_12[12]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    
                    html.Div([
                        html.H3(children='5. Метаболический баланс', style={'textAlign':'center','margin':'0px','line-height':'normal','display':'inline-block','vertical-align':'center'}),]
                    , style={'width':'100%','background-color':'#2563eb','border-radius':'5px 5px 0px 0px', 'color':'white','font-family':'Calibri','margin':'0px','height':'35px','line-height':'35px','text-align':'center','margin-top':'5px'}),
                    html.Div([
                    html.Div([
                        html.Div([html.B('Витамины и нейромедиаторы',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'16px','font-family':'Calibri','color':'#2563eb','line-height':'40px'}),
                        html.Div([html.Div('Результат',style={'display':'inline-block', 'fontSize': '14px', 'color': '#4D5052', 'fontWeight': '500'})],style={'width':'7%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center'}),
                       html.Div([
                            html.Div([
                                html.Span('20%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('40%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('60%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('80%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                            ], style={
                                'width': '100%',
                                'display': 'flex',
                                'justify-content': 'space-between',
                                'font-family': 'Calibri',
                                'color': '#4D5052',
                                'font-size': '13px',
                                'padding': '4px 8px',
                            })
                        ], style={
                            'width': '27%',
                            'margin': '0px'
                        }),
                        html.Div([html.Div('Норма, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'#4D5052','text-align':'center'}),
                    ], style={'width':'100%','display':'flex','alignItems':'center','justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Пантотеновая кислота',style={'height':'20px'}),html.P('Витамин B5',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_13[0]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_13[0],ref_13[0])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_13[0],ref_13[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_13[0],ref_13[0])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_13[0],ref_13[0])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_13[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Рибофлавин',style={'height':'20px'}),html.P('Витамин B2',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_13[1]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_13[1],ref_13[1])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_13[1],ref_13[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_13[1],ref_13[1])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_13[1],ref_13[1])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_13[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Мелатонин',style={'height':'20px'}),html.P('Регулирует циркадные ритмы',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_13[2]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_13[2],ref_13[2])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_13[2],ref_13[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_13[2],ref_13[2])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_13[2],ref_13[2])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_13[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    
                    
                ], style={'margin':'0px'}),
            ]),
            html.Div([
                html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
                style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"left",'font-style':'italic','margin-top':'5px','width':'85%'}),
                html.P('|5',
                    style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"right",'font-style':'italic','margin-top':'5px','width':'10%','margin-top':'15px'}),
            ], style={'page-break-after': 'always','margin':'0px','display':'flex','justify-content':'space-between','width':'100%','margin-top':'95px'}),
            
            #7 страница
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
                        html.B("MetaboScan-Test01",style={'margin':'0px','font-size':'18px','font-family':'Calibri','color':'#FFFFFF'}),
                    ], style={'width':'33.3%','text-align':'center'}),
                    html.Div([
                        html.Img(src=app.get_asset_url('logo.jpg'),style={'height':'53px','float':'right'}),
                    ], style={'width':'33.3%'}),
                ], style={'display':'flex', 'justify-content':'space-between','width':'100%','height':'53px','color':'#2563eb'}),    
                
               html.Div([
                    html.Div([
                    html.Div([
                        html.Div([html.B('Нуклеозиды',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#2563eb','line-height':'40px'}),
                        html.Div([html.Div('Результат',style={'display':'inline-block', 'fontSize': '14px', 'color': '#4D5052', 'fontWeight': '500'})],style={'width':'7%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center'}),
                       html.Div([
                            html.Div([
                                html.Span('20%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('40%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('60%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('80%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                            ], style={
                                'width': '100%',
                                'display': 'flex',
                                'justify-content': 'space-between',
                                'font-family': 'Calibri',
                                'color': '#4D5052',
                                'font-size': '13px',
                                'padding': '4px 8px',
                            })
                        ], style={
                            'width': '27%',
                            'margin': '0px'
                        }),
                        html.Div([html.Div('Норма, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'#4D5052','text-align':'center'}),
                    ], style={'width':'100%','display':'flex','alignItems':'center','justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Уридин',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_14[0]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_14[0],ref_14[0])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_14[0],ref_14[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_14[0],ref_14[0])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_14[0],ref_14[0])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_14[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Аденозин',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_14[1]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_14[1],ref_14[1])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_14[1],ref_14[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_14[1],ref_14[1])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_14[1],ref_14[1])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_14[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                                html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Цитидин',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_14[2]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_14[2],ref_14[2])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_14[2],ref_14[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_14[2],ref_14[2])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_14[2],ref_14[2])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_14[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                         html.Div([
                    html.Div([
                        html.Div([html.B('Аллергия и стресс',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#2563eb','line-height':'40px'}),
                        html.Div([html.Div('Результат',style={'display':'inline-block', 'fontSize': '14px', 'color': '#4D5052', 'fontWeight': '500'})],style={'width':'7%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center'}),
                       html.Div([
                            html.Div([
                                html.Span('20%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('40%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('60%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                                html.Span('80%', style={'display': 'inline-block', 'width': '25%', 'text-align': 'center'}),
                            ], style={
                                'width': '100%',
                                'display': 'flex',
                                'justify-content': 'space-between',
                                'font-family': 'Calibri',
                                'color': '#4D5052',
                                'font-size': '13px',
                                'padding': '4px 8px',
                            })
                        ], style={
                            'width': '27%',
                            'margin': '0px'
                        }),
                        html.Div([html.Div('Норма, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'#4D5052','text-align':'center'}),
                    ], style={'width':'100%','display':'flex','alignItems':'center','justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    
                        html.Div([
                            html.Div([
                                html.Div([html.B('Кортизол',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_15[0]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_15[0],ref_15[0])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_15[0],ref_15[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_15[0],ref_15[0])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_15[0],ref_15[0])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_15[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Гистамин',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#2563eb','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{value_15[1]}',style={'text-align':'center','width':'50%', 'background-color':f'{heighlight_out_of_range(value_15[1],ref_15[1])}', 'padding': '3px 8px', 'borderRadius': '12px'})],style={'width':'100%','display':'flex','justify-content':'center','margin-top':f'{need_of_margin(value_15[1],ref_15[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_15[1],ref_15[1])}','line-height':'53px'}),
                                                        # Progress bar with pointer
                                html.Div([
                                    # Progress bar
                                    html.Img(src=app.get_asset_url('progress_left.png'), 
                                            style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                                'display': 'inline-block', 'vertical-align': 'center'}),
                                    # Pointer (arrow)
                                    html.Img(src=app.get_asset_url('pointer.png'), 
                                            style={
                                                'position': 'absolute',
                                                'height': '38px',
                                                'width': '4px',
                                                'left': f'{calculate_pointer_position(value_15[1],ref_15[1])}%',
                                                'top': '6px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#2563eb', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_15[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    
                html.Div(
    style={
        'width': '100%',
        'fontFamily': 'Calibri',
        'padding': '5px'
    },
    children=[
        # Main Card
        html.Div(
            style={
                'backgroundColor': 'white',
                'borderRadius': '5px',
                'overflow': 'hidden'
            },
            children=[
                # Section Header
                html.Div([
                    html.H3(
                        children='8. Метилирование, обмен холина и метионина', 
                        style={
                            'textAlign': 'center',
                            'margin': '0px',
                            'lineHeight': 'normal',
                            'display': 'inline-block',
                            'verticalAlign': 'center',
                            'fontWeight': '600',
                            'fontSize': '19px'
                        }
                    )],
                    style={
                        'width': '100%',
                        'backgroundColor': '#2563eb',
                        'borderRadius': '5px 5px 0px 0px', 
                        'color': 'white',
                        'fontFamily': 'Calibri',
                        'margin': '0px',
                        'height': '35px',
                        'lineHeight': '35px',
                        'textAlign': 'center',
                        'marginTop': '20px'
                    }
                ),
                
                # Table Content
                html.Div(
                    style={'padding': '10px 0px'},
                    children=[
                        # Table Headers
                        html.Div(
                            style={
                                'display': 'grid',
                                'gridTemplateColumns': 'repeat(13, minmax(0, 1fr))',
                                'gap': '10px',
                                'fontWeight': '500',
                                'color': "#4D5052",
                                'backgroundColor': '#f8f9fa',
                                'padding': '8px',
                                'borderRadius': '5px',
                                'margin': '0px',
                                'fontSize': '14px',
                                'fontFamily': 'Calibri'
                            },
                            children=[
                                html.Div("Показатель", style={'gridColumn': 'span 3'}),
                                html.Div("Результат", style={'gridColumn': 'span 2', 'textAlign': 'center'}),
                                html.Div("Статус", style={'gridColumn': 'span 1', 'textAlign': 'center'}),
                                html.Div("Норма", style={'gridColumn': 'span 2', 'textAlign': 'center'}),
                                html.Div("Что это отражает?", style={'gridColumn': 'span 5'}),
                            ]
                        ),
                        
                        # Data Rows
                        *[
                            html.Div(
                                style={
                                    'display': 'grid',
                                    'gridTemplateColumns': 'repeat(13, minmax(0, 1fr))',
                                    'gap': '10px',
                                    'padding': '8px 10px',
                                    'alignItems': 'center',
                                    'borderBottom': '1px solid #e9ecef',
                                    'fontFamily': 'Calibri'
                                },
                                children=[
                                    html.Div(
                                        item["name"],
                                        style={
                                            'gridColumn': 'span 3',
                                            'fontWeight': '600',
                                            
                                            'fontSize': '14px',
                                            'color': '#212529'
                                        }
                                    ),
                                    html.Div(
                                        style={
                                            'gridColumn': 'span 2',
                                            'display': 'flex',
                                            'alignItems': 'center',
                                            'justifyContent': 'center',
                                            'gap': '4px'
                                        },
                                        children=[
                                            html.Div(
                                                f"{item['value']}",
                                                style={
                                                    'fontWeight': 'bold',
                                                    'fontSize': '15px',
                                                    'color': {
                                                        'blue': '#2563eb',
                                                        'red': '#dc3545',
                                                        'green': '#212529'
                                                        }[get_status_color(item["value"], item["norm"])]
                                                }
                                            ),
                                            html.Div(
                                                style={
                                                    'width': '0',
                                                    'height': '0',
                                                    'borderLeft': '5px solid transparent',
                                                    'borderRight': '5px solid transparent',
                                                    'borderTop': '8px solid #2563eb' if get_status_color(item['value'], item['norm']) == 'blue' else 'none',
                                                    'borderBottom': '8px solid #dc3545' if get_status_color(item['value'], item['norm']) == 'red' else 'none',
                                                    'visibility': 'visible' if get_status_color(item['value'], item['norm']) in ['red', 'blue'] else 'hidden',
                                                    'marginLeft': '4px'
                                                }
                                            )
                                        ]
                                    ),
                                    
                                    html.Div(
                                        style={
                                            'gridColumn': 'span 1',
                                            'textAlign': 'center',
                                            'justifySelf': 'center',
                                        },
                                        children=html.Span(
                                            get_status_text(item["value"], item["norm"]),
                                            style={
                                                'padding': '3px 8px',
                                                'borderRadius': '12px',
                                                'fontSize': '14px',
                                                'fontWeight': '500',
                                                'backgroundColor': {
                                                    'blue': '#e7f1ff',
                                                    'red': '#f8d7da',
                                                    'green': '#e6f7ee'
                                                }[get_status_color(item["value"], item["norm"])],
                                                'color': {
                                                    'blue': '#2563eb',
                                                    'red': '#dc3545',
                                                    'green': '#198754'
                                                }[get_status_color(item["value"], item["norm"])]
                                            }
                                        )
                                    ),
                                    html.Div(
                                        f"{item['norm']}",
                                        style={
                                            'gridColumn': 'span 2',
                                            'textAlign': 'center',
                                            
                                            'fontSize': '14px',
                                            'color': '#6c757d',
                                            'alignItems': 'center'
                                        }
                                    ),
                                    html.Div(
                                        item["description"],
                                        style={
                                            'gridColumn': 'span 5',
                                            'color': '#6c757d',
                                            'lineHeight': '1.4',
                                            'fontSize': '14px'
                                        }
                                    ),
                                ]
                            )
                            for item in methylation_data
                        ],
                    ]
                ),
                
                
            ]
        )
    ]
),      
                
                        
         
                             html.Div([
                        html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
                        style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"left",'font-style':'italic','margin-top':'5px','width':'85%'}),
                        html.P('|6',
                            style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"right",'font-style':'italic','margin-top':'5px','width':'10%','margin-top':'15px'}),
                    ], style={'page-break-after': 'always','margin':'0px','display':'flex','justify-content':'space-between','width':'100%','margin-top':'200px'}), 
    
           
               html.Div([
                html.Div([
                    html.B(f"Дата: {date}",style={'margin':'0px','font-size':'18px','font-family':'Calibri'}),
                    html.Div([
                        html.B(f'Пациент: {name}',style={'margin':'0px','font-size':'18px','font-family':'Calibri'}),
                    ],style={'margin-top':'10px'}),
                ], style={'width':'33.3%'}),
                html.Div([
                    html.B("MetaboScan-Test01",style={'margin':'0px','font-size':'18px','font-family':'Calibri','color':'#FFFFFF'}),
                ], style={'width':'33.3%','text-align':'center'}),
                html.Div([
                    html.Img(src=app.get_asset_url('logo.jpg'),style={'height':'54px','float':'right'}),
                ], style={'width':'33.3%'}),
            ], style={'display':'flex', 'justify-content':'space-between','width':'100%','height':'54px','color':'#2563eb'}),

           
           html.Div(
    style={
        'width': '100%',
        'fontFamily': 'Calibri',
        'padding': '5px'
    },
    children=[
        # Main Card
        html.Div(
            style={
                'backgroundColor': 'white',
                'borderRadius': '5px',
                'overflow': 'hidden'
            },
            children=[
                # Section Header
                html.Div([
                    html.H3(
                        children='7. Воспаление, стресс и нейромедиаторный баланс', 
                        style={
                            'textAlign': 'center',
                            'margin': '0px',
                            'lineHeight': 'normal',
                            'display': 'inline-block',
                            'verticalAlign': 'center',
                            'fontWeight': '600',
                            'fontSize': '19px'
                        }
                    )],
                    style={
                        'width': '100%',
                        'backgroundColor': '#2563eb',
                        'borderRadius': '5px 5px 0px 0px', 
                        'color': 'white',
                        'fontFamily': 'Calibri',
                        'margin': '0px',
                        'height': '35px',
                        'lineHeight': '35px',
                        'textAlign': 'center',
                        'marginTop': '0px'
                    }
                ),
                
                # Table Content
                html.Div(
                    style={'padding': '10px 0px'},
                    children=[
                        # Table Headers
                        html.Div(
                            style={
                                'display': 'grid',
                                'gridTemplateColumns': 'repeat(13, minmax(0, 1fr))',
                                'gap': '10px',
                                'fontWeight': '500',
                                'color': "#4D5052",
                                'backgroundColor': '#f8f9fa',
                                'padding': '8px',
                                'borderRadius': '5px',
                                'margin': '0px',
                                'fontSize': '14px',
                                'fontFamily': 'Calibri'
                            },
                            children=[
                                html.Div("Показатель", style={'gridColumn': 'span 3'}),
                                html.Div("Результат", style={'gridColumn': 'span 2', 'textAlign': 'center'}),
                                html.Div("Статус", style={'gridColumn': 'span 1', 'textAlign': 'center'}),
                                html.Div("Норма", style={'gridColumn': 'span 2', 'textAlign': 'center'}),
                                html.Div("Что это отражает?", style={'gridColumn': 'span 5'}),
                            ]
                        ),
                        
                        # Data Rows
                        *[
                            html.Div(
                                style={
                                    'display': 'grid',
                                    'gridTemplateColumns': 'repeat(13, minmax(0, 1fr))',
                                    'gap': '10px',
                                    'padding': '8px 10px',
                                    'alignItems': 'center',
                                    'borderBottom': '1px solid #e9ecef',
                                    'fontFamily': 'Calibri'
                                },
                                children=[
                                    html.Div(
                                        item["name"],
                                        style={
                                            'gridColumn': 'span 3',
                                            'fontWeight': '600',
                                            
                                            'fontSize': '14px',
                                            'color': '#212529'
                                        }
                                    ),
                                    html.Div(
                                        style={
                                            'gridColumn': 'span 2',
                                            'display': 'flex',
                                            'alignItems': 'center',
                                            'justifyContent': 'center',
                                            'gap': '4px'
                                        },
                                        children=[
                                            html.Div(
                                                f"{item['value']}",
                                                style={
                                                    'fontWeight': 'bold',
                                                    'fontSize': '15px',
                                                    'color': {
                                                        'blue': '#2563eb',
                                                        'red': '#dc3545',
                                                        'green': '#212529'
                                                        }[get_status_color(item["value"], item["norm"])]
                                                }
                                            ),
                                            html.Div(
                                                style={
                                                    'width': '0',
                                                    'height': '0',
                                                    'borderLeft': '5px solid transparent',
                                                    'borderRight': '5px solid transparent',
                                                    'borderTop': '8px solid #2563eb' if get_status_color(item['value'], item['norm']) == 'blue' else 'none',
                                                    'borderBottom': '8px solid #dc3545' if get_status_color(item['value'], item['norm']) == 'red' else 'none',
                                                    'visibility': 'visible' if get_status_color(item['value'], item['norm']) in ['red', 'blue'] else 'hidden',
                                                    'marginLeft': '4px'
                                                }
                                            )
                                        ]
                                    ),
                                    
                                    html.Div(
                                        style={
                                            'gridColumn': 'span 1',
                                            'textAlign': 'center',
                                            'justifySelf': 'center',
                                        },
                                        children=html.Span(
                                            get_status_text(item["value"], item["norm"]),
                                            style={
                                                'padding': '3px 8px',
                                                'borderRadius': '12px',
                                                'fontSize': '14px',
                                                'fontWeight': '500',
                                                'backgroundColor': {
                                                    'blue': '#e7f1ff',
                                                    'red': '#f8d7da',
                                                    'green': '#e6f7ee'
                                                }[get_status_color(item["value"], item["norm"])],
                                                'color': {
                                                    'blue': '#2563eb',
                                                    'red': '#dc3545',
                                                    'green': '#198754'
                                                }[get_status_color(item["value"], item["norm"])]
                                            }
                                        )
                                    ),
                                    html.Div(
                                        f"{item['norm']}",
                                        style={
                                            'gridColumn': 'span 2',
                                            'textAlign': 'center',
                                            
                                            'fontSize': '14px',
                                            'color': '#6c757d',
                                            'alignItems': 'center'
                                        }
                                    ),
                                    html.Div(
                                        item["description"],
                                        style={
                                            'gridColumn': 'span 5',
                                            'color': '#6c757d',
                                            'lineHeight': '1.4',
                                            'fontSize': '14px'
                                        }
                                    ),
                                ]
                            )
                            for item in inflammation_data
                        ],
                    ]
                ),
                
                
            ]
        )
    ]
),
           
                    html.Div([
                        html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
                        style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"left",'font-style':'italic','margin-top':'5px','width':'85%'}),
                        html.P('|7',
                            style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"right",'font-style':'italic','margin-top':'5px','width':'10%','margin-top':'15px'}),
                    ], style={'page-break-after': 'always','margin':'0px','display':'flex','justify-content':'space-between','width':'100%','margin-top':'70px'}),      
    
                            html.Div([
                html.Div([
                    html.B(f"Дата: {date}",style={'margin':'0px','font-size':'18px','font-family':'Calibri'}),
                    html.Div([
                        html.B(f'Пациент: {name}',style={'margin':'0px','font-size':'18px','font-family':'Calibri'}),
                    ],style={'margin-top':'10px'}),
                ], style={'width':'33.3%'}),
                html.Div([
                    html.B("MetaboScan-Test01",style={'margin':'0px','font-size':'18px','font-family':'Calibri','color':'#FFFFFF'}),
                ], style={'width':'33.3%','text-align':'center'}),
                html.Div([
                    html.Img(src=app.get_asset_url('logo.jpg'),style={'height':'54px','float':'right'}),
                ], style={'width':'33.3%'}),
            ], style={'display':'flex', 'justify-content':'space-between','width':'100%','height':'54px','color':'#2563eb'}),

        html.Div(
    style={
        'width': '100%',
        'fontFamily': 'Calibri',
        'padding': '5px'
    },
    children=[
        # Main Card
        html.Div(
            style={
                'backgroundColor': 'white',
                'borderRadius': '5px',
                'overflow': 'hidden'
            },
            children=[
                # Section Header
                html.Div([
                    html.H3(
                        children='6. Состояние сосудистой системы и эндотелиальной функции', 
                        style={
                            'textAlign': 'center',
                            'margin': '0px',
                            'lineHeight': 'normal',
                            'display': 'inline-block',
                            'verticalAlign': 'center',
                            'fontWeight': '600',
                            'fontSize': '19px'
                        }
                    )],
                    style={
                        'width': '100%',
                        'backgroundColor': '#2563eb',
                        'borderRadius': '5px 5px 0px 0px', 
                        'color': 'white',
                        'fontFamily': 'Calibri',
                        'margin': '0px',
                        'height': '35px',
                        'lineHeight': '35px',
                        'textAlign': 'center',
                        'marginTop': '0px'
                    }
                ),
                
                # Table Content
                html.Div(
                    style={'padding': '10px 0px'},
                    children=[
                        # Table Headers
                        html.Div(
                            style={
                                'display': 'grid',
                                'gridTemplateColumns': 'repeat(13, minmax(0, 1fr))',
                                'gap': '10px',
                                'fontWeight': '500',
                                'color': "#4D5052",
                                'backgroundColor': '#f8f9fa',
                                'padding': '8px',
                                'borderRadius': '5px',
                                'margin': '0px',
                                'fontSize': '14px',
                                'fontFamily': 'Calibri'
                            },
                            children=[
                                html.Div("Показатель", style={'gridColumn': 'span 3'}),
                                html.Div("Результат", style={'gridColumn': 'span 2', 'textAlign': 'center'}),
                                html.Div("Статус", style={'gridColumn': 'span 1', 'textAlign': 'center'}),
                                html.Div("Норма", style={'gridColumn': 'span 2', 'textAlign': 'center'}),
                                html.Div("Что это отражает?", style={'gridColumn': 'span 5'}),
                            ]
                        ),
                        
                        # Data Rows
                        *[
                            html.Div(
                                style={
                                    'display': 'grid',
                                    'gridTemplateColumns': 'repeat(13, minmax(0, 1fr))',
                                    'gap': '10px',
                                    'padding': '8px 10px',
                                    'alignItems': 'center',
                                    'borderBottom': '1px solid #e9ecef',
                                    'fontFamily': 'Calibri'
                                },
                                children=[
                                    html.Div(
                                        item["name"],
                                        style={
                                            'gridColumn': 'span 3',
                                            'fontWeight': '600',
                                            
                                            'fontSize': '14px',
                                            'color': '#212529'
                                        }
                                    ),
                                    html.Div(
                                        style={
                                            'gridColumn': 'span 2',
                                            'display': 'flex',
                                            'alignItems': 'center',
                                            'justifyContent': 'center',
                                            'gap': '4px'
                                        },
                                        children=[
                                            html.Div(
                                                f"{item['value']}",
                                                style={
                                                    'fontWeight': 'bold',
                                                    'fontSize': '15px',
                                                    'color': {
                                                        'blue': '#2563eb',
                                                        'red': '#dc3545',
                                                        'green': '#212529'
                                                        }[get_status_color(item["value"], item["norm"])]
                                                }
                                            ),
                                            html.Div(
                                                style={
                                                    'width': '0',
                                                    'height': '0',
                                                    'borderLeft': '5px solid transparent',
                                                    'borderRight': '5px solid transparent',
                                                    'borderTop': '8px solid #2563eb' if get_status_color(item['value'], item['norm']) == 'blue' else 'none',
                                                    'borderBottom': '8px solid #dc3545' if get_status_color(item['value'], item['norm']) == 'red' else 'none',
                                                    'visibility': 'visible' if get_status_color(item['value'], item['norm']) in ['red', 'blue'] else 'hidden',
                                                    'marginLeft': '4px'
                                                }
                                            )
                                        ]
                                    ),
                                    
                                    html.Div(
                                        style={
                                            'gridColumn': 'span 1',
                                            'textAlign': 'center',
                                            'justifySelf': 'center',
                                        },
                                        children=html.Span(
                                            get_status_text(item["value"], item["norm"]),
                                            style={
                                                'padding': '3px 8px',
                                                'borderRadius': '12px',
                                                'fontSize': '14px',
                                                'fontWeight': '500',
                                                'backgroundColor': {
                                                    'blue': '#e7f1ff',
                                                    'red': '#f8d7da',
                                                    'green': '#e6f7ee'
                                                }[get_status_color(item["value"], item["norm"])],
                                                'color': {
                                                    'blue': '#2563eb',
                                                    'red': '#dc3545',
                                                    'green': '#198754'
                                                }[get_status_color(item["value"], item["norm"])]
                                            }
                                        )
                                    ),
                                    html.Div(
                                        f"{item['norm']}",
                                        style={
                                            'gridColumn': 'span 2',
                                            'textAlign': 'center',
                                            
                                            'fontSize': '14px',
                                            'color': '#6c757d',
                                            'alignItems': 'center'
                                        }
                                    ),
                                    html.Div(
                                        item["description"],
                                        style={
                                            'gridColumn': 'span 5',
                                            'color': '#6c757d',
                                            'lineHeight': '1.4',
                                            'fontSize': '14px'
                                        }
                                    ),
                                ]
                            )
                            for item in vascular_data
                        ],
                    ]
                ),
                
                
            ]
        )
    ]
),  
                            html.Div([
                        html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
                        style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"left",'font-style':'italic','margin-top':'5px','width':'85%'}),
                        html.P('|8',
                            style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"right",'font-style':'italic','margin-top':'5px','width':'10%','margin-top':'15px'}),
                    ], style={'page-break-after': 'always','margin':'0px','display':'flex','justify-content':'space-between','width':'100%','margin-top':'285px'}),      
    
                html.Div([
                html.Div([
                    html.B(f"Дата: {date}",style={'margin':'0px','font-size':'18px','font-family':'Calibri'}),
                    html.Div([
                        html.B(f'Пациент: {name}',style={'margin':'0px','font-size':'18px','font-family':'Calibri'}),
                    ],style={'margin-top':'10px'}),
                ], style={'width':'33.3%'}),
                html.Div([
                    html.B("MetaboScan-Test01",style={'margin':'0px','font-size':'18px','font-family':'Calibri','color':'#FFFFFF'}),
                ], style={'width':'33.3%','text-align':'center'}),
                html.Div([
                    html.Img(src=app.get_asset_url('logo.jpg'),style={'height':'54px','float':'right'}),
                ], style={'width':'33.3%'}),
            ], style={'display':'flex', 'justify-content':'space-between','width':'100%','height':'54px','color':'#2563eb'}),

    
    html.Div(
    style={
        'width': '100%',
        'fontFamily': 'Calibri',
        'padding': '5px'
    },
    children=[
        # Main Card
        html.Div(
            style={
                'backgroundColor': 'white',
                'borderRadius': '5px',
                'overflow': 'hidden'
            },
            children=[
                # Section Header
                html.Div([
                    html.H3(
                        children='9. Энергетический обмен, цикл Кребса и баланс аминокислот', 
                        style={
                            'textAlign': 'center',
                            'margin': '0px',
                            'lineHeight': 'normal',
                            'display': 'inline-block',
                            'verticalAlign': 'center',
                            'fontWeight': '600',
                            'fontSize': '19px'
                        }
                    )],
                    style={
                        'width': '100%',
                        'backgroundColor': '#2563eb',
                        'borderRadius': '5px 5px 0px 0px', 
                        'color': 'white',
                        'fontFamily': 'Calibri',
                        'margin': '0px',
                        'height': '35px',
                        'lineHeight': '35px',
                        'textAlign': 'center',
                        'marginTop': '0px'
                    }
                ),
                
                # Table Content
                html.Div(
                    style={'padding': '10px 0px'},
                    children=[
                        # Table Headers
                        html.Div(
                            style={
                                'display': 'grid',
                                'gridTemplateColumns': 'repeat(13, minmax(0, 1fr))',
                                'gap': '10px',
                                'fontWeight': '500',
                                'color': "#4D5052",
                                'backgroundColor': '#f8f9fa',
                                'padding': '8px',
                                'borderRadius': '5px',
                                'margin': '0px',
                                'fontSize': '14px',
                                'fontFamily': 'Calibri'
                            },
                            children=[
                                html.Div("Показатель", style={'gridColumn': 'span 3'}),
                                html.Div("Результат", style={'gridColumn': 'span 2', 'textAlign': 'center'}),
                                html.Div("Статус", style={'gridColumn': 'span 1', 'textAlign': 'center'}),
                                html.Div("Норма", style={'gridColumn': 'span 2', 'textAlign': 'center'}),
                                html.Div("Что это отражает?", style={'gridColumn': 'span 5'}),
                            ]
                        ),
                        
                        # Data Rows
                        *[
                            html.Div(
                                style={
                                    'display': 'grid',
                                    'gridTemplateColumns': 'repeat(13, minmax(0, 1fr))',
                                    'gap': '10px',
                                    'padding': '8px 10px',
                                    'alignItems': 'center',
                                    'borderBottom': '1px solid #e9ecef',
                                    'fontFamily': 'Calibri'
                                },
                                children=[
                                    html.Div(
                                        item["name"],
                                        style={
                                            'gridColumn': 'span 3',
                                            'fontWeight': '600',
                                            
                                            'fontSize': '14px',
                                            'color': '#212529'
                                        }
                                    ),
                                    html.Div(
                                        style={
                                            'gridColumn': 'span 2',
                                            'display': 'flex',
                                            'alignItems': 'center',
                                            'justifyContent': 'center',
                                            'gap': '4px'
                                        },
                                        children=[
                                            html.Div(
                                                f"{item['value']}",
                                                style={
                                                    'fontWeight': 'bold',
                                                    'fontSize': '15px',
                                                    'color': {
                                                        'blue': '#2563eb',
                                                        'red': '#dc3545',
                                                        'green': '#212529'
                                                        }[get_status_color(item["value"], item["norm"])]
                                                }
                                            ),
                                            html.Div(
                                                style={
                                                    'width': '0',
                                                    'height': '0',
                                                    'borderLeft': '5px solid transparent',
                                                    'borderRight': '5px solid transparent',
                                                    'borderTop': '8px solid #2563eb' if get_status_color(item['value'], item['norm']) == 'blue' else 'none',
                                                    'borderBottom': '8px solid #dc3545' if get_status_color(item['value'], item['norm']) == 'red' else 'none',
                                                    'visibility': 'visible' if get_status_color(item['value'], item['norm']) in ['red', 'blue'] else 'hidden',
                                                    'marginLeft': '4px'
                                                }
                                            )
                                        ]
                                    ),
                                    
                                    html.Div(
                                        style={
                                            'gridColumn': 'span 1',
                                            'textAlign': 'center',
                                            'justifySelf': 'center',
                                        },
                                        children=html.Span(
                                            get_status_text(item["value"], item["norm"]),
                                            style={
                                                'padding': '3px 8px',
                                                'borderRadius': '12px',
                                                'fontSize': '14px',
                                                'fontWeight': '500',
                                                'backgroundColor': {
                                                    'blue': '#e7f1ff',
                                                    'red': '#f8d7da',
                                                    'green': '#e6f7ee'
                                                }[get_status_color(item["value"], item["norm"])],
                                                'color': {
                                                    'blue': '#2563eb',
                                                    'red': '#dc3545',
                                                    'green': '#198754'
                                                }[get_status_color(item["value"], item["norm"])]
                                            }
                                        )
                                    ),
                                    html.Div(
                                        f"{item['norm']}",
                                        style={
                                            'gridColumn': 'span 2',
                                            'textAlign': 'center',
                                            
                                            'fontSize': '14px',
                                            'color': '#6c757d',
                                            'alignItems': 'center'
                                        }
                                    ),
                                    html.Div(
                                        item["description"],
                                        style={
                                            'gridColumn': 'span 5',
                                            'color': '#6c757d',
                                            'lineHeight': '1.4',
                                            'fontSize': '14px'
                                        }
                                    ),
                                ]
                            )
                            for item in energy_metabolism_data
                        ],
                    ]
                ),
                
                
            ]
        )
    ]
),
                                 
                                                     html.Div([
                        html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
                        style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"left",'font-style':'italic','margin-top':'5px','width':'85%'}),
                        html.P('|9',
                            style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"right",'font-style':'italic','margin-top':'5px','width':'10%','margin-top':'15px'}),
                    ], style={'page-break-after': 'always','margin':'0px','display':'flex','justify-content':'space-between','width':'100%','margin-top':'75px'}),      
    
    
                html.Div([
                html.Div([
                    html.B(f"Дата: {date}",style={'margin':'0px','font-size':'18px','font-family':'Calibri'}),
                    html.Div([
                        html.B(f'Пациент: {name}',style={'margin':'0px','font-size':'18px','font-family':'Calibri'}),
                    ],style={'margin-top':'10px'}),
                ], style={'width':'33.3%'}),
                html.Div([
                    html.B("MetaboScan-Test01",style={'margin':'0px','font-size':'18px','font-family':'Calibri','color':'#FFFFFF'}),
                ], style={'width':'33.3%','text-align':'center'}),
                html.Div([
                    html.Img(src=app.get_asset_url('logo.jpg'),style={'height':'54px','float':'right'}),
                ], style={'width':'33.3%'}),
            ], style={'display':'flex', 'justify-content':'space-between','width':'100%','height':'54px','color':'#2563eb'}),

                                 
                                            html.Div(
    style={
        'width': '100%',
        'fontFamily': 'Calibri',
        'padding': '5px'
    },
    children=[
        # Main Card
        html.Div(
            style={
                'backgroundColor': 'white',
                'borderRadius': '5px',
                'overflow': 'hidden'
            },
            children=[
                # Section Header
                html.Div([
                    html.H3(
                        children='10. Здоровье митохондрий и β-окисление жирных кислот', 
                        style={
                            'textAlign': 'center',
                            'margin': '0px',
                            'lineHeight': 'normal',
                            'display': 'inline-block',
                            'verticalAlign': 'center',
                            'fontWeight': '600',
                            'fontSize': '19px'
                        }
                    )],
                    style={
                        'width': '100%',
                        'backgroundColor': '#2563eb',
                        'borderRadius': '5px 5px 0px 0px', 
                        'color': 'white',
                        'fontFamily': 'Calibri',
                        'margin': '0px',
                        'height': '35px',
                        'lineHeight': '35px',
                        'textAlign': 'center',
                        'marginTop': '0px'
                    }
                ),
                
                # Table Content
                html.Div(
                    style={'padding': '10px 0px'},
                    children=[
                        # Table Headers
                        html.Div(
                            style={
                                'display': 'grid',
                                'gridTemplateColumns': 'repeat(13, minmax(0, 1fr))',
                                'gap': '10px',
                                'fontWeight': '500',
                                'color': "#4D5052",
                                'backgroundColor': '#f8f9fa',
                                'padding': '8px',
                                'borderRadius': '5px',
                                'margin': '0px',
                                'fontSize': '14px',
                                'fontFamily': 'Calibri'
                            },
                            children=[
                                html.Div("Показатель", style={'gridColumn': 'span 3'}),
                                html.Div("Результат", style={'gridColumn': 'span 2', 'textAlign': 'center'}),
                                html.Div("Статус", style={'gridColumn': 'span 1', 'textAlign': 'center'}),
                                html.Div("Норма", style={'gridColumn': 'span 2', 'textAlign': 'center'}),
                                html.Div("Что это отражает?", style={'gridColumn': 'span 5'}),
                            ]
                        ),
                        
                        # Data Rows
                        *[
                            html.Div(
                                style={
                                    'display': 'grid',
                                    'gridTemplateColumns': 'repeat(13, minmax(0, 1fr))',
                                    'gap': '10px',
                                    'padding': '8px 10px',
                                    'alignItems': 'center',
                                    'borderBottom': '1px solid #e9ecef',
                                    'fontFamily': 'Calibri'
                                },
                                children=[
                                    html.Div(
                                        item["name"],
                                        style={
                                            'gridColumn': 'span 3',
                                            'fontWeight': '600',
                                            
                                            'fontSize': '14px',
                                            'color': '#212529'
                                        }
                                    ),
                                    html.Div(
                                        style={
                                            'gridColumn': 'span 2',
                                            'display': 'flex',
                                            'alignItems': 'center',
                                            'justifyContent': 'center',
                                            'gap': '4px'
                                        },
                                        children=[
                                            html.Div(
                                                f"{item['value']}",
                                                style={
                                                    'fontWeight': 'bold',
                                                    'fontSize': '15px',
                                                    'color': {
                                                        'blue': '#2563eb',
                                                        'red': '#dc3545',
                                                        'green': '#212529'
                                                        }[get_status_color(item["value"], item["norm"])]
                                                }
                                            ),
                                            html.Div(
                                                style={
                                                    'width': '0',
                                                    'height': '0',
                                                    'borderLeft': '5px solid transparent',
                                                    'borderRight': '5px solid transparent',
                                                    'borderTop': '8px solid #2563eb' if get_status_color(item['value'], item['norm']) == 'blue' else 'none',
                                                    'borderBottom': '8px solid #dc3545' if get_status_color(item['value'], item['norm']) == 'red' else 'none',
                                                    'visibility': 'visible' if get_status_color(item['value'], item['norm']) in ['red', 'blue'] else 'hidden',
                                                    'marginLeft': '4px'
                                                }
                                            )
                                        ]
                                    ),
                                    
                                    html.Div(
                                        style={
                                            'gridColumn': 'span 1',
                                            'textAlign': 'center',
                                            'justifySelf': 'center',
                                        },
                                        children=html.Span(
                                            get_status_text(item["value"], item["norm"]),
                                            style={
                                                'padding': '3px 8px',
                                                'borderRadius': '12px',
                                                'fontSize': '14px',
                                                'fontWeight': '500',
                                                'backgroundColor': {
                                                    'blue': '#e7f1ff',
                                                    'red': '#f8d7da',
                                                    'green': '#e6f7ee'
                                                }[get_status_color(item["value"], item["norm"])],
                                                'color': {
                                                    'blue': '#2563eb',
                                                    'red': '#dc3545',
                                                    'green': '#198754'
                                                }[get_status_color(item["value"], item["norm"])]
                                            }
                                        )
                                    ),
                                    html.Div(
                                        f"{item['norm']}",
                                        style={
                                            'gridColumn': 'span 2',
                                            'textAlign': 'center',
                                            
                                            'fontSize': '14px',
                                            'color': '#6c757d',
                                            'alignItems': 'center'
                                        }
                                    ),
                                    html.Div(
                                        item["description"],
                                        style={
                                            'gridColumn': 'span 5',
                                            'color': '#6c757d',
                                            'lineHeight': '1.4',
                                            'fontSize': '14px'
                                        }
                                    ),
                                ]
                            )
                            for item in mitochondrial_data
                        ],
                    ]
                ),
                
                
            ]
        )
    ]
),
                       html.Div([
                        html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
                        style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"left",'font-style':'italic','margin-top':'5px','width':'85%'}),
                        html.P('|10',
                            style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"right",'font-style':'italic','margin-top':'5px','width':'10%','margin-top':'15px'}),
                    ], style={'page-break-after': 'always','margin':'0px','display':'flex','justify-content':'space-between','width':'100%','margin-top':'75px'}),      
                
                
                
    
                html.Div([
                html.Div([
                    html.B(f"Дата: {date}",style={'margin':'0px','font-size':'18px','font-family':'Calibri'}),
                    html.Div([
                        html.B(f'Пациент: {name}',style={'margin':'0px','font-size':'18px','font-family':'Calibri'}),
                    ],style={'margin-top':'10px'}),
                ], style={'width':'33.3%'}),
                html.Div([
                    html.B("MetaboScan-Test01",style={'margin':'0px','font-size':'18px','font-family':'Calibri','color':'#FFFFFF'}),
                ], style={'width':'33.3%','text-align':'center'}),
                html.Div([
                    html.Img(src=app.get_asset_url('logo.jpg'),style={'height':'54px','float':'right'}),
                ], style={'width':'33.3%'}),
            ], style={'display':'flex', 'justify-content':'space-between','width':'100%','height':'54px','color':'#2563eb'}),
   
                                            
                # Table Content
                html.Div(
                    style={'padding': '10px 0px'},
                    children=[
                        # Table Headers
                        html.Div(
                            style={
                                'display': 'grid',
                                'gridTemplateColumns': 'repeat(13, minmax(0, 1fr))',
                                'gap': '10px',
                                'fontWeight': '500',
                                'color': "#4D5052",
                                'backgroundColor': '#f8f9fa',
                                'padding': '8px',
                                'borderRadius': '5px',
                                'margin': '0px',
                                'fontSize': '14px',
                                'fontFamily': 'Calibri'
                            },
                            children=[
                                html.Div("Показатель", style={'gridColumn': 'span 3'}),
                                html.Div("Результат", style={'gridColumn': 'span 2', 'textAlign': 'center'}),
                                html.Div("Статус", style={'gridColumn': 'span 1', 'textAlign': 'center'}),
                                html.Div("Норма", style={'gridColumn': 'span 2', 'textAlign': 'center'}),
                                html.Div("Что это отражает?", style={'gridColumn': 'span 5'}),
                            ]
                        ),
                        
                        # Data Rows
                        *[
                            html.Div(
                                style={
                                    'display': 'grid',
                                    'gridTemplateColumns': 'repeat(13, minmax(0, 1fr))',
                                    'gap': '10px',
                                    'padding': '8px 10px',
                                    'alignItems': 'center',
                                    'borderBottom': '1px solid #e9ecef',
                                    'fontFamily': 'Calibri'
                                },
                                children=[
                                    html.Div(
                                        item["name"],
                                        style={
                                            'gridColumn': 'span 3',
                                            'fontWeight': '600',
                                            
                                            'fontSize': '14px',
                                            'color': '#212529'
                                        }
                                    ),
                                    html.Div(
                                        style={
                                            'gridColumn': 'span 2',
                                            'display': 'flex',
                                            'alignItems': 'center',
                                            'justifyContent': 'center',
                                            'gap': '4px'
                                        },
                                        children=[
                                            html.Div(
                                                f"{item['value']}",
                                                style={
                                                    'fontWeight': 'bold',
                                                    'fontSize': '15px',
                                                    'color': {
                                                        'blue': '#2563eb',
                                                        'red': '#dc3545',
                                                        'green': '#212529'
                                                        }[get_status_color(item["value"], item["norm"])]
                                                }
                                            ),
                                            html.Div(
                                                style={
                                                    'width': '0',
                                                    'height': '0',
                                                    'borderLeft': '5px solid transparent',
                                                    'borderRight': '5px solid transparent',
                                                    'borderTop': '8px solid #2563eb' if get_status_color(item['value'], item['norm']) == 'blue' else 'none',
                                                    'borderBottom': '8px solid #dc3545' if get_status_color(item['value'], item['norm']) == 'red' else 'none',
                                                    'visibility': 'visible' if get_status_color(item['value'], item['norm']) in ['red', 'blue'] else 'hidden',
                                                    'marginLeft': '4px'
                                                }
                                            )
                                        ]
                                    ),
                                    
                                    html.Div(
                                        style={
                                            'gridColumn': 'span 1',
                                            'textAlign': 'center',
                                            'justifySelf': 'center',
                                        },
                                        children=html.Span(
                                            get_status_text(item["value"], item["norm"]),
                                            style={
                                                'padding': '3px 8px',
                                                'borderRadius': '12px',
                                                'fontSize': '14px',
                                                'fontWeight': '500',
                                                'backgroundColor': {
                                                    'blue': '#e7f1ff',
                                                    'red': '#f8d7da',
                                                    'green': '#e6f7ee'
                                                }[get_status_color(item["value"], item["norm"])],
                                                'color': {
                                                    'blue': '#2563eb',
                                                    'red': '#dc3545',
                                                    'green': '#198754'
                                                }[get_status_color(item["value"], item["norm"])]
                                            }
                                        )
                                    ),
                                    html.Div(
                                        f"{item['norm']}",
                                        style={
                                            'gridColumn': 'span 2',
                                            'textAlign': 'center',
                                            
                                            'fontSize': '14px',
                                            'color': '#6c757d',
                                            'alignItems': 'center'
                                        }
                                    ),
                                    html.Div(
                                        item["description"],
                                        style={
                                            'gridColumn': 'span 5',
                                            'color': '#6c757d',
                                            'lineHeight': '1.4',
                                            'fontSize': '14px'
                                        }
                                    ),
                                ]
                            )
                            for item in mytochondrial_data_2
                        ],
                    ]
                ),
                                                       
                    
                    html.Div([
                        html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
                        style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"left",'font-style':'italic','margin-top':'5px','width':'85%'}),
                        html.P('|11',
                            style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"right",'font-style':'italic','margin-top':'5px','width':'10%','margin-top':'15px'}),
                    ], style={'page-break-after':'always','margin':'0px','display':'flex','justify-content':'space-between','width':'100%','margin-top':'345px'}), 
                        


                # Header section
                html.Div([
                    html.Div([
                        html.B(f"Дата: {date}", style={'margin':'0px','font-size':'18px','font-family':'Calibri'}),
                        html.Div([
                            html.B(f'Пациент: {name}', style={'margin':'0px','font-size':'18px','font-family':'Calibri'}),
                        ], style={'margin-top':'10px'}),
                    ], style={'width':'33.3%'}),
                    
                    html.Div([
                        html.B("MetaboScan-Test01", style={'margin':'0px','font-size':'18px','font-family':'Calibri','color':'#FFFFFF'}),
                    ], style={'width':'33.3%','text-align':'center'}),
                    
                    html.Div([
                        html.Img(src=app.get_asset_url('logo.jpg'), style={'height':'54px','float':'right'}),
                    ], style={'width':'33.3%'}),
                ], style={'display':'flex', 'justify-content':'space-between','width':'100%','height':'54px','color':'#2563eb'}),
                
                # Health corridor title
                html.Div([
                    html.H3(children='Коридор здоровья', 
                        style={'textAlign':'left','margin':'0px','line-height':'normal',
                                'display':'inline-block','vertical-align':'center'})
                ], style={'width':'100%','background-color':'#2563eb','border-radius':'5px 5px 0px 0px', 
                        'color':'white','font-family':'Calibri','margin':'0px','height':'35px',
                        'line-height':'35px','text-align':'center','margin-top':'5px'}),
                
            
             html.Div([
            # ADD info icon
            
            html.Img(src=app.get_asset_url('info_icon.png'), style={'width':'20px','height':'20px','margin-right':'15px'}),
            
            html.Div('Данные по оценке стандартного отклонения от средних показателей здоровых людей получены из экспериментальных данных образцов биобанка Центра биофармацевтического анализа и метаболомных исследований Сеченовского университета.',
                    style={'color':'black','font-family':'Calibri','font-size':'13px','text-align':"left", 'margin': '0px !important'}),
            ], style={'display': 'flex','margin-top':'10px','margin-bottom':'10px', 'flex-direction': 'row','align-items': 'center', 'width':'fit-content', "borderRadius": "0.5rem", 'padding': '5px 7px 5px 15px', 'border': '2px solid rgb(255, 184, 113)', 'background-color': '#fffede'}),
 
            
            html.Div([
                html.Div([
                    # First image container
                    html.Div([
                        html.Img(
                            src=fig_phenylalanine_metabolism,
                            style={
                                'height': 'fit-content',
                                'width': '100%',
                                'object-fit': 'contain'
                            }
                        )
                    ], style={
                        'border': '1px solid #e5e7eb',
                        'borderRadius': '12px',
                        'padding': '10px 5px',
                        'margin-right': '10px',
                        'width': '50%',  # Changed from 400px to 50%
                        'object-fit': 'contain',
                        'background-color': 'white',
                        'display': 'inline-block'  # Added for side-by-side layout
                    }),
                    
                    # Second image container
                    html.Div([
                        html.Img(
                            src=fig_histidine_metabolism,
                            style={
                                'height': 'fit-content',
                                'width': '100%',
                                'object-fit': 'contain'
                            }
                        )
                    ], style={
                        'border': '1px solid #e5e7eb',
                        'borderRadius': '12px',
                        'padding': '10px 5px',
                        'width': '50%',  # Changed from 400px to 50%
                        'object-fit': 'contain',
                        'background-color': 'white',
                        'display': 'inline-block'  # Added for side-by-side layout
                    })
                ], style={
                    'margin-top': '10px',
                    'width': '765px',
                    'white-space': 'nowrap'  # Prevents wrapping to next line
                })
            ]),
                        html.Div([
                html.Div([
                    # First image container
                    html.Div([
                        html.Img(
                            src=fig_methionine_metabolism,
                            style={
                                'height': 'fit-content',
                                'width': '100%',
                                'object-fit': 'contain'
                            }
                        )
                    ], style={
                        'border': '1px solid #e5e7eb',
                        'borderRadius': '12px',
                        'padding': '10px 5px',
                        'margin-right': '10px',
                        'width': '50%',  # Changed from 400px to 50%
                        'object-fit': 'contain',
                        'background-color': 'white',
                        'display': 'inline-block'  # Added for side-by-side layout
                    }),
                    
                    # Second image container
                    html.Div([
                        html.Img(
                            src=fig_kynurenine_pathway,
                            style={
                                'height': 'fit-content',
                                'width': '100%',
                                'object-fit': 'contain'
                            }
                        )
                    ], style={
                        'border': '1px solid #e5e7eb',
                        'borderRadius': '12px',
                        'padding': '10px 5px',
                        'width': '50%',  # Changed from 400px to 50%
                        'object-fit': 'contain',
                        'background-color': 'white',
                        'display': 'inline-block'  # Added for side-by-side layout
                    })
                ], style={
                    'margin-top': '10px',
                    'width': '765px',
                    'white-space': 'nowrap'  # Prevents wrapping to next line
                })
            ]),
                                    html.Div([
                html.Div([
                    # First image container
                    html.Div([
                        html.Img(
                            src=fig_serotonin_pathway,
                            style={
                                'height': 'fit-content',
                                'width': '100%',
                                'object-fit': 'contain'
                            }
                        )
                    ], style={
                        'border': '1px solid #e5e7eb',
                        'borderRadius': '12px',
                        'padding': '10px 5px',
                        'margin-right': '10px',
                        'width': '50%',  # Changed from 400px to 50%
                        'object-fit': 'contain',
                        'background-color': 'white',
                        'display': 'inline-block'  # Added for side-by-side layout
                    }),
                    
                    # Second image container
                    html.Div([
                        html.Img(
                            src=fig_indole_pathway,
                            style={
                                'height': 'fit-content',
                                'width': '100%',
                                'object-fit': 'contain'
                            }
                        )
                    ], style={
                        'border': '1px solid #e5e7eb',
                        'borderRadius': '12px',
                        'padding': '10px 5px',
                        'width': '50%',  # Changed from 400px to 50%
                        'object-fit': 'contain',
                        'background-color': 'white',
                        'display': 'inline-block'  # Added for side-by-side layout
                    })
                ], style={
                    'margin-top': '10px',
                    'width': '765px',
                    'white-space': 'nowrap'  # Prevents wrapping to next line
                })
            ]),               
                    
              html.Div([
                        html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
                        style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"left",'font-style':'italic','margin-top':'5px','width':'85%'}),
                        html.P('|12',
                            style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"right",'font-style':'italic','margin-top':'5px','width':'10%','margin-top':'15px'}),
                    ], style={'page-break-after':'always','margin':'0px','display':'flex','justify-content':'space-between','width':'100%','margin-top':'30px'}), 
                        


                # Header section
                html.Div([
                    html.Div([
                        html.B(f"Дата: {date}", style={'margin':'0px','font-size':'18px','font-family':'Calibri'}),
                        html.Div([
                            html.B(f'Пациент: {name}', style={'margin':'0px','font-size':'18px','font-family':'Calibri'}),
                        ], style={'margin-top':'10px'}),
                    ], style={'width':'33.3%'}),
                    
                    html.Div([
                        html.B("MetaboScan-Test01", style={'margin':'0px','font-size':'18px','font-family':'Calibri','color':'#FFFFFF'}),
                    ], style={'width':'33.3%','text-align':'center'}),
                    
                    html.Div([
                        html.Img(src=app.get_asset_url('logo.jpg'), style={'height':'54px','float':'right'}),
                    ], style={'width':'33.3%'}),
                ], style={'display':'flex', 'justify-content':'space-between','width':'100%','height':'54px','color':'#2563eb'}),
                
                # Health corridor title
                html.Div([
                    html.H3(children='Коридор здоровья', 
                        style={'textAlign':'left','margin':'0px','line-height':'normal',
                                'display':'inline-block','vertical-align':'center'})
                ], style={'width':'100%','background-color':'#2563eb','border-radius':'5px 5px 0px 0px', 
                        'color':'white','font-family':'Calibri','margin':'0px','height':'35px',
                        'line-height':'35px','text-align':'center','margin-top':'5px'}),
                
            
             html.Div([
            # ADD info icon
            
            html.Img(src=app.get_asset_url('info_icon.png'), style={'width':'20px','height':'20px','margin-right':'15px'}),
            
            html.Div('Данные по оценке стандартного отклонения от средних показателей здоровых людей получены из экспериментальных данных образцов биобанка Центра биофармацевтического анализа и метаболомных исследований Сеченовского университета.',
                    style={'color':'black','font-family':'Calibri','font-size':'13px','text-align':"left", 'margin': '0px !important'}),
            ], style={'display': 'flex','margin-top':'10px','margin-bottom':'10px', 'flex-direction': 'row','align-items': 'center', 'width':'fit-content', "borderRadius": "0.5rem", 'padding': '5px 7px 5px 15px', 'border': '2px solid rgb(255, 184, 113)', 'background-color': '#fffede'}),
 
            
            html.Div([
                html.Div([
                    # First image container
                    html.Div([
                        html.Img(
                            src=fig_arginine_metabolism,
                            style={
                                'height': 'fit-content',
                                'width': '100%',
                                'object-fit': 'contain'
                            }
                        )
                    ], style={
                        'border': '1px solid #e5e7eb',
                        'borderRadius': '12px',
                        'padding': '10px 5px',
                        'margin-right': '10px',
                        'width': '50%',  # Changed from 400px to 50%
                        'object-fit': 'contain',
                        'background-color': 'white',
                        'display': 'inline-block'  # Added for side-by-side layout
                    }),
                    
                    # Second image container
                    html.Div([
                        html.Img(
                            src=fig_acylcarnitine_ratios,
                            style={
                                'height': 'fit-content',
                                'width': '100%',
                                'object-fit': 'contain'
                            }
                        )
                    ], style={
                        'border': '1px solid #e5e7eb',
                        'borderRadius': '12px',
                        'padding': '10px 5px',
                        'width': '50%',  # Changed from 400px to 50%
                        'object-fit': 'contain',
                        'background-color': 'white',
                        'display': 'inline-block'  # Added for side-by-side layout
                    })
                ], style={
                    'margin-top': '10px',
                    'width': '765px',
                    'white-space': 'nowrap'  # Prevents wrapping to next line
                })
            ]),
                        html.Div([
                html.Div([
                    # First image container
                    html.Div([
                        html.Img(
                            src=fig_short_chain_acyl,
                            style={
                                'height': 'fit-content',
                                'width': '100%',
                                'object-fit': 'contain'
                            }
                        )
                    ], style={
                        'border': '1px solid #e5e7eb',
                        'borderRadius': '12px',
                        'padding': '10px 5px',
                        'margin-right': '10px',
                        'width': '50%',  # Changed from 400px to 50%
                        'object-fit': 'contain',
                        'background-color': 'white',
                        'display': 'inline-block'  # Added for side-by-side layout
                    }),
                    
                    # Second image container
                    html.Div([
                        html.Img(
                            src=fig_medium_chain_acyl,
                            style={
                                'height': 'fit-content',
                                'width': '100%',
                                'object-fit': 'contain'
                            }
                        )
                    ], style={
                        'border': '1px solid #e5e7eb',
                        'borderRadius': '12px',
                        'padding': '10px 5px',
                        'width': '50%',  # Changed from 400px to 50%
                        'object-fit': 'contain',
                        'background-color': 'white',
                        'display': 'inline-block'  # Added for side-by-side layout
                    })
                ], style={
                    'margin-top': '10px',
                    'width': '765px',
                    'white-space': 'nowrap'  # Prevents wrapping to next line
                })
            ]),
                                    html.Div([
                html.Div([
                    # First image container
                    html.Div([
                        html.Img(
                            src=fig_long_chain_acyl,
                            style={
                                'height': 'fit-content',
                                'width': '100%',
                                'object-fit': 'contain'
                            }
                        )
                    ], style={
                        'border': '1px solid #e5e7eb',
                        'borderRadius': '12px',
                        'padding': '10px 5px',
                        'margin-right': '10px',
                        'width': '50%',  # Changed from 400px to 50%
                        'object-fit': 'contain',
                        'background-color': 'white',
                        'display': 'inline-block'  # Added for side-by-side layout
                    }),
                    
                    # Second image container
                    html.Div([
                        html.Img(
                            src=fig_other_metabolites,
                            style={
                                'height': 'fit-content',
                                'width': '100%',
                                'object-fit': 'contain'
                            }
                        )
                    ], style={
                        'border': '1px solid #e5e7eb',
                        'borderRadius': '12px',
                        'padding': '10px 5px',
                        'width': '50%',  # Changed from 400px to 50%
                        'object-fit': 'contain',
                        'background-color': 'white',
                        'display': 'inline-block'  # Added for side-by-side layout
                    })
                ], style={
                    'margin-top': '10px',
                    'width': '765px',
                    'white-space': 'nowrap'  # Prevents wrapping to next line
                })
            ]),                           
                       html.Div([
                        html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
                        style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"left",'font-style':'italic','margin-top':'5px','width':'85%'}),
                        html.P('|13',
                            style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"right",'font-style':'italic','margin-top':'5px','width':'10%','margin-top':'15px'}),
                    ], style={'margin':'0px','display':'flex','justify-content':'space-between','width':'100%','margin-top':'30px'}),      
                
                
                # Header section
                html.Div([
                    html.Div([
                        html.B(f"Дата: {date}", style={'margin':'0px','font-size':'18px','font-family':'Calibri'}),
                        html.Div([
                            html.B(f'Пациент: {name}', style={'margin':'0px','font-size':'18px','font-family':'Calibri'}),
                        ], style={'margin-top':'10px'}),
                    ], style={'width':'33.3%'}),
                    
                    html.Div([
                        html.B("MetaboScan-Test01", style={'margin':'0px','font-size':'18px','font-family':'Calibri','color':'#FFFFFF'}),
                    ], style={'width':'33.3%','text-align':'center'}),
                    
                    html.Div([
                        html.Img(src=app.get_asset_url('logo.jpg'), style={'height':'54px','float':'right'}),
                    ], style={'width':'33.3%'}),
                ], style={'display':'flex', 'justify-content':'space-between','width':'100%','height':'54px','color':'#2563eb'}),
                
                # Health corridor title
                html.Div([
                    html.H3(children='Часто задаваемые вопросы', 
                        style={'textAlign':'left','margin':'0px','line-height':'normal',
                                'display':'inline-block','vertical-align':'center'})
                ], style={'width':'100%','background-color':'#2563eb','border-radius':'5px 5px 0px 0px', 
                        'color':'white','font-family':'Calibri','margin':'0px','height':'35px',
                        'line-height':'35px','text-align':'center','margin-top':'5px'}),
                
        # Content
        html.Div(
            style={
                'padding': '15px 0px 0px 0px',
                'backgroundColor': 'white',
                'borderTop': 'none',
            },
            children=[
                # Question
                html.Div(
                    style={
                        'display': 'flex',
                        'gap': '12px',
                        
                    },
                    children=[
                        html.Div(
                            style={
                                'flexShrink': '0',
                                'display': 'flex',
                                'flexDirection': 'column',
                                'alignItems': 'center'
                            },
                            children=[
                                html.Div(
                                    style={
                                        'width': '26px',
                                        'height': '26px',
                                        'backgroundColor': '#fc892f',
                                        'borderRadius': '50%',
                                        'display': 'flex',
                                        'justifyContent': 'center',
                                        'alignItems': 'center'
                                    },
                                    children=html.Img(
                                        src='/assets/person.svg',  # Path to your SVG in the assets folder
                                        style={
                                            'width': '16px',  # Adjust size as needed
                                            'height': '16px',
                                            'filter': 'brightness(0) invert(1)'  # Makes the icon white
                                        }
                                    )
                                ),
                                html.Div(
                                    "",
                                    style={
                                        'fontSize': '12px',
                                        'color': '#3d1502',
                                        'marginTop': '4px',
                                        'font-family':'Calibri'
                                    }
                                )
                            ]
                        ),
                        html.Div(
                            style={
                                'width': 'fit-content', 'height': 'fit-content',
                                'backgroundColor': '#fee4cf',
                                
                                'borderRadius': '16px',
                                'borderTopLeftRadius': '4px',
                                'padding': '7px 16px',
                                'cursor': 'pointer'
                            },
                            children=[
                                html.Div(
                                    style={
                                        'display': 'flex',
                                        'justifyContent': 'space-between',
                                        'alignItems': 'center'
                                    },
                                    children=[
                                        html.Div(
                                            "На чём основаны выводы и рекомендации, представленные в отчёте?",
                                            style={
                                                'color': '#3d1502',
                                                'fontSize': '13px',
                                                'fontWeight': '500',
                                                'margin': '0',
                                                'font-family':'Calibri'
                                            }
                                        ),

                                    ]
                                )
                            ]
                        )
                    ]
                ),
                
                # Answer
                html.Div(
                    style={
                        'display': 'flex',
                        'gap': '12px',
                        'justifyContent': 'flex-end',
                        'margin-top': '10px',
                        
                    },
                    children=[
                        html.Div(
                            style={
                                'width': 'fit-content', 'height': 'fit-content',
                                'maxWidth': '80%'
                            },
                            children=
                                    html.Div(
                                        style={
                                            'backgroundColor': '#dbeafe',
                                            'borderRadius': '16px',
                                            'borderTopRightRadius': '4px',
                                            'padding': '8px 16px'
                                        },
                                        children=[
                                            html.Div([
                                                "Все выводы и рекомендации носят ",
                                                html.B("информационный характер"),
                                                " и основаны на ",
                                                html.B("современных научных публикациях"),
                                                ", ",
                                                html.B("результатах метаболомного профилирования"),
                                                ", а также на ",
                                                html.B("экспериментальных данных"),
                                                ", полученных на реальных образцах от здоровых лиц и пациентов с различными установленными заболеваниями из биобанка Центра биофармацевтического анализа и метаболомных исследований Сеченовского университета. Оценка состояния проводится с использованием ",
                                                html.B("методов искусственного интеллекта"),
                                                "."
                                            ], style={
                                                'color': '#150c77',
                                                'fontSize': '13px',
                                                'margin': '0',
                                                'lineHeight': '1.5',
                                                'font-family': 'Calibri'
                                            })
                                        ]
                                    )
                        ),
                        html.Div(
                            style={
                                'flexShrink': '0',
                                'display': 'flex',
                                'flexDirection': 'column',
                                'alignItems': 'center'
                            },
                            children=[
                                html.Div(
                                    style={
                                        'width': '26px',
                                        'height': '26px',
                                        'backgroundColor': '#2563eb',
                                        'borderRadius': '50%',
                                        'display': 'flex',
                                        'justifyContent': 'center',
                                        'alignItems': 'center'
                                    },
                                    children=html.Img(
                                        src='/assets/person.svg',  # Path to your SVG in the assets folder
                                        style={
                                            'width': '16px',  # Adjust size as needed
                                            'height': '16px',
                                            'filter': 'brightness(0) invert(1)'  # Makes the icon white
                                        }
                                    )
                                ),
                                html.Div(
                                    "Метабоскан",
                                    style={
                                        'fontSize': '12px',
                                        'color': '#6b7280',
                                        'marginTop': '4px',
                                        'font-family': 'Calibri',
                                        'whiteSpace': 'nowrap'
                                    }
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
                # Content
        html.Div(
            style={
                'padding': '10px 0px 0px 0px',
                'backgroundColor': 'white',
                'borderTop': 'none',
            },
            children=[
                # Question
                html.Div(
                    style={
                        'display': 'flex',
                        'gap': '12px',
                        
                    },
                    children=[
                        html.Div(
                            style={
                                'flexShrink': '0',
                                'display': 'flex',
                                'flexDirection': 'column',
                                'alignItems': 'center'
                            },
                            children=[
                                html.Div(
                                    style={
                                        'width': '26px',
                                        'height': '26px',
                                        'backgroundColor': '#fc892f',
                                        'borderRadius': '50%',
                                        'display': 'flex',
                                        'justifyContent': 'center',
                                        'alignItems': 'center'
                                    },
                                    children=html.Img(
                                        src='/assets/person.svg',  # Path to your SVG in the assets folder
                                        style={
                                            'width': '16px',  # Adjust size as needed
                                            'height': '16px',
                                            'filter': 'brightness(0) invert(1)'  # Makes the icon white
                                        }
                                    )
                                ),
                                html.Div(
                                    "",
                                    style={
                                        'fontSize': '12px',
                                        'color': '#fee4cf',
                                        'marginTop': '4px',
                                        'font-family':'Calibri'
                                    }
                                )
                            ]
                        ),
                        html.Div(
                            style={
                                'width': 'fit-content', 'height': 'fit-content',
                                'backgroundColor': '#fee4cf',
                                
                                'borderRadius': '16px',
                                'borderTopLeftRadius': '4px',
                                'padding': '7px 16px',
                                'cursor': 'pointer'
                            },
                            children=[
                                html.Div(
                                    style={
                                        'display': 'flex',
                                        'justifyContent': 'space-between',
                                        'alignItems': 'center'
                                    },
                                    children=[
                                        html.Div(
                                            "Что именно оценивает система Метабоскан?",
                                            style={
                                                'color': '#3d1502',
                                                'fontSize': '13px',
                                                'fontWeight': '500',
                                                'margin': '0',
                                                'font-family': 'Calibri',
                                            }
                                        ),

                                    ]
                                )
                            ]
                        )
                    ]
                ),
                
                # Answer
                html.Div(
                    style={
                        'display': 'flex',
                        'gap': '12px',
                        'justifyContent': 'flex-end',
                        'margin-top': '10px',
                        
                    },
                    children=[
                        html.Div(
                            style={
                                'width': 'fit-content', 'height': 'fit-content',
                                'maxWidth': '80%'
                            },
                            children=html.Div(
                                        style={
                                            'backgroundColor': '#dbeafe',
                                            'borderRadius': '16px',
                                            'borderTopRightRadius': '4px',
                                            'padding': '8px 16px'
                                        },
                                        children=[
                                            html.Div([
                                                "Система Метабоскан предназначена для оценки ",
                                                html.B("текущего функционального состояния организма на молекулярном уровне"),
                                                ". Она ",
                                                html.B("не предназначена"),
                                                " для определения предрасположенности к заболеваниям или для ",
                                                html.B("самостоятельной диагностики"),
                                                "."
                                            ], style={
                                                'color': '#150c77',
                                                'fontSize': '13px',
                                                'margin': '0',
                                                'lineHeight': '1.5',
                                                'font-family': 'Calibri'
                                            })
                                        ]
                                    )
                        ),
                        html.Div(
                            style={
                                'flexShrink': '0',
                                'display': 'flex',
                                'flexDirection': 'column',
                                'alignItems': 'center'
                            },
                            children=[
                                html.Div(
                                    style={
                                        'width': '26px',
                                        'height': '26px',
                                        'backgroundColor': '#2563eb',
                                        'borderRadius': '50%',
                                        'display': 'flex',
                                        'justifyContent': 'center',
                                        'alignItems': 'center'
                                    },
                                    children=html.Img(
                                        src='/assets/person.svg',  # Path to your SVG in the assets folder
                                        style={
                                            'width': '16px',  # Adjust size as needed
                                            'height': '16px',
                                            'filter': 'brightness(0) invert(1)'  # Makes the icon white
                                        }
                                    )
                                ),
                                html.Div(
                                    "Метабоскан",
                                    style={
                                        'fontSize': '12px',
                                        'color': '#6b7280',
                                        'marginTop': '4px',
                                        'font-family': 'Calibri',
                                        'whiteSpace': 'nowrap'
                                    }
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
                # Content
        html.Div(
            style={
                'padding': '10px 0px 0px 0px',
                'backgroundColor': 'white',
                'borderTop': 'none',
            },
            children=[
                # Question
                html.Div(
                    style={
                        'display': 'flex',
                        'gap': '12px',
                        
                    },
                    children=[
                        html.Div(
                            style={
                                'flexShrink': '0',
                                'display': 'flex',
                                'flexDirection': 'column',
                                'alignItems': 'center'
                            },
                            children=[
                                html.Div(
                                    style={
                                        'width': '26px',
                                        'height': '26px',
                                        'backgroundColor': '#fc892f',
                                        'borderRadius': '50%',
                                        'display': 'flex',
                                        'justifyContent': 'center',
                                        'alignItems': 'center'
                                    },
                                    children=html.Img(
                                        src='/assets/person.svg',  # Path to your SVG in the assets folder
                                        style={
                                            'width': '16px',  # Adjust size as needed
                                            'height': '16px',
                                            'filter': 'brightness(0) invert(1)'  # Makes the icon white
                                        }
                                    )
                                ),
                                html.Div(
                                    "",
                                    style={
                                        'fontSize': '12px',
                                        'color': '#6b7280',
                                        'marginTop': '4px',
                                        'font-family':'Calibri'
                                    }
                                )
                            ]
                        ),
                        html.Div(
                            style={
                                'width': 'fit-content', 'height': 'fit-content',
                                'backgroundColor': '#fee4cf',
                                
                                'borderRadius': '16px',
                                'borderTopLeftRadius': '4px',
                                'padding': '7px 16px',
                                'cursor': 'pointer'
                            },
                            children=[
                                html.Div(
                                    style={
                                        'display': 'flex',
                                        'justifyContent': 'space-between',
                                        'alignItems': 'center'
                                    },
                                    children=[
                                        html.Div(
                                            "Что показывает метаболомный анализ?",
                                            style={
                                                'color': '#3d1502',
                                                'fontSize': '13px',
                                                'fontWeight': '500',
                                                'margin': '0',
                                                'font-family': 'Calibri',
                                            }
                                        ),

                                    ]
                                )
                            ]
                        )
                    ]
                ),
                
                # Answer
                html.Div(
                    style={
                        'display': 'flex',
                        'gap': '12px',
                        'justifyContent': 'flex-end',
                        'margin-top': '10px',
                        
                    },
                    children=[
                        html.Div(
                            style={
                                'width': 'fit-content', 'height': 'fit-content',
                                'maxWidth': '80%'
                            },
                            children=html.Div(
                                            style={
                                                'backgroundColor': '#dbeafe',
                                                'borderRadius': '16px',
                                                'borderTopRightRadius': '4px',
                                                'padding': '8px 16px'
                                            },
                                            children=[
                                                html.Div([
                                                    "Метаболомный анализ отражает ",
                                                    html.B("текущие биохимические процессы"),
                                                    " в организме и выявляет ",
                                                    html.B("изменения обмена веществ"),
                                                    ", которые могут быть связаны с вашими индивидуальными особенностями, хроническими заболеваниями, образом жизни и внешними факторами."
                                                ], style={
                                                    'color': '#150c77',
                                                    'fontSize': '13px',
                                                    'margin': '0',
                                                    'lineHeight': '1.5',
                                                    'font-family': 'Calibri'
                                                })
                                            ]
                                        )
                        ),
                        html.Div(
                            style={
                                'flexShrink': '0',
                                'display': 'flex',
                                'flexDirection': 'column',
                                'alignItems': 'center'
                            },
                            children=[
                                html.Div(
                                    style={
                                        'width': '26px',
                                        'height': '26px',
                                        'backgroundColor': '#2563eb',
                                        'borderRadius': '50%',
                                        'display': 'flex',
                                        'justifyContent': 'center',
                                        'alignItems': 'center'
                                    },
                                    children=html.Img(
                                        src='/assets/person.svg',  # Path to your SVG in the assets folder
                                        style={
                                            'width': '16px',  # Adjust size as needed
                                            'height': '16px',
                                            'filter': 'brightness(0) invert(1)'  # Makes the icon white
                                        }
                                    )
                                ),
                                html.Div(
                                    "Метабоскан",
                                    style={
                                        'fontSize': '12px',
                                        'color': '#6b7280',
                                        'marginTop': '4px',
                                        'font-family': 'Calibri',
                                        'whiteSpace': 'nowrap'
                                    }
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
                # Content
        html.Div(
            style={
                'padding': '10px 0px 0px 0px',
                'backgroundColor': 'white',
                'borderTop': 'none',
            },
            children=[
                # Question
                html.Div(
                    style={
                        'display': 'flex',
                        'gap': '12px',
                        
                    },
                    children=[
                        html.Div(
                            style={
                                'flexShrink': '0',
                                'display': 'flex',
                                'flexDirection': 'column',
                                'alignItems': 'center'
                            },
                            children=[
                                html.Div(
                                    style={
                                        'width': '26px',
                                        'height': '26px',
                                        'backgroundColor': '#fc892f',
                                        'borderRadius': '50%',
                                        'display': 'flex',
                                        'justifyContent': 'center',
                                        'alignItems': 'center'
                                    },
                                    children=html.Img(
                                        src='/assets/person.svg',  # Path to your SVG in the assets folder
                                        style={
                                            'width': '16px',  # Adjust size as needed
                                            'height': '16px',
                                            'filter': 'brightness(0) invert(1)'  # Makes the icon white
                                        }
                                    )
                                ),
                                html.Div(
                                    "",
                                    style={
                                        'fontSize': '12px',
                                        'color': '#6b7280',
                                        'marginTop': '4px',
                                        'font-family':'Calibri'
                                    }
                                )
                            ]
                        ),
                        html.Div(
                            style={
                                'width': 'fit-content', 'height': 'fit-content',
                                'backgroundColor': '#fee4cf',
                                
                                'borderRadius': '16px',
                                'borderTopLeftRadius': '4px',
                                'padding': '7px 16px',
                                'cursor': 'pointer'
                            },
                            children=[
                                html.Div(
                                    style={
                                        'display': 'flex',
                                        'justifyContent': 'space-between',
                                        'alignItems': 'center'
                                    },
                                    children=[
                                        html.Div(
                                            "Может ли метаболомный анализ заменить полноценное медицинское обследование?",
                                            style={
                                                'color': '#3d1502',
                                                'fontSize': '13px',
                                                'fontWeight': '500',
                                                'margin': '0',
                                                'font-family': 'Calibri',
                                            }
                                        ),

                                    ]
                                )
                            ]
                        )
                    ]
                ),
                
                # Answer
                html.Div(
                    style={
                        'display': 'flex',
                        'gap': '12px',
                        'justifyContent': 'flex-end',
                        'margin-top': '10px',
                        
                    },
                    children=[
                        html.Div(
                            style={
                                'width': 'fit-content', 'height': 'fit-content',
                                'maxWidth': '80%'
                            },
                            children=html.Div(
                                    style={
                                        'backgroundColor': '#dbeafe',
                                        'borderRadius': '16px',
                                        'borderTopRightRadius': '4px',
                                        'padding': '8px 16px'
                                    },
                                    children=[
                                        html.Div([
                                            html.B("Нет."),
                                            " Данный подход ",
                                            html.B("не заменяет медицинского обследования"),
                                            " и не учитывает в полной мере анамнез, приём лекарственных препаратов, БАДов и все аспекты внешней среды, включая особенности питания."
                                        ], style={
                                            'color': '#150c77',
                                            'fontSize': '13px',
                                            'margin': '0',
                                            'lineHeight': '1.5',
                                            'font-family': 'Calibri'
                                        })
                                    ]
                                )
                        ),
                        html.Div(
                            style={
                                'flexShrink': '0',
                                'display': 'flex',
                                'flexDirection': 'column',
                                'alignItems': 'center'
                            },
                            children=[
                                html.Div(
                                    style={
                                        'width': '26px',
                                        'height': '26px',
                                        'backgroundColor': '#2563eb',
                                        'borderRadius': '50%',
                                        'display': 'flex',
                                        'justifyContent': 'center',
                                        'alignItems': 'center'
                                    },
                                    children=html.Img(
                                        src='/assets/person.svg',  # Path to your SVG in the assets folder
                                        style={
                                            'width': '16px',  # Adjust size as needed
                                            'height': '16px',
                                            'filter': 'brightness(0) invert(1)'  # Makes the icon white
                                        }
                                    )
                                ),
                                html.Div(
                                    "Метабоскан",
                                    style={
                                        'fontSize': '12px',
                                        'color': '#6b7280',
                                        'marginTop': '4px',
                                        'font-family': 'Calibri',
                                        'whiteSpace': 'nowrap'
                                    }
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
                # Content
        html.Div(
            style={
                'padding': '10px 0px 0px 0px',
                'backgroundColor': 'white',
                'borderTop': 'none',
            },
            children=[
                # Question
                html.Div(
                    style={
                        'display': 'flex',
                        'gap': '12px',
                        
                    },
                    children=[
                        html.Div(
                            style={
                                'flexShrink': '0',
                                'display': 'flex',
                                'flexDirection': 'column',
                                'alignItems': 'center'
                            },
                            children=[
                                html.Div(
                                    style={
                                        'width': '26px',
                                        'height': '26px',
                                        'backgroundColor': '#fc892f',
                                        'borderRadius': '50%',
                                        'display': 'flex',
                                        'justifyContent': 'center',
                                        'alignItems': 'center'
                                    },
                                    children=html.Img(
                                        src='/assets/person.svg',  # Path to your SVG in the assets folder
                                        style={
                                            'width': '16px',  # Adjust size as needed
                                            'height': '16px',
                                            'filter': 'brightness(0) invert(1)'  # Makes the icon white
                                        }
                                    )
                                ),
                                html.Div(
                                    "",
                                    style={
                                        'fontSize': '12px',
                                        'color': '#6b7280',
                                        'marginTop': '4px',
                                        'font-family': 'Calibri',
                                        
                                    }
                                )
                            ]
                        ),
                        html.Div(
                            style={
                                'width': 'fit-content', 'height': 'fit-content',
                                'backgroundColor': '#fee4cf',
                                
                                'borderRadius': '16px',
                                'borderTopLeftRadius': '4px',
                                'padding': '7px 16px',
                                'cursor': 'pointer'
                            },
                            children=[
                                html.Div(
                                    style={
                                        'display': 'flex',
                                        'justifyContent': 'space-between',
                                        'alignItems': 'center'
                                    },
                                    children=[
                                        html.Div(
                                            "Для кого и зачем предназначена система Метабоскан?",
                                            style={
                                                'color': '#3d1502',
                                                'fontSize': '13px',
                                                'fontWeight': '500',
                                                'margin': '0',
                                                'font-family': 'Calibri',
                                            }
                                        ),

                                    ]
                                )
                            ]
                        )
                    ]
                ),
                
                # Answer
                html.Div(
                    style={
                        'display': 'flex',
                        'gap': '12px',
                        'justifyContent': 'flex-end',
                        'margin-top': '10px',
                        
                    },
                    children=[
                        html.Div(
                            style={
                                'width': 'fit-content', 'height': 'fit-content',
                                'maxWidth': '80%'
                            },
                            children=html.Div(
                                    style={
                                        'backgroundColor': '#dbeafe',
                                        'borderRadius': '16px',
                                        'borderTopRightRadius': '4px',
                                        'padding': '8px 16px'
                                    },
                                    children=[
                                        html.Div([
                                            "Метабоскан — ",
                                            html.B("навигационный инструмент"),
                                            " для тех, кто решил взять своё здоровье под контроль. С его помощью вы можете ",
                                            html.B("отслеживать изменения"),
                                            " функционального состояния организма на молекулярном уровне, ",
                                            html.B("своевременно замечать"),
                                            " положительные или отрицательные последствия различных воздействий и ",
                                            html.B("оперативно принимать меры"),
                                            "."
                                        ], style={
                                            'color': '#150c77',
                                            'fontSize': '13px',
                                            'margin': '0',
                                            'lineHeight': '1.5',
                                            'font-family': 'Calibri'
                                        })
                                    ]
                                )
                        ),
                        html.Div(
                            style={
                                'flexShrink': '0',
                                'display': 'flex',
                                'flexDirection': 'column',
                                'alignItems': 'center'
                            },
                            children=[
                                html.Div(
                                    style={
                                        'width': '26px',
                                        'height': '26px',
                                        'backgroundColor': '#2563eb',
                                        'borderRadius': '50%',
                                        'display': 'flex',
                                        'justifyContent': 'center',
                                        'alignItems': 'center'
                                    },
                                    children=html.Img(
                                        src='/assets/person.svg',  # Path to your SVG in the assets folder
                                        style={
                                            'width': '16px',  # Adjust size as needed
                                            'height': '16px',
                                            'filter': 'brightness(0) invert(1)'  # Makes the icon white
                                        }
                                    )
                                ),
                                html.Div(
                                    "Метабоскан",
                                    style={
                                        'fontSize': '12px',
                                        'color': '#6b7280',
                                        'marginTop': '4px',
                                        'font-family': 'Calibri',
                                        'whiteSpace': 'nowrap'
                                    }
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
                        # Content
        html.Div(
            style={
                'padding': '10px 0px 0px 0px',
                'backgroundColor': 'white',
                'borderTop': 'none',
            },
            children=[
                # Question
                html.Div(
                    style={
                        'display': 'flex',
                        'gap': '12px',
                        
                    },
                    children=[
                        html.Div(
                            style={
                                'flexShrink': '0',
                                'display': 'flex',
                                'flexDirection': 'column',
                                'alignItems': 'center'
                            },
                            children=[
                                html.Div(
                                    style={
                                        'width': '26px',
                                        'height': '26px',
                                        'backgroundColor': '#fc892f',
                                        'borderRadius': '50%',
                                        'display': 'flex',
                                        'justifyContent': 'center',
                                        'alignItems': 'center'
                                    },
                                    children=html.Img(
                                        src='/assets/person.svg',  # Path to your SVG in the assets folder
                                        style={
                                            'width': '16px',  # Adjust size as needed
                                            'height': '16px',
                                            'filter': 'brightness(0) invert(1)'  # Makes the icon white
                                        }
                                    )
                                ),
                                html.Div(
                                    "",
                                    style={
                                        'fontSize': '12px',
                                        'color': '#6b7280',
                                        'marginTop': '4px',
                                        'font-family': 'Calibri',
                                    }
                                )
                            ]
                        ),
                        html.Div(
                            style={
                                'width': 'fit-content', 'height': 'fit-content',
                                'backgroundColor': '#fee4cf',
                                
                                'borderRadius': '16px',
                                'borderTopLeftRadius': '4px',
                                'padding': '7px 16px',
                            },
                            children=[
                                html.Div(
                                    style={
                                        'display': 'flex',
                                        'justifyContent': 'space-between',
                                        'alignItems': 'center'
                                    },
                                    children=[
                                        html.Div(
                                            "Что делать, если я хочу правильно понять результаты анализа?",
                                            style={
                                                'color': '#3d1502',
                                                'fontSize': '13px',
                                                'fontWeight': '500',
                                                'margin': '0',
                                                'font-family': 'Calibri',
                                            }
                                        ),

                                    ]
                                )
                            ]
                        )
                    ]
                ),
                
                # Answer
                html.Div(
                    style={
                        'display': 'flex',
                        'gap': '12px',
                        'justifyContent': 'flex-end',
                        'margin-top': '10px',
                        
                    },
                    children=[
                        html.Div(
                            style={
                                'width': 'fit-content', 'height': 'fit-content',
                                
                                'maxWidth': '80%'
                            },
                            children=html.Div(
                                    style={
                                        'backgroundColor': '#dbeafe',
                                        'borderRadius': '16px',
                                        'borderTopRightRadius': '4px',
                                        'borderBottomRightRadius': '8px',
                                        'padding': '8px 16px'
                                    },
                                    children=[
                                        html.Div([
                                            "Для ",
                                            html.B("корректной интерпретации"),
                                            " результатов метаболомного анализа необходима ",
                                            html.B("консультация врача"),
                                            " с учётом полного анамнеза и вашего образа жизни."
                                        ], style={
                                            'color': '#150c77',
                                            'fontSize': '13px',
                                            'margin': '0',
                                            'lineHeight': '1.5',
                                            'font-family': 'Calibri'
                                        })
                                    ]
                                )
                        ),
                        html.Div(
                            style={
                                'flexShrink': '0',
                                'display': 'flex',
                                'flexDirection': 'column',
                                'alignItems': 'center'
                            },
                            children=[
                                html.Div(
                                    style={
                                        'width': '26px',
                                        'height': '26px',
                                        'backgroundColor': '#2563eb',
                                        'borderRadius': '50%',
                                        'display': 'flex',
                                        'justifyContent': 'center',
                                        'alignItems': 'center'
                                    },
                                    children=html.Img(
                                        src='/assets/person.svg',  # Path to your SVG in the assets folder
                                        style={
                                            'width': '16px',  # Adjust size as needed
                                            'height': '16px',
                                            'filter': 'brightness(0) invert(1)'  # Makes the icon white
                                        }
                                    )
                                ),
                                html.Div(
                                    "Метабоскан",
                                    style={
                                        'fontSize': '12px',
                                        'color': '#6b7280',
                                        'marginTop': '4px',
                                        'font-family': 'Calibri',
                                        'whiteSpace': 'nowrap'
                                    }
                                )
                            ]
                        )
                    ]
                )
            ]
        ), 
        # Answer
                html.Div(
                    style={
                        'display': 'flex',
                        'gap': '12px',
                        'justifyContent': 'flex-end',
                        'marginTop': '5px'
                        
                    },
                    children=[
                        html.Div(
                            style={
                                'width': 'fit-content', 'height': 'fit-content',
                                
                                'maxWidth': '80%'
                            },
                            children=html.Div(
                                    style={
                                        'backgroundColor': '#dbeafe',
                                        'borderRadius': '16px',
                                        'borderTopRightRadius': '8px',
                                        'borderBottomRightRadius': '8px',
                                        'padding': '8px 16px'
                                    },
                                    children=[
                                        html.Div([
                                            "Больше информации Вы найдете на сайте Центра ",
                                            html.B("metaboscan.ru"),
                                            ", а также рекомендуем Вам научно-популярные статьи о метаболомике в Telegram-канале ",
                                            html.B("@metaboscan"),
                                            "."
                                        ], style={
                                            'color': '#150c77',
                                            'fontSize': '13px',
                                            'margin': '0',
                                            'lineHeight': '1.5',
                                            'font-family': 'Calibri'
                                        })
                                    ]
                                )
                        ),
                        html.Div(
                            style={
                                'flexShrink': '0',
                                'display': 'flex',
                                'flexDirection': 'column',
                                'alignItems': 'center'
                            },
                            children=[
                                html.Div(
                                    style={
                                        'width': '26px',
                                        'height': '26px',
                                        'backgroundColor': '#fff',
                                        'borderRadius': '50%',
                                        'display': 'flex',
                                        'justifyContent': 'center',
                                        'alignItems': 'center'
                                    },
                                    children=html.I(className="fas fa-robot", style={'color': 'white'})
                                ),
                                html.Div(
                                    "Метабоскан",
                                    style={
                                        'fontSize': '12px',
                                        'color': '#fff',
                                        'marginTop': '4px',
                                        'font-family': 'Calibri',
                                        'whiteSpace': 'nowrap'
                                    }
                                )
                            ]
                        )
                    ]
                ),
                
                 html.Div(
                    style={
                        'display': 'flex',
                        'gap': '12px',
                        'justifyContent': 'flex-end',
                        'marginTop': '5px'
                        
                    },
                    children=[
                        html.Div(
                            style={
                                'width': 'fit-content', 'height': 'fit-content',
                                
                                'maxWidth': '80%'
                            },
                            children=html.Div(
                                style={
                                    'backgroundColor': '#dbeafe',
                                    
                                    'borderRadius': '16px',
                                    'borderTopRightRadius': '8px',
                                    'padding': '7px 16px'
                                },
                                children=html.Div(
                                    children=[
                                        html.B("Желаем вам крепкого здоровья и хорошего самочувствия!"),
                                        "❤️"
                                    ],
                                    style={
                                        'color': '#150c77',
                                        'fontSize': '13px',
                                        'margin': '0',
                                        'lineHeight': '1.5',
                                        'font-family': 'Calibri'
                                    }
                                )
                            )
                        ),
                        html.Div(
                            style={
                                'flexShrink': '0',
                                'display': 'flex',
                                'flexDirection': 'column',
                                'alignItems': 'center'
                            },
                            children=[
                                html.Div(
                                    style={
                                        'width': '26px',
                                        'height': '26px',
                                        'backgroundColor': '#fff',
                                        'borderRadius': '50%',
                                        'display': 'flex',
                                        'justifyContent': 'center',
                                        'alignItems': 'center'
                                    },
                                    children=html.I(className="fas fa-robot", style={'color': 'white'})
                                ),
                                html.Div(
                                    "Метабоскан",
                                    style={
                                        'fontSize': '12px',
                                        'color': '#fff',
                                        'marginTop': '4px',
                                        'font-family': 'Calibri',
                                        'whiteSpace': 'nowrap'
                                    }
                                )
                            ]
                        )
                    ]
                ),
                 
                 html.Div(
    style={
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'justifyContent': 'center',
        'gap': '10px',
        'padding': '30px 0px 0px 0px',
        'backgroundColor': 'white'
    },
    children=[
        # QR Codes Row
        html.Div(
            style={
                'display': 'flex',
                'flexDirection': 'row',
                'justifyContent': 'center',
                'gap': '40px',
                'flexWrap': 'wrap'
            },
            children=[
                # Telegram QR Code
                html.Div(
                    style={
                        'display': 'flex',
                        'flexDirection': 'column',
                        'alignItems': 'center',
                        'gap': '8px'
                    },
                    children=[
                        html.Img(
                            src='assets/telegram_qr_link.png',  # Replace with your actual path
                            style={
                                'width': '100px',
                                'height': '100px',
                                'borderRadius': '8px'
                            }
                        ),
                        html.Div(
                            "Наш Telegram-канал",
                            style={
                                'fontFamily': 'Calibri',
                                'fontSize': '14px',
                                'color': '#4b5563'
                            }
                        )
                    ]
                ),
                # Website QR Code
                html.Div(
                    style={
                        'display': 'flex',
                        'flexDirection': 'column',
                        'alignItems': 'center',
                        'gap': '8px'
                    },
                    children=[
                        html.Img(
                            src='assets/web_qr_link.png',  # Replace with your actual path
                            style={
                                'width': '100px',
                                'height': '100px',
                                'borderRadius': '8px'
                            }
                        ),
                        html.Div(
                            "https://metaboscan.ru/",
                            style={
                                'fontFamily': 'Calibri',
                                'fontSize': '14px',
                                'color': '#4b5563',
                                'textDecoration': 'none'
                            }
                        )
                    ]
                )
            ]
        ),
        # Optional description
        html.Div(
            "Отсканируйте QR-код для перехода",
            style={
                'fontFamily': 'Calibri',
                'fontSize': '12px',
                'color': '#6b7280',
                'marginTop': '5px'
            }
        )
    ]
)
        
                

                ], style={'margin':'0px'}),
            ]),
        
            ],style={'margin-right':'5mm','width':'800px'}) 

        app.layout = create_layout()
        
        print("Starting Dash server...")
        app.run_server(
            debug=False,
            port=8050,
            host='0.0.0.0',
            dev_tools_serve_dev_bundles=False
        )
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

   
if __name__ == "__main__":
    main()