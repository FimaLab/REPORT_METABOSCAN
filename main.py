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

import pandas as pd
import json

def create_ref_stats_from_excel(excel_path):
    # Read Excel with explicit handling of decimal commas
    df = pd.read_excel(excel_path, engine='openpyxl')
    
    # Transpose to metabolites-as-rows format
    df = df.set_index('metabolite').T.reset_index()
    df.columns.name = None
    
    ref_stats = {}
    
    for _, row in df.iterrows():
        try:
            metabolite = row['index']
            data = {
                'mean': float(str(row['mean']).replace(',', '.')),
                'sd': float(str(row['sd']).replace(',', '.')),
                'ref_min': float(str(row['ref_min']).replace(',', '.')) if pd.notna(row['ref_min']) else None,
                'ref_max': float(str(row['ref_max']).replace(',', '.')) if pd.notna(row['ref_max']) else None,
                'smart_round': int(row['smart_round']),
                'name_view': row['name_view']
            }
            
            # Generate norm string
            if data['ref_min'] is not None and data['ref_max'] is not None:
                if data['ref_min'] == 0:
                    data['norm'] = f"< {data['ref_max']}"
                else:
                    data['norm'] = f"{data['ref_min']} - {data['ref_max']}"
            
            ref_stats[metabolite] = {k: v for k, v in data.items() if v is not None}
            
        except Exception as e:
            print(f"Error processing {row.get('index', 'unknown')}: {str(e)}")
            continue
    
    # Save to JSON
    with open('ref_stats.json', 'w', encoding='utf-8') as f:
        json.dump(ref_stats, f, ensure_ascii=False, indent=2)
    
    return ref_stats


ref_stats = create_ref_stats_from_excel('Ref.xlsx')
risk_params = pd.read_excel('Params_metaboscan.xlsx')

def plot_metabolite_z_scores(metabolite_concentrations, group_title, norm_ref=[-1, 1]):
    # Set font to Calibri
    mpl.rcParams['font.family'] = 'Calibri'
    
    # Calculate z-scores and determine colors
    data = []
    highlight_green_metabolites = []
    missing_metabolites = []
    name_translations = {}  # Track original to display name mappings
    
    for original_name, conc in metabolite_concentrations.items():
        # Skip if metabolite not in reference
        if original_name not in ref_stats:
            missing_metabolites.append(original_name)
            continue
            
        ref_data = ref_stats[original_name]
        
        # Skip if required fields are missing
        if "mean" not in ref_data or "sd" not in ref_data:
            missing_metabolites.append(original_name)
            continue
            
        # Get display name (use name_view if available, otherwise original)
        display_name = ref_data.get("name_view", original_name)
        name_translations[original_name] = display_name
        
        # Calculate z-score (deviation from mean in SD units)
        try:
            z_score = round((conc - ref_data["mean"]) / ref_data["sd"], 2)
            
            # Handle special case for "<" reference ranges
            if "norm" in ref_data and isinstance(ref_data["norm"], str):
                if "<" in ref_data["norm"] and z_score <= 0:
                    z_score = 0
                    highlight_green_metabolites.append(display_name)
            
            # Determine color based on z-score
            if abs(z_score) > 1.2:  # Significant deviation
                color = "#dc2626"  # red
            elif abs(z_score) > 1:   # Moderate deviation
                color = "#feb61d"  # orange
            else:                   # Normal range
                color = "#10b981"  # green
                
            data.append({
                "original_name": original_name,
                "display_name": display_name,
                "value": z_score,
                "color": color,
                "original_value": conc
            })
            
        except (TypeError, ValueError):
            missing_metabolites.append(original_name)

    # Create figure - show empty plot if no valid data
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
    if not data:
        ax.text(0.5, 0.5, 
               "No valid reference data available\nfor these metabolites", 
               ha='center', va='center',
               fontsize=14, color='#6B7280')
        ax.set_title(group_title, fontsize=22, pad=20, color='#404547', fontweight='bold')
        for spine in ['top', 'right', 'bottom', 'left']:
            ax.spines[spine].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
        plt.tight_layout()
        return fig_to_uri(fig)

    # Create bars using display names
    bars = ax.bar([d["display_name"] for d in data], 
                 [d["value"] for d in data], 
                 color=[d["color"] for d in data], 
                 edgecolor='white', 
                 linewidth=1)

    # Add value labels on top of bars
    for bar, item in zip(bars, data):
        height = item["value"]
        va = 'bottom' if height >= 0 else 'top'
        y = height + 0.05 if height >= 0 else height - 0.05
        
        # Determine text color - green if in highlight list, otherwise black
        text_color = '#10b981' if item["display_name"] in highlight_green_metabolites else 'black'
        
        # Adjust fontsize based on number of labels
        fontsize = 11 if len(data) > 15 else 14
        
        ax.text(bar.get_x() + bar.get_width()/2., y,
               f'{height:.2f}',
               ha='center', va=va, 
               fontsize=fontsize, 
               fontweight='bold',
               color=text_color)

    # Add horizontal lines
    ax.axhline(0, color='#374151', linewidth=1)
    ax.axhline(norm_ref[1], color='#6B7280', linestyle='--', linewidth=1)
    ax.axhline(norm_ref[0], color='#6B7280', linestyle='--', linewidth=1)
    ax.axhline(1.2, color='#6B7280', linestyle=':', linewidth=1, alpha=0.5)
    ax.axhline(-1.2, color='#6B7280', linestyle=':', linewidth=1, alpha=0.5)

    # Set title and labels
    ax.set_title(group_title, fontsize=22, pad=20, color='#404547', fontweight='bold')
    ax.set_ylabel(f"Отклонение от состояния ЗДОРОВЫЙ, норма от {norm_ref[0]} до {norm_ref[1]}", 
                 fontsize=14, labelpad=15)
                 
    # Set y-axis scale with appropriate steps
    y_min = round(min(-1.5, min([d["value"] for d in data])) - 0.2, 1)
    y_max = round(max(1.5, max([d["value"] for d in data])) + 0.2, 1)
    ax.set_ylim(y_min, y_max)
    
    y_range = max(abs(y_min), abs(y_max))
    step = 3.0 if y_range > 15 else 1.5 if y_range > 10 else 1.0 if y_range > 7 else 0.75 if y_range > 5 else 0.5
    ax.set_yticks(np.arange(np.floor(y_min), np.ceil(y_max) + step, step))

    # Customize axes
    for spine in ['top', 'right', 'bottom', 'left']:
        ax.spines[spine].set_visible(False)
    ax.xaxis.set_tick_params(length=0)
    ax.yaxis.set_tick_params(length=0)
    plt.yticks(fontsize=13)

    # Adjust x-axis labels
    xticklabels = ax.get_xticklabels()
    for label in xticklabels:
        display_name = label.get_text()
        fontsize = (13.5 if len(display_name) > 20 else 
                   15 if len(display_name) > 12 else 15.5)
        label.set_fontsize(fontsize)
        label.set_rotation(45)
        label.set_ha('right')

    # Add warning about missing metabolites if needed
    if missing_metabolites:
        # Try to get display names for missing metabolites
        missing_display_names = []
        for name in missing_metabolites:
            if name in ref_stats and "name_view" in ref_stats[name]:
                missing_display_names.append(ref_stats[name]["name_view"])
            else:
                missing_display_names.append(name)
                
        warning_text = (f"Missing data for:\n{', '.join(missing_display_names[:3])}" + 
                       ("..." if len(missing_display_names) > 3 else ""))
        
        ax.text(1.02, 0.95, 
               warning_text,
               transform=ax.transAxes,
               fontsize=10, color='#dc2626',
               ha='left', va='top',
               bbox=dict(facecolor='white', alpha=0.8, edgecolor='#fecaca', pad=4))

    plt.tight_layout()
    return fig_to_uri(fig)

def fig_to_uri(fig):
    """Convert matplotlib figure to data URI"""
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
    buf.seek(0)
    img = base64.b64encode(buf.getvalue()).decode("ascii")
    plt.close(fig)
    return f"data:image/png;base64,{img}"

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
    
def smart_round(value, default_decimals=3, ref_stats_entry=None):
    """
    Округляет число с учетом значимых цифр
    
    :param value: исходное значение (число или строка)
    :param default_decimals: знаки после запятой по умолчанию
    :param ref_stats_entry: словарь с ref_min и ref_max
    :return: округлённое значение
    """
    try:
        num = float(value)
    except (ValueError, TypeError):
        return 0.0
    
    if num == 0:
        return 0.0

    decimals = default_decimals
    
    if ref_stats_entry and isinstance(ref_stats_entry, dict):
        try:
            # Get ref_min and ref_max directly from the dict
            ref_min = ref_stats_entry.get('ref_min')
            ref_max = ref_stats_entry.get('ref_max')
            
            if ref_min is not None and ref_max is not None:
                def count_decimals(x):
                    if isinstance(x, (int, float)):
                        s = f"{x:.10f}".rstrip('0')
                        return len(s.split('.')[1]) if '.' in s else 0
                    return 0
                
                decimals = max(
                    count_decimals(ref_min),
                    count_decimals(ref_max),
                    default_decimals
                )
        except (TypeError, ValueError, AttributeError):
            pass
    
    # First rounding attempt
    rounded = round(num, decimals)
    
    # If non-zero, return it
    if rounded != 0:
        return rounded
    
    # Find first non-zero digit if rounded to zero
    abs_num = abs(num)
    precision = decimals
    while round(abs_num, precision) == 0 and precision <= 10:
        precision += 1
    
    return round(num, min(precision, 10))

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
    

def get_ref_min_max(ref_stats_entry):
    ref_min = ref_stats_entry["ref_min"]
    ref_max = ref_stats_entry["ref_max"]
    return ref_min, ref_max


def calculate_pointer_position(value: float, ref_stats_entry: dict):
    """
    Calculate position indicator (0-100) for a value within its reference range
    
    :param value: Input value to evaluate
    :param ref_stats_entry: Dictionary containing 'ref_min' and 'ref_max'
    :return: Position percentage (0-100) or None if invalid
    """
    try:
        value = float(value)
        ref_min, ref_max = get_ref_min_max(ref_stats_entry)
        
        # Calculate position
        if value < ref_min:
            return 0
        elif value > ref_max:
            return 100
        else:
            position = ((value - ref_min) / (ref_max - ref_min)) * 100
            return max(0, min(100, round(position, 2)))  # Clamp and round
    
    except (ValueError, TypeError, KeyError):
        return 50


def color_text_ref(value: float, ref_stats_entry: str):
    ref_min, ref_max = get_ref_min_max(ref_stats_entry)
    if value > ref_max:
        return '#dc3545'
    elif value <  ref_min:
        return '#dc3545'
    else:
        return '#404547' 


def heighlight_out_of_range(value: float, ref_stats_entry: str):
    ref_min, ref_max = get_ref_min_max(ref_stats_entry)
    if value > ref_max:
        return '#f8d7da'
    elif value <  ref_min:
        return '#f8d7da'
    else:
        return 'white'
    


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

#[template_elements_img/group_params.png]
def render_category_params(group_number, group_risk_name, risk_scores, ref_params):
    # Filter the reference parameters for the specific group risk
    group_data = ref_params[ref_params['Группа_риска'] == group_risk_name]
    
    # Calculate scores for each parameter in the group
    param_scores = {}
    for _, row in group_data.iterrows():
        param_name = row['Категория']
        score = row['Subgroup_score']
        param_scores[param_name] = score
    
    # Get the overall risk score for this group
    overall_score = risk_scores.loc[risk_scores['Группа риска'] == group_risk_name, 'Риск-скор'].values[0]
    
    # Create header based on name length
    if len(group_risk_name) > 30:
        header = html.Div([
            # Header container
            html.Div([
                html.Div([
                    html.P(f"{group_number}.", style={
                        'margin': '0px', 
                        'margin-bottom': '1px', 
                        'font-weight': 'bold', 
                        'margin-right': '5px', 
                        'color': '#404547'
                    }),
                    html.P(group_risk_name, style={
                        'margin': '0px', 
                        'margin-bottom': '1px', 
                        'width': '200px', 
                        'font-weight': 'bold', 
                        'color': '#404547'
                    }),
                ], style={
                    'display': 'flex', 
                    'justify-content': 'left', 
                    'width': 'auto', 
                    'height': '18px'
                }),
                
                # Score container
                html.Div([
                    html.Div([
                        html.Div([], style={
                            'width': f"{overall_score * 10}%",
                            'background-color': get_color_under_normal_dist(100 - (overall_score * 10)),
                            'border-radius': '2px',
                            'height': '13px',
                            'line-height': 'normal',
                            'display': 'inline-block',
                            'vertical-align': 'center',
                        }),
                    ], style={
                        'display': 'flex', 
                        'align-self': 'center',
                        'width': '70px', 
                        'height': '13px',
                        'line-height': 'normal', 
                        'border-radius': '2px',
                        'background-color': 'lightgrey', 
                        'margin-left': '5px', 
                        'margin-right': '5px'
                    }),
                    html.B(
                        f"{overall_score} из 10",
                        style={'margin': '0px', 'color': '#404547'}
                    )
                ], style={
                    'display': 'flex', 
                    'flex-direction': 'row', 
                    'flex-wrap': 'nowrap', 
                    'align-items': 'center'
                })
            ], style={
                'color': 'black',
                'font-family': 'Calibri',
                'font-size': '16px',
                'margin': '0px',
                'display': 'flex',
                'justify-content': 'space-between',
                'margin-bottom': '15px'
            })
        ])
    else:
        # Standard header for short names
        header = html.Div([
            html.P(f"{group_number}. {group_risk_name}", style={
                'margin': '0px', 
                'margin-bottom': '1px', 
                'font-weight': 'bold', 
                'color': '#404547'
            }),
            html.Div([
                html.Div([
                    html.Div([], style={
                        'width': f"{overall_score * 10}%",
                        'background-color': get_color_under_normal_dist(100 - (overall_score * 10)),
                        'border-radius': '2px',
                        'height': '13px',
                        'line-height': 'normal',
                        'display': 'inline-block',
                        'vertical-align': 'center',
                    }),
                ], style={
                    'display': 'flex', 
                    'align-self': 'center',
                    'width': '70px', 
                    'height': '13px',
                    'line-height': 'normal', 
                    'border-radius': '2px',
                    'background-color': 'lightgrey', 
                    'margin-left': '5px', 
                    'margin-right': '5px'
                }),
                html.B(
                    f"{overall_score} из 10",
                    style={'margin': '0px', 'color': '#404547'}
                )
            ], style={'display': 'flex', 'flex-direction': 'row', 'flex-wrap': 'nowrap'})
        ], style={
            'color': 'black',
            'font-family': 'Calibri',
            'font-size': '16px',
            'margin': '0px',
            'display': 'flex',
            'justify-content': 'space-between',
            'margin-bottom': '0px'
        })
    
    # Create the HTML structure
    return html.Div([
        # Header
        header,
        
        # Divider line
        html.Div([], style={
            'width': "100%",
            'background-color': "#2563eb",
            'height': '2px',
            'line-height': 'normal',
            'display': 'inline-block',
            'vertical-align': 'center',
            'margin-bottom': '2px'
        }),
        
        # Parameters list
        *[
            html.Div([
                html.Div([
                    html.Div([], style={
                        'width': f'{100 - score}%',
                        'background-color': get_color_under_normal_dist(score),
                        'border-radius': '5px',
                        'height': '10px',
                        'line-height': 'normal',
                        'display': 'inline-block',
                        'vertical-align': 'center',
                    }),
                ], style={
                    'width': '23%', 
                    'height': '18px', 
                    'line-height': '18px', 
                    'margin-right': '5px'
                }),
                html.Div([
                    html.P(param_name, style={
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
            })
            for param_name, score in param_scores.items()
        ]
    ], style={'width': '100%', 'height': 'fit-content'})
    
#[template_elements_img/ml_card.png]
def render_ml_score_card(title, subtitle, description, metrics, risk_scores):
    """
    Render a standardized ML score card component with improved title formatting
    
    Parameters:
    - title: Main title string (will be split at hyphens)
    - subtitle: Subtitle text
    - description: Detailed description text
    - metrics: Dictionary of metrics to display
    - risk_scores: DataFrame containing risk scores
    """
    try:
        score = int(round(risk_scores.loc[risk_scores["Группа риска"] == title, "Риск-скор"].values[0], 0))
    except Exception as e:
        print(f"Error getting score for '{title}': {e}")
        score = 0
    
    try:
        score_color = get_color_under_normal_dist(100 - score * 10)
        status_level = get_status_level(100 - score * 10)
    except Exception as e:
        print(f"Error calculating color/status: {e}")
        score_color = "#e5e7eb"
        status_level = "Н/Д"

    # Process status level to display vertically
    status_words = status_level.split()
    status_display = html.Div(
        [html.Div(word, style={"margin": "2px 0"}) for word in status_words],
        style={
            "color": score_color,
            "fontWeight": "600",
            "fontSize": "0.9rem",
            "textAlign": "center",
            "width": "100%",
            "margin": "5px 0 0 0",
            "padding": "0",
            "lineHeight": "0.8",
            "display": "flex",
            "flexDirection": "column",
            "alignItems": "center"
        }
    )

    # Score visualization components
    score_circle = dcc.Graph(
        figure={
            "data": [{
                "type": "pie",
                "values": [score, 10-score],
                "hole": 0.8,
                "marker": {"colors": [score_color, "#e5e7eb"]},
                "rotation": 90,
                "direction": "clockwise",
                "showlegend": False,
                "textinfo": "none",
                "hoverinfo": "none"
            }],
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
    )

    score_display = html.Div(
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
                f"{score}",
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

    # Left section (30% width)
    left_section = html.Div(
        style={
            "flex": "0 0 29%",
            "display": "flex",
            "flexDirection": "column",
            "alignItems": "center",
            "paddingRight": "10px"
        },
        children=[
            html.H2(
                title,
                style={
                    "fontSize": "0.9rem",
                    "fontWeight": "bold",
                    "color": "#111827",
                    "lineHeight": "1.25",
                    "marginBottom": "0.75rem",
                    "alignSelf": "flex-start",
                    "width": "100%",
                    "textAlign": "left"
                }
            ),
            html.Div(
                [score_circle, score_display],
                style={
                    "position": "relative",
                    "width": "70px",
                    "height": "70px",
                    "marginBottom": "0.25rem"
                }
            ),
            status_display
        ]
    )

    # Right section (70% width)
    metrics_display = [
        html.Div(
            [html.Span(f"{key}: "), html.Span(value, style={"fontWeight": "bold"})],
            style={"fontSize": "0.75rem", "color": "#111827"}
        )
        for key, value in metrics.items()
    ]

    right_section = html.Div(
        style={
            "flex": "1",
            "paddingLeft": "10px",
            "borderLeft": "1px solid #e5e7eb"
        },
        children=[
            html.H3(
                subtitle,
                style={
                    "fontSize": "0.8rem",
                    "fontWeight": "600",
                    "color": "#111827",
                    "marginBottom": "0.5rem"
                }
            ),
            html.P(
                description,
                style={
                    "color": "#374151",
                    "fontSize": "0.75rem",
                    "lineHeight": "1.4",
                    "marginBottom": "0.75rem"
                }
            ),
            html.Div(
                metrics_display,
                style={
                    "display": "flex",
                    "gap": "0.75rem",
                    "flexWrap": "wrap",
                    "marginTop": "0.25rem"
                }
            )
        ]
    )

    # Main card container
    return html.Div(
        style={
            "flex": "0 0 50%",
            "backgroundColor": "white",
            "border": "1px solid #e5e7eb",
            "borderRadius": "0.5rem",
            "padding": "0.25rem 1rem 0.75rem 1rem",
            "boxSizing": "border-box",
            "fontFamily": "Calibri"
        },
        children=[
            html.Div(
                [left_section, right_section],
                style={
                    "display": "flex",
                    "width": "100%",
                    "height": "100%"
                }
            )
        ]
    )
    
#[template_elements_img/metabolite_row.png]
def render_metabolite_row(concentration, ref_stats_entry, subtitle):
    """
    Render a metabolite row with title, subtitle (if exists), concentration value, and reference stats
    
    Parameters:
    - concentration: Current concentration value
    - ref_stats_entry: Reference statistics dictionary entry
    - subtitle: Description (e.g., "Незаменимая глюко-, кетогенная аминокислота") or empty string
    """
    # Determine if we should show the subtitle
    show_subtitle = bool(subtitle.strip())
    
    return html.Div(
        style={'margin': '0px'},
        children=[
            html.Div(
                style={'margin': '0px', 'margin-left': '20px'},
                children=[
                    html.Div(
                        style={
                            'width': '100%',
                            'display': 'flex', 
                            'justify-content': 'space-between',
                            'height': '45px' if not show_subtitle else '53px',  # Adjust height based on subtitle
                            'margin-left': '5px'
                        },
                        children=[
                            # Title and subtitle column (39%)
                            html.Div(
                                style={
                                    'width': '39%',
                                    'height': '45px' if not show_subtitle else '53px',
                                    'margin': '0px',
                                    'font-size': '15px',
                                    'font-family': 'Calibri',
                                    'color': 'black',
                                    'display': 'flex',
                                    'flex-direction': 'column',
                                    'justify-content': 'center'  # Center vertically
                                },
                                children=[
                                    html.B(ref_stats_entry["name_view"], style={'height': '20px'}),
                                    html.P(
                                        subtitle,
                                        style={
                                            'height': '20px',
                                            'font-size': '12px',
                                            'font-family': 'Calibri',
                                            'color': '#2563eb',
                                            'margin': '0px',
                                            'margin-left': '5px',
                                            'line-height': '0.9em',
                                            'display': 'none' if not show_subtitle else 'block'  # Hide if no subtitle
                                        }
                                    ) if subtitle else None  # Don't render at all if no subtitle
                                ]
                            ),
                            
                            # Concentration value column (8%)
                            html.Div(
                                style={
                                    'width': '8%',
                                    'height': '45px' if not show_subtitle else '53px',
                                    'margin': '0px',
                                    'font-size': '15px',
                                    'font-family': 'Calibri',
                                    'color': color_text_ref(concentration, ref_stats_entry=ref_stats_entry),
                                    'display': 'flex',
                                    'align-items': 'center',
                                    'justify-content': 'center'
                                },
                                children=[
                                    html.Div(
                                        html.B(
                                            smart_round(concentration, ref_stats_entry=ref_stats_entry),
                                            style={
                                                'text-align': 'center',
                                                'background-color': heighlight_out_of_range(concentration, ref_stats_entry=ref_stats_entry),
                                                'padding': '3px 8px', 
                                                'borderRadius': '12px'
                                            }
                                        )
                                    )
                                ]
                            ),
                            
                            # Progress bar column (27%)
                            html.Div(
                                style={
                                    'width': '27%', 
                                    'height': '45px' if not show_subtitle else '53px', 
                                    'margin': '0px', 
                                    'font-size': '15px', 
                                    'font-family': 'Calibri', 
                                    'color': '#2563eb', 
                                    'display': 'flex',
                                    'align-items': 'center',
                                    'position': 'relative'
                                },
                                children=[
                                    html.Div(
                                        style={
                                            'width': '100%',
                                            'position': 'relative'
                                        },
                                        children=[
                                            # Progress bar
                                            html.Img(
                                                src="assets/progress.png" if ref_stats_entry["ref_min"] != 0 else "assets/progress_left.png",
                                                style={
                                                    'width': '100%', 
                                                    'height': '18px', 
                                                    'line-height': 'normal', 
                                                    'display': 'inline-block', 
                                                    'vertical-align': 'center'
                                                }
                                            ),
                                            # Pointer (arrow)
                                            html.Img(
                                                src='assets/pointer.png', 
                                                style={
                                                    'position': 'absolute',
                                                    'height': '38px',
                                                    'width': '4px',
                                                    'left': f'{calculate_pointer_position(concentration, ref_stats_entry=ref_stats_entry)}%',
                                                    'top': '50%',
                                                    'transform': 'translate(-50%, -50%)'
                                                }
                                            )
                                        ]
                                    )
                                ]
                            ),
                            
                            # Reference range column (21%)
                            html.Div(
                                style={
                                    'width': '21%',
                                    'height': '45px' if not show_subtitle else '53px',
                                    'margin': '0px',
                                    'font-size': '15px',
                                    'font-family': 'Calibri',
                                    'color': 'black',
                                    'display': 'flex',
                                    'align-items': 'center',
                                    'justify-content': 'center'
                                },
                                children=[
                                    html.P(
                                        ref_stats_entry["norm"],
                                        style={
                                            'height': '20px',
                                            'line-height': 'normal',
                                            'display': 'inline-block',
                                            'vertical-align': 'center',
                                            'margin': '0'
                                        }
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )

def render_category_header(order_number, title):
    """
    Render a category header with blue background and white text
    
    Parameters:
    - title: The header text to display (e.g., "4. Метаболизм жирных кислот")
    """
    return html.Div(
        style={
            'width': '100%',
            'background-color': '#2563eb',
            'border-radius': '5px 5px 0px 0px',
            'color': 'white',
            'font-family': 'Calibri',
            'margin': '0px',
            'height': '35px',
            'line-height': '35px',
            'text-align': 'center',
            'margin-top': '5px'
        },
        children=[
            html.H3(
                children=order_number + '. ' + title,
                style={
                    'textAlign': 'center',
                    'margin': '0px',
                    'line-height': 'normal',
                    'display': 'inline-block',
                    'vertical-align': 'center'
                }
            )
        ]
    )

def render_metabolite_category_header(title):
    """
    Render a metabolite category header with title, scale markers, and reference label
    
    Parameters:
    - title: The category title to display (e.g., "Индоловый путь")
    """
    return html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.B(title, style={
                        'height': '20px',
                        'line-height': 'normal',
                        'display': 'inline-block',
                        'vertical-align': 'center'
                    })
                ], style={
                    'width': '39%',
                    'height': '40px',
                    'margin': '0px',
                    'font-size': '16px',
                    'font-family': 'Calibri',
                    'color': '#2563eb',
                    'line-height': '40px'
                }),
                html.Div([
                    html.Div('Результат', style={
                        'display': 'inline-block',
                        'fontSize': '14px',
                        'color': '#4D5052',
                        'fontWeight': '500'
                    })
                ], style={
                    'width': '7%',
                    'height': '20px',
                    'margin': '0px',
                    'font-size': '15px',
                    'font-family': 'Calibri',
                    'color': 'black',
                    'text-align': 'center'
                }),
                html.Div([
                    html.Div([
                        html.Span('20%', style={
                            'display': 'inline-block',
                            'width': '25%',
                            'text-align': 'center'
                        }),
                        html.Span('40%', style={
                            'display': 'inline-block',
                            'width': '25%',
                            'text-align': 'center'
                        }),
                        html.Span('60%', style={
                            'display': 'inline-block',
                            'width': '25%',
                            'text-align': 'center'
                        }),
                        html.Span('80%', style={
                            'display': 'inline-block',
                            'width': '25%',
                            'text-align': 'center'
                        }),
                    ], style={
                        'width': '100%',
                        'display': 'flex',
                        'justify-content': 'space-between',
                        'font-family': 'Calibri',
                        'color': '#4D5052',
                        'font-size': '13px',
                        'padding': '4px 8px',
                    })
                ], style={'width': '27%', 'margin': '0px'}),
                html.Div([
                    html.Div('Норма, мкмоль/л')
                ], style={
                    'width': '21%',
                    'height': '20px',
                    'margin': '0px',
                    'font-size': '14px',
                    'font-family': 'Calibri',
                    'color': '#4D5052',
                    'text-align': 'center'
                }),
            ], style={
                'width': '100%',
                'display': 'flex',
                'alignItems': 'center',
                'justify-content': 'space-between',
                'height': '40px'
            }), 
        ], style={'margin': '0px', 'margin-left': '20px'})
    ])
    
def render_page_header(date, name, logo_height='53px'):
    """
    Render the main header with date/name on left and logo on right
    
    Parameters:
    - date: Date string to display
    - name: Patient name string to display
    - logo_height: Height of the logo image (default '53px')
    """
    return html.Div(
        style={
            'display': 'flex',
            'justify-content': 'space-between',
            'width': '100%',
            'height': '53px',
            'color': '#2563eb'
        },
        children=[
            # Left section with date and name
            html.Div(
                style={'width': '50%'},
                children=[
                    html.B(
                        f"Дата: {date}",
                        style={
                            'margin': '0px',
                            'font-size': '18px',
                            'font-family': 'Calibri'
                        }
                    ),
                    html.Div(
                        style={'margin-top': '2px'},
                        children=[
                            html.B(
                                f'Пациент: {name}',
                                style={
                                    'margin': '0px',
                                    'font-size': '18px',
                                    'font-family': 'Calibri'
                                }
                            )
                        ]
                    )
                ]
            ),
            
            # Right section with logo
            html.Div(
                style={'width': '50%', 'text-align': 'right'},
                children=[
                    html.Img(
                        src=app.get_asset_url('logo.jpg'),
                        style={
                            'height': logo_height,
                            'float': 'right'
                        }
                    )
                ]
            )
        ]
    )

def render_page_footer(page_number):
    """
    Render a standardized page footer with disclaimer and page number
    
    Parameters:
    - page_number: The page number to display (e.g., 4)
    - margin_top: Top margin for the footer container (default '10px')
    """
    return html.Div(
        style={
            'page-break-after': 'always',
            'margin': '0px',
            'display': 'flex',
            'justify-content': 'space-between',
            'width': '100%',
            'margin-top': '10px'
        },
        children=[
            # Disclaimer text
            html.P(
                'Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
                style={
                    'color': 'black',
                    'font-family': 'Calibri',
                    'font-size': '14px',
                    'margin': '0px',
                    'text-align': "left",
                    'font-style': 'italic',
                    'width': '85%'
                }
            ),
            # Page number
            html.P(
                f'|{page_number}',
                style={
                    'color': 'black',
                    'font-family': 'Calibri',
                    'font-size': '14px',
                    'margin': '0px',
                    'text-align': "right",
                    'font-style': 'italic',
                    'margin-top': '15px',  # Note: Overrides the 5px from parent
                    'width': '10%'
                }
            )
        ]
    )
    
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
        ref_params = pd.read_excel(risk_params_path)
        
        # Generate radial diagram
        radial_path = os.path.join('assets', "radial_diagram.png")
        generate_radial_diagram(risk_scores, radial_path)
                
        
        # vascular_data = [
        #         {
        #             "name": "Аргинин/ADMA",
        #             "value": smart_round(metabolite_data['Arg/ADMA'], 2),
        #             "norm": '33.93 - 290.07',
        #             "description": "Отражает баланс между доступным для синтеза оксида азота (NO) аргинином и ингибитором синтеза NO – асимметричным диметиларгинином (ADMA).",
        #         },
        #         {
        #             "name": "(Аргинин + Гомоаргинин) / ADMA",
        #             "value": smart_round(metabolite_data['(Arg+HomoArg)/ADMA'], 2),
        #             "norm": '37.49 - 298.4',
        #             "description": "Отражает общий баланс сосудорасширяющих (вазопротективных) и сосудосуживающих (вазопатогенных) факторов, связанных с синтезом оксида азота (NO) и эндотелиальной функцией.",
        #         },
        #         {
        #             "name": "GABR = Аргинин / (Орнитин + Цитруллин)",
        #             "value": smart_round(metabolite_data['GABR'], 2),
        #             "norm": '0.29 - 1.53',
        #             "description": "Отражает активность и баланс обменных процессов в цикле мочевины и доступность аргинина как субстрата для синтеза оксида азота (NO).",
        #         },
        #         {
        #             "name": "ADMA / (Аденозин + Аргинин)",
        #             "value": smart_round(metabolite_data['ADMA/(Adenosin+Arginine)'], 3),
        #             "norm": '0.001 - 0.011',
        #             "description": "Отражает баланс между сосудосуживающими и воспалительными влияниями (связанными с ADMA) и сосудорасширяющими, защитными эффектами, обусловленными аденозином и аргинином.",
        #         },
        #         {
        #             "name": "ADMA / Аргинин",
        #             "value":  smart_round(1 / metabolite_data['Arg/ADMA'], 3),
        #             "norm": '0.001 - 0.011',
        #             "description": "Отражает степень метилирования аргинина, приводящего к образованию асимметричного диметиларгинина (ADMA), в сравнении с доступностью аргинина.",
        #         },
        #         {
        #             "name": "SDMA / Аргинин",
        #             "value":  smart_round(metabolite_data['Symmetrical Arg Methylation'], 3),
        #             "norm": '0.001 - 0.011',
        #             "description": "Отражает степень метилирования аргинина, приводящего к образованию симметричного диметиларгинина (SDMA), в сравнении с доступностью аргинина.",
        #         },
        #         {
        #             "name": "Сумма диметилированных производных аргинина (ADMA+SDMA)",
        #             "value":  smart_round(metabolite_data['Sum of Dimethylated Arg'], 2),
        #             "norm": '0.79 - 1.83',
        #             "description": "Отражает общий уровень метилированных производных аргинина, связанных с сосудистым воспалением, эндотелиальной дисфункцией и состоянием почечной фильтрации.",
        #         },
        #     ]
        
        # inflammation_data = [
        #     {
        #         "name": "Кинуренин / Триптофан (Kyn/Trp)",
        #         "value": smart_round(metabolite_data['Kynurenine / Trp'], 3),
        #         "norm": "0.015 - 0.048",
        #         "description": "Отражает активность кинуренинового пути обмена триптофана, тесно связанного с воспалением, состоянием иммунной системы и оксидативным стрессом."
        #     },
        #     {
        #         "name": "Триптофан / Кинуренин (Trp/Kyn)",
        #         "value": smart_round(1 / metabolite_data['Kynurenine / Trp'], 2),
        #         "norm": "15.00 - 48.80",
        #         "description": "Является обратным показателем Kyn/Trp и отражает доступность триптофана относительно его воспалительного метаболита кинуренина. Он характеризует запас триптофана и интенсивность его потребления через кинурениновый путь при воспалении и иммунной активации."
        #     },
        #     {
        #         "name": "Trp/(Kyn+QA)",
        #         "value": smart_round(metabolite_data['Trp/(Kyn+QA)'], 2),
        #         "norm": "13.29 - 38.78",
        #         "description": "Это соотношение концентрации триптофана к сумме его метаболитов (кинуренина и хинолиновой кислоты). Он является важным маркером воспалительного и нейротоксического стресса, отражая баланс между доступным триптофаном и продуктами воспалительного катаболизма (психоэмоц. статус)."
        #     },
        #     {
        #         "name": "Кинуренин / Хинолиновая кислота (Kyn/QА)",
        #         "value": smart_round(metabolite_data['Kyn/Quin'], 2),
        #         "norm": "0.98 - 7.90",
        #         "description": "Отражает баланс между промежуточными метаболитами кинуренинового пути: относительно нейтральным по действию кинуренином и нейротоксичным метаболитом хинолиновой кислотой (QА). Этот показатель важен для оценки уровня воспаления, нейротоксичности и оксидативного стресса."
        #     },
        #     {
        #         "name": "Серотонин / Триптофан (Ser/Trp)",
        #         "value": smart_round(metabolite_data['Serotonin / Trp'], 2),
        #         "norm": "< 0.03",
        #         "description": "Отражает эффективность превращения аминокислоты триптофана в нейромедиатор серотонин (5-HT), тем самым характеризуя функциональное состояние серотонинергической системы и баланс эмоционального и психического статуса."
        #     },
        #     {
        #         "name": "Триптамин / Индол-3-уксусная кислота (ТА/IAA)",
        #         "value": smart_round(metabolite_data['Tryptamine / IAA'], 2),
        #         "norm": "< 0.13",
        #         "description": "Отражает баланс в микробном метаболизме триптофана в кишечнике и характеризует состояние кишечной микробиоты и кишечного барьера."
        #     },
        #     {
        #         "name": "TMAO Synthesis = TMAO / (Betaine+C0+Choline)",
        #         "value": smart_round(metabolite_data['TMAO Synthesis'], 4),
        #         "norm": "0.0007 - 0.0713",
        #         "description": "Отражает интенсивность образования триметиламин-N-оксида (TMAO) из его предшественников (бетаина, холина и карнитина), характеризуя активность кишечной микробиоты и риск воспаления и атеросклероза."
        #     }
        # ]

        # methylation_data = [
        #     {
        #         "name": "Бетаин/Холин (Bet/Chl)",
        #         "value": smart_round(metabolite_data['Betaine/choline'], 2),
        #         "norm": "1.14 - 7.57",
        #         "description": "Отражает активность обмена холина и степень его конверсии в бетаин, характеризуя функциональное состояние печени, эффективность процессов метилирования и риск развития жировой болезни печени (стеатоза)."
        #     },
        #     {
        #         "name": "Диметилглицин / Холин (DMG/Chl)",
        #         "value": smart_round(metabolite_data['DMG / Choline'], 3),
        #         "norm": "0.005 - 0.060",
        #         "description": "Отражает активность пути метилирования, эффективность обмена холина и функционирование печени."
        #     },
        #     {
        #         "name": "Cумма концентраций метионина и таурина (∑(Met + Tau))",
        #         "value": smart_round(metabolite_data['Methionine + Taurine'], 2),
        #         "norm": "58.22 - 180.08",
        #         "description": "Отражает совокупный запас метаболитов, участвующих в антиоксидантной защите, детоксикации, метилировании и регуляции клеточного метаболизма."
        #     },
        #     {
        #         "name": "Met Oxidation = MetSO / Met",
        #         "value": smart_round(metabolite_data['Met Oxidation'], 4),
        #         "norm": "< 0.0319",
        #         "description": "Отражает степень окисления метионина до его окисленного метаболита (метионин-сульфоксида), являясь прямым маркером оксидативного стресса и антиоксидантной защиты организма."
        #     }
        # ]

        # energy_metabolism_data = [
        #     {
        #         "name": "Глутамин/Глутамат (Gln/Glu)",
        #         "value": smart_round(metabolite_data['Glutaminase Activity'], 2),
        #         "norm": "0.44 - 3.66",
        #         "description": "Отражает баланс между аминокислотами, участвующими в азотном обмене, регуляции энергетического метаболизма и нейротрансмиттерной активности."
        #     },
        #     {
        #         "name": "Пролин / Цитруллин (Pro/Cit)",
        #         "value": smart_round(metabolite_data['Ratio of Pro to Cit'], 2),
        #         "norm": "1.87 - 9.09",
        #         "description": "Отражает баланс аминокислотного обмена, связанного с циклом мочевины, синтезом аргинина и состоянием энергетического и сосудистого метаболизма организма."
        #     },
        #     {
        #         "name": "Цитруллин / Орнитин (Cit/Orn)",
        #         "value": smart_round(metabolite_data['Cit Synthesis'], 2),
        #         "norm": "0.18 - 0.97",
        #         "description": "Отражает эффективность процесса синтеза цитруллина из орнитина в рамках цикла мочевины, а также функциональное состояние печени, сосудистого здоровья и обмена азота."
        #     },
        #     {
        #         "name": "BCAA",
        #         "value": smart_round(metabolite_data['BCAA'], 2),
        #         "norm": "299.69 - 531.01",
        #         "description": "Отражает общий уровень трёх аминокислот: валина (Val), лейцина (Leu) и изолейцина (Ile). Эти аминокислоты важны для оценки энергетического метаболизма, мышечного и печёночного обмена, риска развития метаболического синдрома, диабета и сердечно-сосудистых заболеваний."
        #     },
        #     {
        #         "name": "Индекс Фишера (BCAA/AAAs)",
        #         "value": smart_round(metabolite_data['BCAA/AAA'], 2),
        #         "norm": "1.84 - 4.31",
        #         "description": "Индекс Фишера, отношение аминокислот с разветвлённой цепью к ароматическим аминокислотам - отражает баланс между группами аминокислот и используется для оценки функционального состояния печени, метаболического статуса и риска печёночной энцефалопатии."
        #     },
        #     {
        #         "name": "Фенилаланин / Тирозин (Phe/Tyr)",
        #         "value": smart_round(metabolite_data['Phe/Tyr'], 2),
        #         "norm": "0.42 - 1.58",
        #         "description": "Отражает активность фермента фенилаланин-гидроксилазы, участвующего в превращении фенилаланина в тирозин, и является маркером состояния функции печени и процессов метаболизма аминокислот."
        #     },
        #     {
        #         "name": "Глицин / Серин (Gly/Ser)",
        #         "value": smart_round(metabolite_data['Glycine/Serine'], 2),
        #         "norm": "0.59 - 2.72",
        #         "description": "Отражает баланс между двумя важными аминокислотами, участвующими в процессах метилирования, антиоксидантной защиты, регуляции воспаления и клеточного метаболизма."
        #     },
        #     {
        #         "name": "GSG Index = (Glu/(Ser+Gly))",
        #         "value": smart_round(metabolite_data['GSG Index'], 4),
        #         "norm": "0.0844 - 0.66",
        #         "description": "Отражает баланс между возбуждающей нейромедиаторной активностью и антиоксидантной, противовоспалительной защитой организма."
        #     }
        # ]

        # mitochondrial_data = [
        #     {
        #         "name": "Cоотношение гидрокси- ацилкарнитинов к общим ацилкарнитинам (AC-OHs/ACs)",
        #         "value": smart_round(metabolite_data['Ratio of AC-OHs to ACs'], 4),
        #         "norm": "0.0004 - 0.0013",
        #         "description": "Отражает эффективность β-окисления жирных кислот в митохондриях и характеризует митохондриальную функцию и энергетический обмен организма."
        #     },
        #     {
        #         "name": "Cоотношение среднецепочечных к длинноцепочечным ацилкарнитинам (ССК/СДК)",
        #         "value": smart_round(metabolite_data['Ratio of Medium-Chain to Long-Chain ACs'], 2),
        #         "norm": "0.75 - 1.79",
        #         "description": "Отражает эффективность β-окисления жирных кислот разной длины цепи в митохондриях, а также способность организма эффективно использовать жирные кислоты в качестве источника энергии."
        #     },
        #     {
        #         "name": "Cумма длинноцепочечных ацилкарнитинов (СДК)",
        #         "value": smart_round(metabolite_data['СДК'], 2),
        #         "norm": "0.28 - 0.45",
        #         "description": "Отражает общий уровень длинноцепочечных ацилкарнитинов (С14–С18), которые являются промежуточными метаболитами β-окисления жирных кислот в митохондриях."
        #     },
        #     {
        #         "name": "Cумма среднецепочечных ацилкарнитинов (ССК)",
        #         "value": smart_round(metabolite_data['ССК'], 2),
        #         "norm": "0.31 - 0.62",
        #         "description": "Отражает общий уровень среднецепочечных ацилкарнитинов (С6–С12), которые являются промежуточными метаболитами β-окисления жирных кислот средней длины в митохондриях."
        #     },
        #     {
        #         "name": "Cумма короткоцепочечных ацилкарнитинов (СКК)",
        #         "value": smart_round(metabolite_data['СКК'], 2),
        #         "norm": "4.37 - 12.93",
        #         "description": "Отражает общий уровень короткоцепочечных ацилкарнитинов (С2–С5), которые являются промежуточными метаболитами β-окисления короткоцепочечных жирных кислот и аминокислотного обмена в митохондриях."
        #     },
        #     {
        #         "name": "C0/(C16+C18)",
        #         "value": smart_round(metabolite_data['C0/(C16+C18)'], 2),
        #         "norm": "171.58 - 603.84",
        #         "description": "Отражает баланс между свободным карнитином и длинноцепочечными ацилкарнитинами, характеризуя способность митохондрий эффективно транспортировать и окислять длинноцепочечные жирные кислоты."
        #     },
        #     {
        #         "name": "(C16+C18-1)/C2",
        #         # вопрос
        #         "value": smart_round(metabolite_data['CPT-2 Deficiency (NBS)'], 4),
        #         "norm": "0.0041 - 0.0182",
        #         "description": "Отражает баланс между накоплением длинноцепочечных жирных кислот и эффективностью финальной стадии их окисления до ацетилкарнитина (C2), характеризуя общую эффективность митохондриального β-окисления жирных кислот."
        #     },
        #     {
        #         "name": "С2/С0",
        #         "value": smart_round(metabolite_data['С2/С0'], 2),
        #         "norm": "0.07 - 0.39",
        #         "description": "Отражает баланс между ацетилированной формой карнитина (ацетилкарнитином), образующейся в результате энергетического обмена, и свободным карнитином, необходимым для транспорта жирных кислот в митохондрии."
        #     }
        # ]
        
        # mytochondrial_data_2 = [
        #     {
        #         "name": "Cоотношение короткоцепочечных к длинноцепочечным ацилкарнитинам (СКК/СДК)",
        #         "value": smart_round(metabolite_data['Ratio of Short-Chain to Long-Chain ACs'], 2),
        #         "norm": "10.72 - 36.56",
        #         "description": "Отражает баланс между короткоцепочечными и длинноцепочечными ацилкарнитинами, характеризуя соотношение активности окисления короткоцепочечных жирных кислот и аминокислот к активности окисления длинноцепочечных жирных кислот."
        #     },
        #     {
        #         "name": "Cоотношение короткоцепочечных к среднецепочечным ацилкарнитинам (СКК/ССК)",
        #         "value": smart_round(metabolite_data['Ratio of Short-Chain to Medium-Chain ACs'], 2),
        #         "norm": "7.44 - 29.81",
        #         "description": "Отражает баланс между короткоцепочечными и среднецепочечными ацилкарнитинами и характеризует эффективность митохондриального окисления жирных кислот разной длины цепи, а также баланс аминокислотного обмена."
        #     },
        #     {
        #         "name": "Общая сумма ацилкарнитинов (∑AСs)",
        #         "value": smart_round(metabolite_data['Sum of ACs'], 2),
        #         "norm": "5.20 - 13.77",
        #         "description": "Отражает общий уровень ацилкарнитинов различной длины цепи (коротко-, средне-, длинноцепочечные), являясь интегральным маркером состояния митохондриального β-окисления жирных кислот и аминокислотного обмена."
        #     },
        #     {
        #         "name": "Сумма ацилкарнитинов и свободного карнитина (∑AСs) + С0)",
        #         "value": smart_round(metabolite_data['Sum of ACs + С0'], 2),
        #         "norm": "28.39 - 59.97",
        #         "description": "Отражает общий пул карнитина в организме, включая как свободную форму карнитина (С0), так и все связанные формы (ацилкарнитины различной длины цепи). Является интегральным маркером состояния карнитинового обмена, митохондриальной функции и энергетического метаболизма."
        #     },
        #     {
        #         "name": "Отношение общей суммы ацилкарнитинов к свободному карнитину (∑ACs/C0)",
        #         "value":  smart_round(metabolite_data['Sum of ACs/C0'], 2),
        #         "norm": "0.10 - 0.45",
        #         "description": "Отражает баланс между связанными формами карнитина (ацилкарнитины) и свободным карнитином (С0), являясь важным интегральным индикатором митохондриальной функции, карнитинового обмена и общего энергетического статуса организма."
        #     }]
        
        fig_phenylalanine_metabolism = plot_metabolite_z_scores(
        metabolite_concentrations={
                "Phenylalanine": metabolite_data["Phenylalanine"],
                "Tyrosin": metabolite_data["Tyrosin"],
                "Summ Leu-Ile": metabolite_data["Summ Leu-Ile"],
                "Valine": metabolite_data["Valine"],
                "BCAA": metabolite_data["BCAA"],
                "BCAA/AAA": metabolite_data["BCAA/AAA"],
                "Phe/Tyr": metabolite_data["Phe/Tyr"],
                "Val/C4": metabolite_data["Val/C4"],
                "(Leu+IsL)/(C3+С5+С5-1+C5-DC)": metabolite_data["(Leu+IsL)/(C3+С5+С5-1+C5-DC)"],
            },
            group_title="Метаболизм фенилаланина"
        )
        
        fig_histidine_metabolism = plot_metabolite_z_scores(
            metabolite_concentrations={
                "Histidine": metabolite_data["Histidine"],
                "Methylhistidine": metabolite_data["Methylhistidine"],
                "Threonine": metabolite_data["Threonine"],
                "Glycine": metabolite_data["Glycine"],
                "DMG": metabolite_data["DMG"],
                "Serine": metabolite_data["Serine"],
                "Lysine": metabolite_data["Lysine"], 
                "Glutamic acid": metabolite_data["Glutamic acid"],
                "Glutamine/Glutamate": metabolite_data["Glutamine"],
                "Glutamine/Glutamate": metabolite_data["Glutamine/Glutamate"],
                "Glycine/Serine": metabolite_data["Glycine/Serine"],
                "GSG Index": metabolite_data["GSG Index"],
                "Carnosine": metabolite_data["Carnosine"],
            },
            group_title="Метаболизм гистидина"
        )
        
        # Methionine Metabolism
        fig_methionine_metabolism = plot_metabolite_z_scores(
            metabolite_concentrations={
                "Methionine": metabolite_data["Methionine"],
                "Methionine-Sulfoxide": metabolite_data["Methionine-Sulfoxide"],
                "Taurine": metabolite_data["Taurine"],
                "Betaine": metabolite_data["Betaine"],
                "Choline": metabolite_data["Choline"],
                "TMAO": metabolite_data["TMAO"],
                "Betaine/choline": metabolite_data["Betaine/choline"],
                "Methionine + Taurine": metabolite_data["Methionine + Taurine"],
                "Met Oxidation": metabolite_data["Met Oxidation"],
                "TMAO Synthesis": metabolite_data["TMAO Synthesis"],
                "DMG / Choline": metabolite_data["DMG / Choline"],
            },
            group_title="Метаболизм метионина"
        )

        # Kynurenine Pathway
        fig_kynurenine_pathway = plot_metabolite_z_scores(
            metabolite_concentrations={
                "Tryptophan": metabolite_data["Tryptophan"],
                "Kynurenine": metabolite_data["Kynurenine"],
                "Antranillic acid": metabolite_data["Antranillic acid"],
                "Quinolinic acid": metabolite_data["Quinolinic acid"],
                "Xanthurenic acid": metabolite_data["Xanthurenic acid"],
                "Kynurenic acid": metabolite_data["Kynurenic acid"],
                "Kyn/Trp": metabolite_data["Kyn/Trp"],
                "Trp/(Kyn+QA)": metabolite_data["Trp/(Kyn+QA)"],
                "Kyn/Quin": metabolite_data["Kyn/Quin"],
            },
            group_title="Кинурениновый путь"
        )

        # Serotonin Pathway
        fig_serotonin_pathway = plot_metabolite_z_scores(
            metabolite_concentrations={
                "Serotonin": metabolite_data["Serotonin"],
                "HIAA": metabolite_data["HIAA"],
                "5-hydroxytryptophan": metabolite_data["5-hydroxytryptophan"],
                "Serotonin / Trp": metabolite_data["Serotonin / Trp"],
            },
            group_title="Серотониновый путь"
        )

        # Indole Pathway
        fig_indole_pathway = plot_metabolite_z_scores(
            metabolite_concentrations={
                "Indole-3-acetic acid": metabolite_data["Indole-3-acetic acid"],
                "Indole-3-lactic acid": metabolite_data["Indole-3-lactic acid"],
                "Indole-3-carboxaldehyde": metabolite_data["Indole-3-carboxaldehyde"],
                "Indole-3-propionic acid": metabolite_data["Indole-3-propionic acid"],
                "Indole-3-butyric": metabolite_data["Indole-3-butyric"],
                "Tryptamine": metabolite_data["Tryptamine"],
                "Tryptamine / IAA": metabolite_data["Tryptamine / IAA"],
            },
            group_title="Индоловый путь"
        )

        # Arginine Metabolism
        fig_arginine_metabolism = plot_metabolite_z_scores(
            metabolite_concentrations={
                "Proline": metabolite_data["Proline"],
                "Hydroxyproline": metabolite_data["Hydroxyproline"],
                "ADMA": metabolite_data["ADMA"],
                "NMMA": metabolite_data["NMMA"],
                "TotalDMA (SDMA)": metabolite_data["TotalDMA (SDMA)"],
                "Homoarginine": metabolite_data["Homoarginine"],
                "Arginine": metabolite_data["Arginine"],
                "Citrulline": metabolite_data["Citrulline"],
                "Ornitine": metabolite_data["Ornitine"],
                "Asparagine": metabolite_data["Asparagine"],
                "Aspartic acid": metabolite_data["Aspartic acid"],
                "Creatinine": metabolite_data["Creatinine"],
                "Arg/ADMA": metabolite_data["Arg/ADMA"],
                "(Arg+HomoArg)/ADMA": metabolite_data["(Arg+HomoArg)/ADMA"],
                "Arg/Orn+Cit": metabolite_data["Arg/Orn+Cit"],
                "ADMA/(Adenosin+Arginine)": metabolite_data["ADMA/(Adenosin+Arginine)"],
                "Symmetrical Arg Methylation": metabolite_data["Symmetrical Arg Methylation"],
                "Sum of Dimethylated Arg": metabolite_data["Sum of Dimethylated Arg"],
                "Ratio of Pro to Cit": metabolite_data["Ratio of Pro to Cit"],
                "Cit Synthesis": metabolite_data["Cit Synthesis"],
            },
            group_title="Метаболизм аргинина"
        )

        # Acylcarnitine Metabolism (ratios)
        fig_acylcarnitine_ratios = plot_metabolite_z_scores(
            metabolite_concentrations={
                "Alanine": metabolite_data["Alanine"],
                "C0": metabolite_data["C0"],
                "Ratio of AC-OHs to ACs": metabolite_data["Ratio of AC-OHs to ACs"],
                "СДК": metabolite_data["СДК"],
                "ССК": metabolite_data["ССК"],
                "СКК": metabolite_data["СКК"],
                "C0/(C16+C18)": metabolite_data["C0/(C16+C18)"],
                "CPT-2 Deficiency (NBS)": metabolite_data["CPT-2 Deficiency (NBS)"],
                "С2/С0": metabolite_data["С2/С0"],
                "Ratio of Short-Chain to Long-Chain ACs": metabolite_data["Ratio of Short-Chain to Long-Chain ACs"],
                "Ratio of Medium-Chain to Long-Chain ACs": metabolite_data["Ratio of Medium-Chain to Long-Chain ACs"],
                "Ratio of Short-Chain to Medium-Chain ACs": metabolite_data["Ratio of Short-Chain to Medium-Chain ACs"],
                "Sum of ACs": metabolite_data["Sum of ACs"],
                "Sum of ACs + С0": metabolite_data["Sum of ACs + С0"],
                "Sum of ACs/C0": metabolite_data["Sum of ACs/C0"],
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
                "Pantothenic": metabolite_data["Pantothenic"],
                "Riboflavin": metabolite_data["Riboflavin"],
                "Melatonin": metabolite_data["Melatonin"],
                "Uridine": metabolite_data["Uridine"],
                "Adenosin": metabolite_data["Adenosin"],
                "Cytidine": metabolite_data["Cytidine"],
                "Cortisol": metabolite_data["Cortisol"],
                "Histamine": metabolite_data["Histamine"],
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
                html.Div(render_category_params('1', 'Метаболическая детоксикация', risk_scores, ref_params), style={'width': '50%'}),
                html.Div(render_category_params('2', 'Здоровье митохондрий', risk_scores, ref_params), style={'width': '50%'}),
            ], style={
                'width': '100%',
                'gap': '20px',
                'margin-top': '10px',
                'display': 'flex',
                'justify-content': 'space-between',
                'height': 'fit-content'}),
            
            # Plot risk_scores table
            html.Div([
                html.Div(render_category_params('3', 'Воспаление и иммунитет', risk_scores, ref_params), style={'width': '50%'}),
                html.Div(render_category_params('4', 'Метаболическая адаптация и стрессоустойчивость', risk_scores, ref_params), style={'width': '50%'}),
            ], style={
                'width': '100%',
                'gap': '20px',
                'margin-top': '10px',
                'display': 'flex',
                'justify-content': 'space-between',
                'height': 'fit-content'}),
            
            # Plot risk_scores table
            html.Div([
                html.Div(
                    render_category_params('5', 'Витаминный статус', risk_scores, ref_params),
                    style={'width': '50%'}
                ),
                html.Div([
                    render_category_params('6', 'Статус микробиоты', risk_scores, ref_params),
                    html.Div(style={'height': '10px'}),
                    render_category_params('7', 'Резистентность к стрессорам', risk_scores, ref_params),
                ], style={
                    'width': '50%',
                    'display': 'flex',
                    'flex-direction': 'column',
                }),
            ], style={
                'width': '100%',
                'gap': '20px',
                'margin-top': '10px',
                'display': 'flex',
                'height': 'fit-content'
            }),

            # Подвал
            render_page_footer(page_number=1),
            
            render_page_header(date=date, name=name),


        html.Div([
            html.Img(src=app.get_asset_url('info_icon.png'), style={'width':'20px','height':'20px','margin-right':'15px'}),
            html.Div('Данные по оценке состояния организма получены из экспериментальных данных на образцах из биобанка Центра биофармацевтического анализа и метаболомных исследований Сеченовского университета.',
                    style={'color':'#3d1502','font-family':'Calibri','font-size':'13px','text-align':"left", 'margin': '0px !important'}),
            ], style={'display': 'flex','margin-top':'10px','margin-bottom':'10px', 'flex-direction': 'row','align-items': 'center', 'width':'fit-content', "borderRadius": "0.5rem", 'padding': '5px 7px 5px 15px', 'background-color': '#fee4cf'}),
            
            # Main container with all score cards
            html.Div(
                style={
                    "width": "100%",
                    "margin": "0 auto",
                    "marginTop": "10px",
                    "fontFamily": "Calibri, Arial, sans-serif",
                    "display": "flex",
                    "flexWrap": "wrap",
                    "gap": "1rem"
                },
                children=[
                    # First row of cards
                    html.Div(
                        style={"width": "100%", "display": "flex", "gap": "1rem"},
                        children=[
                            # Cardiovascular Score Card
                            render_ml_score_card(
                                title="Состояние сердечно-сосудистой системы",
                                subtitle="Отражает метаболическую нагрузку на сердце и сосуды",
                                description='''Оценка данного параметра основана на
                                                анализе реальных образцов плазмы крови
                                                пациентов без признаков ССЗ и пациентов с
                                                различными формами сердечно-сосудистых
                                                нарушений.
                                                ''',
                                metrics={
                                    "Acc": "93,7%",
                                    "Se": "94,4%",
                                    "Sp": "89,7%",
                                    "+PV": "98,2%",
                                    "-PV": "73,2%"
                                },
                                risk_scores=risk_scores
                            ),
                            
                            # Oncology Score Card
                            render_ml_score_card(
                                title="Оценка пролиферативных процессов",
                                subtitle='''Характеризует метаболическую
                                            сбалансированность процессов
                                            клеточного обновления, деления и
                                            апоптоза''',
                                description='''Оценка данного параметра основана на
                                                анализе плазмы крови пациентов без
                                                признаков онкологических заболеваний и
                                                пациентов с различными формами
                                                опухолевых процессов, а именно рак
                                                легкого, рак простаты, рак прямой кишки,
                                                рак молочной железы и гематологические
                                                злокачественные заболевания: лимфомы
                                                и множественная миелома.
                                                ''',
                                metrics={
                                    "Acc": "92,1%",
                                    "Se": "90,5%",
                                    "Sp": "89,2%",
                                    "+PV": "91,8%",
                                    "-PV": "86,1%"
                                },
                                risk_scores=risk_scores
                            )
                        ]
                    ),
                    
                    # Second row of cards
                    html.Div(
                        style={"width": "100%", "display": "flex", "gap": "1rem", "marginTop": "10px"},
                        children=[
                            # Liver Score Card
                            render_ml_score_card(
                                title="Состояние функции печени",
                                subtitle='''Оценивает вовлеченность печени в
                                            обменные и детоксикационные процессы
                                            организма
                                            ''',
                                description='''Оценка данного параметра основана на
                                                анализе плазмы крови пациентов без
                                                признаков заболеваний печени и пациентов с
                                                различными нарушениями гепатобилиарной
                                                функции, включая неалкогольную жировую
                                                болезнь печени (НАЖБП), хронический
                                                гепатит, алкогольное поражение печени и
                                                цирроз.
                                                ''',
                                metrics={
                                    "Acc": "91,8%",
                                    "Se": "90,7%",
                                    "Sp": "87,9%",
                                    "+PV": "92,1%",
                                    "-PV": "85,4%"
                                },
                                risk_scores=risk_scores
                            ),
                            
                            # Pulmonary Score Card
                            render_ml_score_card(
                                title="Состояние дыхательной системы",
                                subtitle='''Показывает метаболическую адаптацию
                                            дыхательной системы к
                                            физиологическим нагрузкам и внешним
                                            факторам''',
                                description='''Оценка данного параметра основана на
                                                анализе плазмы крови пациентов без
                                                признаков легочной дисфункции и
                                                пациентов с хроническими заболеваниями
                                                дыхательных путей, включая бронхиальную
                                                астму, хроническую обструктивную болезнь
                                                легких (ХОБЛ), постковидный синдром и
                                                легочный фиброз.
                                                ''',
                                metrics={
                                    "Acc": "90,4%",
                                    "Se": "88,9%",
                                    "Sp": "86,2%",
                                    "+PV": "89,7%",
                                    "-PV": "84,5%"
                                },
                                risk_scores=risk_scores
                            )
                        ]
                    ),
                    
                    # Third row (single card)
                    html.Div(
                        style={"width": "100%", "display": "flex", "gap": "1rem", "marginTop": "10px"},
                        children=[
                            # Immune Score Card
                            render_ml_score_card(
                                title="Состояние иммунного метаболического баланса",
                                subtitle='''Отражает метаболические отклонения,
                                            связанные с хронической активацией
                                            иммунной системы и воспалением''',
                                description='''Оценка данного параметра основана на
                                                анализе плазмы крови пациентов без
                                                признаков аутоиммунных расстройств и
                                                пациентов с установленным диагнозом
                                                ревматоидного артрита различной степени
                                                активности.''',
                                metrics={
                                    "Acc": "93,7%",
                                    "Se": "94,4%",
                                    "Sp": "89,7%",
                                    "+PV": "98,2%",
                                    "-PV": "73,2%"
                                },
                                risk_scores=risk_scores
                            ),
                            
                            # Empty div to maintain layout
                            render_ml_score_card(
                                title="Состояние иммунного метаболического баланса",
                                subtitle='''Отражает метаболические отклонения,
                                            связанные с хронической активацией
                                            иммунной системы и воспалением''',
                                description='''Оценка данного параметра основана на
                                                анализе плазмы крови пациентов без
                                                признаков аутоиммунных расстройств и
                                                пациентов с установленным диагнозом
                                                ревматоидного артрита различной степени
                                                активности.''',
                                metrics={
                                    "Acc": "93,7%",
                                    "Se": "94,4%",
                                    "Sp": "89,7%",
                                    "+PV": "98,2%",
                                    "-PV": "73,2%"
                                },
                                risk_scores=risk_scores
                            ),
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
                                html.Td([html.B("+PV: "), html.Span('Прогностичность положительного результата (вероятность того, что заболевание присутствует, когда тест положительный)')]),
                            ]),
                            # Row 5
                            html.Tr([
                                html.Td([html.B("-PV: "), html.Span('Прогностичность отрицательного результата (вероятность того, что заболевание отсутствует, когда тест отрицательный)')]),
                            ]),
                        ], style={'width': '100%', 'border-collapse': 'collapse'}),
                    ], style={
                        'margin-bottom': '5px',
                        'font-family': 'Calibri',
                        'font-size': '12px',
                        'color': '#150c77'
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
                    'background-color': "#dbeafe"
                }),
            render_page_footer(page_number=2),
            # Страница 1.1
            
            # 2 страница
            
render_page_header(date=date, name=name),   
                
                
                render_category_header(order_number='1', title='Аминокислоты'),
                
                html.Div([
                    
                        # Metabolism of Phenylalanine
                        render_metabolite_category_header(title="Метаболизм фенилаланина"),
                    
                    
                        # Phenylalanine (Phe)
                        render_metabolite_row(
                            concentration=metabolite_data["Phenylalanine"],
                            ref_stats_entry=ref_stats["Phenylalanine"],
                            subtitle="Незаменимая глюко-, кетогенная аминокислота"
                        ),
                        
                        # Tyrosine (Tyr)
                        render_metabolite_row(
                            concentration=metabolite_data["Tyrosin"],
                            ref_stats_entry=ref_stats["Tyrosin"],
                            subtitle="Заменимая глюко-, кетогенная аминокислота"
                        ),
                        
                        # Leucine + Isoleucine (Leu+Ile)
                        render_metabolite_row(
                            concentration=metabolite_data["Summ Leu-Ile"],
                            ref_stats_entry=ref_stats["Summ Leu-Ile"],
                            subtitle="Незаменимая глюко-, кетогенная аминокислота"
                        ),
                        
                        # Valine (Val)
                        render_metabolite_row(
                            concentration=metabolite_data["Valine"],
                            ref_stats_entry=ref_stats["Valine"],
                            subtitle="Незаменимая глюкогенная аминокислота"
                        ),
                        
                        # Histidine metabolism header
                        render_metabolite_category_header(title="Метаболизм гистидина"),
                        
                        # Histidine (His)
                        render_metabolite_row(
                            concentration=metabolite_data["Histidine"],
                            ref_stats_entry=ref_stats["Histidine"],
                            subtitle="Незаменимая глюкогенная аминокислота"
                        ),
                        
                        # Methylhistidine (MH)
                        render_metabolite_row(
                            concentration=metabolite_data["Methylhistidine"],
                            ref_stats_entry=ref_stats["Methylhistidine"],
                            subtitle="Метаболит карнозина"
                        ),
                        
                        # Threonine (Thr)
                        render_metabolite_row(
                            concentration=metabolite_data["Threonine"],
                            ref_stats_entry=ref_stats["Threonine"],
                            subtitle="Незаменимая глюкогенная аминокислота"
                        ),
                        
                        # Carnosine (Car)
                        render_metabolite_row(
                            concentration=metabolite_data["Carnosine"],
                            ref_stats_entry=ref_stats["Carnosine"],
                            subtitle="Дипептид, состоящий из аланина и гистидина"
                        ),
                        
                        # Glycine (Gly)
                        render_metabolite_row(
                            concentration=metabolite_data["Glycine"],
                            ref_stats_entry=ref_stats["Glycine"],
                            subtitle="Заменимая глюкогенная аминокислота"
                        ),
                        
                        # Dimethylglycine (DMG)
                        render_metabolite_row(
                            concentration=metabolite_data["DMG"],
                            ref_stats_entry=ref_stats["DMG"],
                            subtitle="Промежуточный продукт синтеза глицина"
                        ),
                        
                        # Serine (Ser)
                        render_metabolite_row(
                            concentration=metabolite_data["Serine"],
                            ref_stats_entry=ref_stats["Serine"],
                            subtitle="Заменимая глюкогенная аминокислота"
                        ),
                        
                        # Lysine (Lys)
                        render_metabolite_row(
                            concentration=metabolite_data["Lysine"],
                            ref_stats_entry=ref_stats["Lysine"],
                            subtitle="Незаменимая кетогенная аминокислота"
                        ),
                        
                        # Glutamic acid (Glu)
                        render_metabolite_row(
                            concentration=metabolite_data["Glutamic acid"],
                            ref_stats_entry=ref_stats["Glutamic acid"],
                            subtitle="Заменимая глюкогенная аминокислота"
                        ),
                        
                        # Glutamine (Gln)
                        render_metabolite_row(
                            concentration=metabolite_data["Glutamine"],
                            ref_stats_entry=ref_stats["Glutamine"],
                            subtitle="Заменимая глюкогенная аминокислота"
                        ),
                        
                        # Methionine metabolism header
                        render_metabolite_category_header(title="Метаболизм метионина"),
                        
                        # Methionine (Met)
                        render_metabolite_row(
                            concentration=metabolite_data["Methionine"],
                            ref_stats_entry=ref_stats["Methionine"],
                            subtitle="Незаменимая глюкогенная аминокислота"
                        ),
                        
                        # Methionine sulfoxide (MetSO)
                        render_metabolite_row(
                            concentration=metabolite_data["Methionine-Sulfoxide"],
                            ref_stats_entry=ref_stats["Methionine-Sulfoxide"],
                            subtitle="Продукт окисления метионина"
                        ),
                        
                    ], style={'margin':'0px'}),
                
                render_page_footer(page_number=3),
            
            
            
            # 3 страница
            html.Div([
                
render_page_header(date=date, name=name), 
                
                html.Div([
                    
                    render_metabolite_category_header(title="Метаболизм метионина"),
                    
                    
                        # Taurine (Tau)
                        render_metabolite_row(
                            concentration=metabolite_data["Taurine"],
                            ref_stats_entry=ref_stats["Taurine"],
                            subtitle="Заменимая глюкогенная аминокислота"
                        ),
                        
                        # Betaine (Bet)
                        render_metabolite_row(
                            concentration=metabolite_data["Betaine"],
                            ref_stats_entry=ref_stats["Betaine"],
                            subtitle="Продукт метаболизма холина"
                        ),
                        
                        # Choline (Chl)
                        render_metabolite_row(
                            concentration=metabolite_data["Choline"],
                            ref_stats_entry=ref_stats["Choline"],
                            subtitle="Компонент мембран клеток, источник ацетилхолина"
                        ),
                        
                        # Trimethylamine N-oxide (TMAO)
                        render_metabolite_row(
                            concentration=metabolite_data["TMAO"],
                            ref_stats_entry=ref_stats["TMAO"],
                            subtitle="Продукт метаболизма холина, бетаина и др. бактериями ЖКТ"
                        ),
    
    
                    
                    render_category_header(order_number='2', title='Метаболизм триптофана'),
                    
                    
                    render_metabolite_category_header(title="Кинурениновый путь"),
                    
                    # Tryptophan (Trp)
                    render_metabolite_row(
                        concentration=metabolite_data["Tryptophan"],
                        ref_stats_entry=ref_stats["Tryptophan"],
                        subtitle="Незаменимая глюко-, кетогенная аминокислота",
                    ),
                    
                    # Kynurenine (Kyn)
                    render_metabolite_row(
                        concentration=metabolite_data["Kynurenine"],
                        ref_stats_entry=ref_stats["Kynurenine"],
                        subtitle="Продукт метаболизма триптофана по кинурениновому пути"
                    ),
                    
                    # Anthranilic acid (Ant)
                    render_metabolite_row(
                        concentration=metabolite_data["Antranillic acid"],
                        ref_stats_entry=ref_stats["Antranillic acid"],
                        subtitle="Продукт метаболизма кинуренина"
                    ),
                    
                    # Quinolinic acid (QA)
                    render_metabolite_row(
                        concentration=metabolite_data["Quinolinic acid"],
                        ref_stats_entry=ref_stats["Quinolinic acid"],
                        subtitle="Продукт метаболизма 3-гидроксиантраниловой кислоты"
                    ),
                    
                    # Xanthurenic acid (Xnt)
                    render_metabolite_row(
                        concentration=metabolite_data["Xanthurenic acid"],
                        ref_stats_entry=ref_stats["Xanthurenic acid"],
                        subtitle="Продукт метаболизма кинуренина"
                    ),
                                
                    render_metabolite_row(
                        concentration=metabolite_data["Kynurenic acid"],
                        ref_stats_entry=ref_stats["Kynurenic acid"],
                        subtitle="Продукт метаболизма триптофана по кинурениновому пути"
                    ),
                   
                    render_metabolite_category_header(title="Серотониновый путь"),
                    
                    # Serotonin (Ser)
                    render_metabolite_row(
                        concentration=metabolite_data["Serotonin"],
                        ref_stats_entry=ref_stats["Serotonin"],
                        subtitle="Нейромедиатор"
                    ),
                    
                    # 5-Hydroxyindoleacetic acid (5-HIAA)
                    render_metabolite_row(
                        concentration=metabolite_data["HIAA"],
                        ref_stats_entry=ref_stats["HIAA"],
                        subtitle="Метаболит серотонина"
                    ),
                    
                    # 5-Hydroxytryptophan (5-HTP)
                    render_metabolite_row(
                        concentration=metabolite_data["5-hydroxytryptophan"],
                        ref_stats_entry=ref_stats["5-hydroxytryptophan"],
                        subtitle="Прекурсор серотонина"
                    ),
                    
                    render_metabolite_category_header(title="Индоловый путь"),
                    
                    # 3-Indoleacetic acid (IAA)
                    render_metabolite_row(
                        concentration=metabolite_data["Indole-3-acetic acid"],
                        ref_stats_entry=ref_stats["Indole-3-acetic acid"],
                        subtitle="Продукт катаболизма триптофана кишечной микробиотой"
                    ),
                    
                    # 3-Indolelactic acid (ILA)
                    render_metabolite_row(
                        concentration=metabolite_data["Indole-3-lactic acid"],
                        ref_stats_entry=ref_stats["Indole-3-lactic acid"],
                        subtitle="Продукт катаболизма триптофана кишечной микробиотой"
                    ),
                    
                ], style={'margin':'0px'}),
            ]),
            render_page_footer(page_number=4),
            #4 страница
            html.Div([
                
render_page_header(date=date, name=name), 
                
                html.Div([
                    
                    html.Div([
                        render_metabolite_category_header('Индоловый путь'),
                        
                        # ICAA
                        render_metabolite_row(
                            concentration=metabolite_data["Indole-3-carboxaldehyde"],
                            ref_stats_entry=ref_stats["Indole-3-carboxaldehyde"],
                            subtitle="Продукт катаболизма триптофана кишечной микробиотой"
                        ),
                        
                        # IPA
                        render_metabolite_row(
                            concentration=metabolite_data["Indole-3-propionic acid"],
                            ref_stats_entry=ref_stats["Indole-3-propionic acid"],
                            subtitle="Продукт катаболизма триптофана кишечной микробиотой"
                        ),
                        
                        # IBA
                        render_metabolite_row(
                            concentration=metabolite_data["Indole-3-butyric"],
                            ref_stats_entry=ref_stats["Indole-3-butyric"],
                            subtitle="Продукт катаболизма триптофана кишечной микробиотой"
                        ),
                        
                        # TA
                        render_metabolite_row(
                            concentration=metabolite_data["Tryptamine"],
                            ref_stats_entry=ref_stats["Tryptamine"],
                            subtitle="Продукт катаболизма триптофана кишечной микробиотой, прекурсор для нейромедиаторов"
                        ),
                        
                        # Arginine Metabolism Section
                        render_category_header(order_number='3', title='Метаболизм аргинина'),
                        
                        render_metabolite_category_header('Метаболизм аргинина'),
                        
                        # Pro
                        render_metabolite_row(
                            concentration=metabolite_data["Proline"],
                            ref_stats_entry=ref_stats["Proline"],
                            subtitle="Заменимая глюкогенная аминокислота"
                        ),
                        
                        # Hyp
                        render_metabolite_row(
                            concentration=metabolite_data["Hydroxyproline"],
                            ref_stats_entry=ref_stats["Hydroxyproline"],
                            subtitle="Источник коллагена"
                        ),
                        
                        # ADMA
                        render_metabolite_row(
                            concentration=metabolite_data["DMG"],
                            ref_stats_entry=ref_stats["DMG"],
                            subtitle="Эндогенный ингибитор синтазы оксида азота"
                        ),
                        
                        # MMA
                        render_metabolite_row(
                            concentration=metabolite_data["NMMA"],
                            ref_stats_entry=ref_stats["NMMA"],
                            subtitle="Эндогенный ингибитор синтазы оксида азота"
                        ),
                        
                        # SDMA
                        render_metabolite_row(
                            concentration=metabolite_data["TotalDMA (SDMA)"],
                            ref_stats_entry=ref_stats["TotalDMA (SDMA)"],
                            subtitle="Продукт метаболизма аргинина, выводится с почками"
                        ),
                        
                        # HomoArg
                        render_metabolite_row(
                            concentration=metabolite_data["Homoarginine"],
                            ref_stats_entry=ref_stats["Homoarginine"],
                            subtitle="Субстрат для синтазы оксида азота"
                        ),
                        
                        # Arg
                        render_metabolite_row(
                            concentration=metabolite_data["Arginine"],
                            ref_stats_entry=ref_stats["Arginine"],
                            subtitle="Незаменимая глюкогенная аминокислота"
                        ),
                        
                        # Cit
                        render_metabolite_row(
                            concentration=metabolite_data["Citrulline"],
                            ref_stats_entry=ref_stats["Citrulline"],
                            subtitle="Метаболит цикла мочевины"
                        ),
                        
                        # Orn
                        render_metabolite_row(
                            concentration=metabolite_data["Ornitine"],
                            ref_stats_entry=ref_stats["Ornitine"],
                            subtitle="Метаболит цикла мочевины"
                        ),
                        
                        # Asn
                        render_metabolite_row(
                            concentration=metabolite_data["Asparagine"],
                            ref_stats_entry=ref_stats["Asparagine"],
                            subtitle="Заменимая глюкогенная аминокислота"
                        ),
                        
                        # Asp
                        render_metabolite_row(
                            concentration=metabolite_data["Aspartic acid"],
                            ref_stats_entry=ref_stats["Aspartic acid"],
                            subtitle="Заменимая глюкогенная аминокислота"
                        ),
                        
                        # Cr
                        render_metabolite_row(
                            concentration=metabolite_data["Creatinine"],
                            ref_stats_entry=ref_stats["Creatinine"],
                            subtitle="Продукт метаболизма аргинина"
                        )
                    ])
                    
                ], style={'margin':'0px'}),
            ]),
           render_page_footer(page_number=5),
            # 5 страница
            html.Div([
                
            render_page_header(date=date, name=name), 
                
                html.Div([
                    html.Div([
                        # Metabolism of Carbohydrates
                        render_category_header(order_number='4', title='Метаболизм жирных кислот'),
                        
                        # Acylcarnitine Metabolism (keeping Russian title)
                        render_metabolite_category_header('Метаболизм ацилкарнитинов'),
                        
                        # Alanine
                        render_metabolite_row(
                            concentration=metabolite_data["Alanine"],
                            ref_stats_entry=ref_stats["Alanine"],
                            subtitle="Заменимая глюкогенная аминокислота"
                        ),
                        
                        # Carnitine (C0)
                        render_metabolite_row(
                            concentration=metabolite_data["C0"],
                            ref_stats_entry=ref_stats["C0"],
                            subtitle="Основа для ацилкарнитинов, транспорт жирных кислот"
                        ),
                        
                        # Acetylcarnitine (C2)
                        render_metabolite_row(
                            concentration=metabolite_data["C2"],
                            ref_stats_entry=ref_stats["C2"],
                            subtitle=""
                        ),
                        
                        # Short-chain acylcarnitines (keeping Russian title)
                        render_metabolite_category_header('Короткоцепочечные ацилкарнитины'),
                        
                        # Propionylcarnitine (C3)
                        render_metabolite_row(
                            concentration=metabolite_data["C3"],
                            ref_stats_entry=ref_stats["C3"],
                            subtitle=""
                        ),
                        
                        # Butyrylcarnitine (C4)
                        render_metabolite_row(
                            concentration=metabolite_data["C4"],
                            ref_stats_entry=ref_stats["C4"],
                            subtitle=""
                        ),
                        
                        # Isovalerylcarnitine (C5)
                        render_metabolite_row(
                            concentration=metabolite_data["C5"],
                            ref_stats_entry=ref_stats["C5"],
                            subtitle=""
                        ),
                        
                        # Tiglylcarnitine (C5-1)
                        render_metabolite_row(
                            concentration=metabolite_data["C5-1"],
                            ref_stats_entry=ref_stats["C5-1"],
                            subtitle=""
                        ),
                        
                        # Glutarylcarnitine (C5-DC)
                        render_metabolite_row(
                            concentration=metabolite_data["C5-DC"],
                            ref_stats_entry=ref_stats["C5-DC"],
                            subtitle=""
                        ),
                        
                        # Hydroxyisovalerylcarnitine (C5-OH)
                        render_metabolite_row(
                            concentration=metabolite_data["C5-OH"],
                            ref_stats_entry=ref_stats["C5-OH"],
                            subtitle=""
                        ),
                        
                        # Medium-chain acylcarnitines (keeping Russian title)
                        render_metabolite_category_header('Среднецепочечные ацилкарнитины'),
                        
                        # Hexanoylcarnitine (C6)
                        render_metabolite_row(
                            concentration=metabolite_data["C6"],
                            ref_stats_entry=ref_stats["C6"],
                            subtitle=""
                        ),
                        
                        # Adipoylcarnitine (C6-DC)
                        render_metabolite_row(
                            concentration=metabolite_data["C6-DC"],
                            ref_stats_entry=ref_stats["C6-DC"],
                            subtitle=""
                        ),
                        
                        # Octanoylcarnitine (C8)
                        render_metabolite_row(
                            concentration=metabolite_data["C8"],
                            ref_stats_entry=ref_stats["C8"],
                            subtitle=""
                        ),
                        
                        # Octenoylcarnitine (C8-1)
                        render_metabolite_row(
                            concentration=metabolite_data["C8-1"],
                            ref_stats_entry=ref_stats["C8-1"],
                            subtitle=""
                        ),
                        
                        # Decanoylcarnitine (C10)
                        render_metabolite_row(
                            concentration=metabolite_data["C10"],
                            ref_stats_entry=ref_stats["C10"],
                            subtitle=""
                        ),
                        
                        # Decenoylcarnitine (C10-1)
                        render_metabolite_row(
                            concentration=metabolite_data["C10-1"],
                            ref_stats_entry=ref_stats["C10-1"],
                            subtitle=""
                        ),
                        
                        # Decadienoylcarnitine (C10-2)
                        render_metabolite_row(
                            concentration=metabolite_data["C10-2"],
                            ref_stats_entry=ref_stats["C10-2"],
                            subtitle=""
                        ),
                        
                        # Dodecanoylcarnitine (C12)
                        render_metabolite_row(
                            concentration=metabolite_data["C12"],
                            ref_stats_entry=ref_stats["C12"],
                            subtitle=""
                        ),
                        
                        # Dodecenoylcarnitine (C12-1)
                        render_metabolite_row(
                            concentration=metabolite_data["C12-1"],
                            ref_stats_entry=ref_stats["C12-1"],
                            subtitle=""
                        )
                    ]),
                    
                ], style={'margin':'0px'}),
            ]),
            render_page_footer(page_number=6),
           # 6 страница
            html.Div([
                
render_page_header(date=date, name=name),   
                
                html.Div([
                    # Long-chain acylcarnitines (keeping Russian title)
                    render_metabolite_category_header('Длинноцепочечные ацилкарнитины'),
                    
                    # Tetradecanoylcarnitine (C14)
                    render_metabolite_row(
                        concentration=metabolite_data["C14"],
                        ref_stats_entry=ref_stats["C14"],
                        subtitle=""
                    ),
                    
                    # Tetradecenoylcarnitine (C14:1)
                    render_metabolite_row(
                        concentration=metabolite_data["C14-1"],
                        ref_stats_entry=ref_stats["C14-1"],
                        subtitle=""
                    ),
                    
                    # Tetradecadienoylcarnitine (C14:2)
                    render_metabolite_row(
                        concentration=metabolite_data["C14-2"],
                        ref_stats_entry=ref_stats["C14-2"],
                        subtitle=""
                    ),
                    
                    # Hydroxytetradecanoylcarnitine (C14-OH)
                    render_metabolite_row(
                        concentration=metabolite_data["C14-OH"],
                        ref_stats_entry=ref_stats["C14-OH"],
                        subtitle=""
                    ),
                    
                    # Palmitoylcarnitine (C16)
                    render_metabolite_row(
                        concentration=metabolite_data["C16"],
                        ref_stats_entry=ref_stats["C16"],
                        subtitle=""
                    ),
                    
                    # Hexadecenoylcarnitine (C16:1)
                    render_metabolite_row(
                        concentration=metabolite_data["C16-1"],
                        ref_stats_entry=ref_stats["C16-1"],
                        subtitle=""
                    ),
                    
                    # Hydroxyhexadecenoylcarnitine (C16:1-OH)
                    render_metabolite_row(
                        concentration=metabolite_data["C16-1-OH"],
                        ref_stats_entry=ref_stats["C16-1-OH"],
                        subtitle=""
                    ),
                    
                    # Hydroxyhexadecanoylcarnitine (C16-OH)
                    render_metabolite_row(
                        concentration=metabolite_data["C16-OH"],
                        ref_stats_entry=ref_stats["C16-OH"],
                        subtitle=""
                    ),
                    
                    # Stearoylcarnitine (C18)
                    render_metabolite_row(
                        concentration=metabolite_data["C18"],
                        ref_stats_entry=ref_stats["C18"],
                        subtitle=""
                    ),
                    
                    # Oleoylcarnitine (C18:1)
                    render_metabolite_row(
                        concentration=metabolite_data["C18-1"],
                        ref_stats_entry=ref_stats["C18-1"],
                        subtitle=""
                    ),
                    
                    # Hydroxyoctadecenoylcarnitine (C18:1-OH)
                    render_metabolite_row(
                        concentration=metabolite_data["C18-1-OH"],
                        ref_stats_entry=ref_stats["C18-1-OH"],
                        subtitle=""
                    ),
                    
                    # Linoleoylcarnitine (C18:2)
                    render_metabolite_row(
                        concentration=metabolite_data["C18-2"],
                        ref_stats_entry=ref_stats["C18-2"],
                        subtitle=""
                    ),
                    
                    # Hydroxyoctadecanoylcarnitine (C18-OH)
                    render_metabolite_row(
                        concentration=metabolite_data["C18-OH"],
                        ref_stats_entry=ref_stats["C18-OH"],
                        subtitle=""
                    ),
                    
                    # Metabolic balance section header (keeping Russian title)
                    render_category_header(order_number='4', title='Метаболический баланс'),
                    
                    # Vitamins and neurotransmitters (keeping Russian title)
                    render_metabolite_category_header('Витамины и нейромедиаторы'),
                    
                    # Pantothenic acid
                    render_metabolite_row(
                        concentration=metabolite_data["Pantothenic"],
                        ref_stats_entry=ref_stats["Pantothenic"],
                        subtitle="Витамин B5"
                    ),
                    
                    # Riboflavin
                    render_metabolite_row(
                        concentration=metabolite_data["Riboflavin"],
                        ref_stats_entry=ref_stats["Riboflavin"],
                        subtitle="Витамин B2"
                    ),
                    
                    # Melatonin
                    render_metabolite_row(
                        concentration=metabolite_data["Melatonin"],
                        ref_stats_entry=ref_stats["Melatonin"],
                        subtitle="Регулирует циркадные ритмы"
                    ),
                    
                    # Nucleosides (keeping Russian title)
                    render_metabolite_category_header('Нуклеозиды'),
                    
                    # Uridine
                    render_metabolite_row(
                        concentration=metabolite_data["Uridine"],
                        ref_stats_entry=ref_stats["Uridine"],
                        subtitle=""
                    ),
                    
                    # Adenosine
                    render_metabolite_row(
                        concentration=metabolite_data["Adenosin"],
                        ref_stats_entry=ref_stats["Adenosin"],
                        subtitle=""
                    ),
                    
                    # Cytidine
                    render_metabolite_row(
                        concentration=metabolite_data["Cytidine"],
                        ref_stats_entry=ref_stats["Cytidine"],
                        subtitle=""
                    ),
                    
                    
                    
                ], style={'margin':'0px'}),
            ]),

            # Footer for page 7
            render_page_footer(page_number=7),
            # 7 страница
            html.Div([
                
            render_page_header(date=date, name=name), 
                            
                html.Div([
                    
               # Allergy and stress (keeping Russian title)
                    render_metabolite_category_header('Аллергия и стресс'),
                    
                    # Cortisol
                    render_metabolite_row(
                        concentration=metabolite_data["Cortisol"],
                        ref_stats_entry=ref_stats["Cortisol"],
                        subtitle=""
                    ),
                    
                    # Histamine
                    render_metabolite_row(
                        concentration=metabolite_data["Histamine"],
                        ref_stats_entry=ref_stats["Histamine"],
                        subtitle=""
                    ),
                    
#                 html.Div(
#     style={
#         'width': '100%',
#         'fontFamily': 'Calibri',
#         'padding': '5px'
#     },
#     children=[
#         # Main Card
#         html.Div(
#             style={
#                 'backgroundColor': 'white',
#                 'borderRadius': '5px',
#                 'overflow': 'hidden'
#             },
#             children=[
#                 # Section Header
#                 html.Div([
#                     html.H3(
#                         children='8. Метилирование, обмен холина и метионина', 
#                         style={
#                             'textAlign': 'center',
#                             'margin': '0px',
#                             'lineHeight': 'normal',
#                             'display': 'inline-block',
#                             'verticalAlign': 'center',
#                             'fontWeight': '600',
#                             'fontSize': '19px'
#                         }
#                     )],
#                     style={
#                         'width': '100%',
#                         'backgroundColor': '#2563eb',
#                         'borderRadius': '5px 5px 0px 0px', 
#                         'color': 'white',
#                         'fontFamily': 'Calibri',
#                         'margin': '0px',
#                         'height': '35px',
#                         'lineHeight': '35px',
#                         'textAlign': 'center',
#                         'marginTop': '20px'
#                     }
#                 ),
                
#                 # Table Content
#                 html.Div(
#                     style={'padding': '10px 0px'},
#                     children=[
#                         # Table Headers
#                         html.Div(
#                             style={
#                                 'display': 'grid',
#                                 'gridTemplateColumns': 'repeat(13, minmax(0, 1fr))',
#                                 'gap': '10px',
#                                 'fontWeight': '500',
#                                 'color': "#4D5052",
#                                 'backgroundColor': '#f8f9fa',
#                                 'padding': '8px',
#                                 'borderRadius': '5px',
#                                 'margin': '0px',
#                                 'fontSize': '14px',
#                                 'fontFamily': 'Calibri'
#                             },
#                             children=[
#                                 html.Div("Показатель", style={'gridColumn': 'span 3'}),
#                                 html.Div("Результат", style={'gridColumn': 'span 2', 'textAlign': 'center'}),
#                                 html.Div("Статус", style={'gridColumn': 'span 1', 'textAlign': 'center'}),
#                                 html.Div("Норма", style={'gridColumn': 'span 2', 'textAlign': 'center'}),
#                                 html.Div("Что это отражает?", style={'gridColumn': 'span 5'}),
#                             ]
#                         ),
                        
#                         # Data Rows
#                         *[
#                             html.Div(
#                                 style={
#                                     'display': 'grid',
#                                     'gridTemplateColumns': 'repeat(13, minmax(0, 1fr))',
#                                     'gap': '10px',
#                                     'padding': '8px 10px',
#                                     'alignItems': 'center',
#                                     'borderBottom': '1px solid #e9ecef',
#                                     'fontFamily': 'Calibri'
#                                 },
#                                 children=[
#                                     html.Div(
#                                         item["name"],
#                                         style={
#                                             'gridColumn': 'span 3',
#                                             'fontWeight': '600',
                                            
#                                             'fontSize': '14px',
#                                             'color': '#212529'
#                                         }
#                                     ),
#                                     html.Div(
#                                         style={
#                                             'gridColumn': 'span 2',
#                                             'display': 'flex',
#                                             'alignItems': 'center',
#                                             'justifyContent': 'center',
#                                             'gap': '4px'
#                                         },
#                                         children=[
#                                             html.Div(
#                                                 f"{item['value']}",
#                                                 style={
#                                                     'fontWeight': 'bold',
#                                                     'fontSize': '15px',
#                                                     'color': {
#                                                         'blue': '#2563eb',
#                                                         'red': '#dc3545',
#                                                         'green': '#212529'
#                                                         }[get_status_color(item["value"], item["norm"])]
#                                                 }
#                                             ),
#                                             html.Div(
#                                                 style={
#                                                     'width': '0',
#                                                     'height': '0',
#                                                     'borderLeft': '5px solid transparent',
#                                                     'borderRight': '5px solid transparent',
#                                                     'borderTop': '8px solid #2563eb' if get_status_color(item['value'], item['norm']) == 'blue' else 'none',
#                                                     'borderBottom': '8px solid #dc3545' if get_status_color(item['value'], item['norm']) == 'red' else 'none',
#                                                     'visibility': 'visible' if get_status_color(item['value'], item['norm']) in ['blue', 'red'] else 'collapse',
#                                                     'marginLeft': '4px' if get_status_color(item['value'], item['norm']) in ['red', 'blue'] else '0px'
#                                                 }
#                                             )
#                                         ]
#                                     ),
                                    
#                                     html.Div(
#                                         style={
#                                             'gridColumn': 'span 1',
#                                             'textAlign': 'center',
#                                             'justifySelf': 'center',
#                                         },
#                                         children=html.Span(
#                                             get_status_text(item["value"], item["norm"]),
#                                             style={
#                                                 'padding': '3px 8px',
#                                                 'borderRadius': '12px',
#                                                 'fontSize': '14px',
#                                                 'fontWeight': '500',
#                                                 'backgroundColor': {
#                                                     'blue': '#e7f1ff',
#                                                     'red': '#f8d7da',
#                                                     'green': '#e6f7ee'
#                                                 }[get_status_color(item["value"], item["norm"])],
#                                                 'color': {
#                                                     'blue': '#2563eb',
#                                                     'red': '#dc3545',
#                                                     'green': '#198754'
#                                                 }[get_status_color(item["value"], item["norm"])]
#                                             }
#                                         )
#                                     ),
#                                     html.Div(
#                                         f"{item['norm']}",
#                                         style={
#                                             'gridColumn': 'span 2',
#                                             'textAlign': 'center',
                                            
#                                             'fontSize': '14px',
#                                             'color': '#6c757d',
#                                             'alignItems': 'center'
#                                         }
#                                     ),
#                                     html.Div(
#                                         item["description"],
#                                         style={
#                                             'gridColumn': 'span 5',
#                                             'color': '#6c757d',
#                                             'lineHeight': '1.4',
#                                             'fontSize': '14px'
#                                         }
#                                     ),
#                                 ]
#                             )
#                             for item in methylation_data
#                         ],
#                     ]
#                 ),
                
                
#             ]
#         )
#     ]
# ),      
                
                        
         
#                        render_page_footer(page_number=8),
           
#    render_page_header(date=date, name=name),

           
#            html.Div(
#     style={
#         'width': '100%',
#         'fontFamily': 'Calibri',
#         'padding': '5px'
#     },
#     children=[
#         # Main Card
#         html.Div(
#             style={
#                 'backgroundColor': 'white',
#                 'borderRadius': '5px',
#                 'overflow': 'hidden'
#             },
#             children=[
#                 # Section Header
#                 html.Div([
#                     html.H3(
#                         children='7. Воспаление, стресс и нейромедиаторный баланс', 
#                         style={
#                             'textAlign': 'center',
#                             'margin': '0px',
#                             'lineHeight': 'normal',
#                             'display': 'inline-block',
#                             'verticalAlign': 'center',
#                             'fontWeight': '600',
#                             'fontSize': '19px'
#                         }
#                     )],
#                     style={
#                         'width': '100%',
#                         'backgroundColor': '#2563eb',
#                         'borderRadius': '5px 5px 0px 0px', 
#                         'color': 'white',
#                         'fontFamily': 'Calibri',
#                         'margin': '0px',
#                         'height': '35px',
#                         'lineHeight': '35px',
#                         'textAlign': 'center',
#                         'marginTop': '0px'
#                     }
#                 ),
                
#                 # Table Content
#                 html.Div(
#                     style={'padding': '10px 0px'},
#                     children=[
#                         # Table Headers
#                         html.Div(
#                             style={
#                                 'display': 'grid',
#                                 'gridTemplateColumns': 'repeat(13, minmax(0, 1fr))',
#                                 'gap': '10px',
#                                 'fontWeight': '500',
#                                 'color': "#4D5052",
#                                 'backgroundColor': '#f8f9fa',
#                                 'padding': '8px',
#                                 'borderRadius': '5px',
#                                 'margin': '0px',
#                                 'fontSize': '14px',
#                                 'fontFamily': 'Calibri'
#                             },
#                             children=[
#                                 html.Div("Показатель", style={'gridColumn': 'span 3'}),
#                                 html.Div("Результат", style={'gridColumn': 'span 2', 'textAlign': 'center'}),
#                                 html.Div("Статус", style={'gridColumn': 'span 1', 'textAlign': 'center'}),
#                                 html.Div("Норма", style={'gridColumn': 'span 2', 'textAlign': 'center'}),
#                                 html.Div("Что это отражает?", style={'gridColumn': 'span 5'}),
#                             ]
#                         ),
                        
#                         # Data Rows
#                         *[
#                             html.Div(
#                                 style={
#                                     'display': 'grid',
#                                     'gridTemplateColumns': 'repeat(13, minmax(0, 1fr))',
#                                     'gap': '10px',
#                                     'padding': '8px 10px',
#                                     'alignItems': 'center',
#                                     'borderBottom': '1px solid #e9ecef',
#                                     'fontFamily': 'Calibri'
#                                 },
#                                 children=[
#                                     html.Div(
#                                         item["name"],
#                                         style={
#                                             'gridColumn': 'span 3',
#                                             'fontWeight': '600',
                                            
#                                             'fontSize': '14px',
#                                             'color': '#212529'
#                                         }
#                                     ),
#                                     html.Div(
#                                         style={
#                                             'gridColumn': 'span 2',
#                                             'display': 'flex',
#                                             'alignItems': 'center',
#                                             'justifyContent': 'center',
#                                             'gap': '4px'
#                                         },
#                                         children=[
#                                             html.Div(
#                                                 f"{item['value']}",
#                                                 style={
#                                                     'fontWeight': 'bold',
#                                                     'fontSize': '15px',
#                                                     'color': {
#                                                         'blue': '#2563eb',
#                                                         'red': '#dc3545',
#                                                         'green': '#212529'
#                                                         }[get_status_color(item["value"], item["norm"])]
#                                                 }
#                                             ),
#                                             html.Div(
#                                                 style={
#                                                     'width': '0',
#                                                     'height': '0',
#                                                     'borderLeft': '5px solid transparent',
#                                                     'borderRight': '5px solid transparent',
#                                                     'borderTop': '8px solid #2563eb' if get_status_color(item['value'], item['norm']) == 'blue' else 'none',
#                                                     'borderBottom': '8px solid #dc3545' if get_status_color(item['value'], item['norm']) == 'red' else 'none',
#                                                     'visibility': 'visible' if get_status_color(item['value'], item['norm']) in ['blue', 'red'] else 'collapse',
#                                                     'marginLeft': '4px' if get_status_color(item['value'], item['norm']) in ['red', 'blue'] else '0px'
#                                                 }
#                                             )
#                                         ]
#                                     ),
                                    
#                                     html.Div(
#                                         style={
#                                             'gridColumn': 'span 1',
#                                             'textAlign': 'center',
#                                             'justifySelf': 'center',
#                                         },
#                                         children=html.Span(
#                                             get_status_text(item["value"], item["norm"]),
#                                             style={
#                                                 'padding': '3px 8px',
#                                                 'borderRadius': '12px',
#                                                 'fontSize': '14px',
#                                                 'fontWeight': '500',
#                                                 'backgroundColor': {
#                                                     'blue': '#e7f1ff',
#                                                     'red': '#f8d7da',
#                                                     'green': '#e6f7ee'
#                                                 }[get_status_color(item["value"], item["norm"])],
#                                                 'color': {
#                                                     'blue': '#2563eb',
#                                                     'red': '#dc3545',
#                                                     'green': '#198754'
#                                                 }[get_status_color(item["value"], item["norm"])]
#                                             }
#                                         )
#                                     ),
#                                     html.Div(
#                                         f"{item['norm']}",
#                                         style={
#                                             'gridColumn': 'span 2',
#                                             'textAlign': 'center',
                                            
#                                             'fontSize': '14px',
#                                             'color': '#6c757d',
#                                             'alignItems': 'center'
#                                         }
#                                     ),
#                                     html.Div(
#                                         item["description"],
#                                         style={
#                                             'gridColumn': 'span 5',
#                                             'color': '#6c757d',
#                                             'lineHeight': '1.4',
#                                             'fontSize': '14px'
#                                         }
#                                     ),
#                                 ]
#                             )
#                             for item in inflammation_data
#                         ],
#                     ]
#                 ),
                
                
#             ]
#         )
#     ]
# ),
           
#                     render_page_footer(page_number=9),
#                 render_page_header(date=date, name=name),

#         html.Div(
#     style={
#         'width': '100%',
#         'fontFamily': 'Calibri',
#         'padding': '5px'
#     },
#     children=[
#         # Main Card
#         html.Div(
#             style={
#                 'backgroundColor': 'white',
#                 'borderRadius': '5px',
#                 'overflow': 'hidden'
#             },
#             children=[
#                 # Section Header
#                 html.Div([
#                     html.H3(
#                         children='6. Состояние сосудистой системы и эндотелиальной функции', 
#                         style={
#                             'textAlign': 'center',
#                             'margin': '0px',
#                             'lineHeight': 'normal',
#                             'display': 'inline-block',
#                             'verticalAlign': 'center',
#                             'fontWeight': '600',
#                             'fontSize': '19px'
#                         }
#                     )],
#                     style={
#                         'width': '100%',
#                         'backgroundColor': '#2563eb',
#                         'borderRadius': '5px 5px 0px 0px', 
#                         'color': 'white',
#                         'fontFamily': 'Calibri',
#                         'margin': '0px',
#                         'height': '35px',
#                         'lineHeight': '35px',
#                         'textAlign': 'center',
#                         'marginTop': '0px'
#                     }
#                 ),
                
#                 # Table Content
#                 html.Div(
#                     style={'padding': '10px 0px'},
#                     children=[
#                         # Table Headers
#                         html.Div(
#                             style={
#                                 'display': 'grid',
#                                 'gridTemplateColumns': 'repeat(13, minmax(0, 1fr))',
#                                 'gap': '10px',
#                                 'fontWeight': '500',
#                                 'color': "#4D5052",
#                                 'backgroundColor': '#f8f9fa',
#                                 'padding': '8px',
#                                 'borderRadius': '5px',
#                                 'margin': '0px',
#                                 'fontSize': '14px',
#                                 'fontFamily': 'Calibri'
#                             },
#                             children=[
#                                 html.Div("Показатель", style={'gridColumn': 'span 3'}),
#                                 html.Div("Результат", style={'gridColumn': 'span 2', 'textAlign': 'center'}),
#                                 html.Div("Статус", style={'gridColumn': 'span 1', 'textAlign': 'center'}),
#                                 html.Div("Норма", style={'gridColumn': 'span 2', 'textAlign': 'center'}),
#                                 html.Div("Что это отражает?", style={'gridColumn': 'span 5'}),
#                             ]
#                         ),
                        
#                         # Data Rows
#                         *[
#                             html.Div(
#                                 style={
#                                     'display': 'grid',
#                                     'gridTemplateColumns': 'repeat(13, minmax(0, 1fr))',
#                                     'gap': '10px',
#                                     'padding': '8px 10px',
#                                     'alignItems': 'center',
#                                     'borderBottom': '1px solid #e9ecef',
#                                     'fontFamily': 'Calibri'
#                                 },
#                                 children=[
#                                     html.Div(
#                                         item["name"],
#                                         style={
#                                             'gridColumn': 'span 3',
#                                             'fontWeight': '600',
                                            
#                                             'fontSize': '14px',
#                                             'color': '#212529'
#                                         }
#                                     ),
#                                     html.Div(
#                                         style={
#                                             'gridColumn': 'span 2',
#                                             'display': 'flex',
#                                             'alignItems': 'center',
#                                             'justifyContent': 'center',
#                                             'gap': '4px'
#                                         },
#                                         children=[
#                                             html.Div(
#                                                 f"{item['value']}",
#                                                 style={
#                                                     'fontWeight': 'bold',
#                                                     'fontSize': '15px',
#                                                     'color': {
#                                                         'blue': '#2563eb',
#                                                         'red': '#dc3545',
#                                                         'green': '#212529'
#                                                         }[get_status_color(item["value"], item["norm"])]
#                                                 }
#                                             ),
#                                             html.Div(
#                                                 style={
#                                                     'width': '0',
#                                                     'height': '0',
#                                                     'borderLeft': '5px solid transparent',
#                                                     'borderRight': '5px solid transparent',
#                                                     'borderTop': '8px solid #2563eb' if get_status_color(item['value'], item['norm']) == 'blue' else 'none',
#                                                     'borderBottom': '8px solid #dc3545' if get_status_color(item['value'], item['norm']) == 'red' else 'none',
#                                                     'visibility': 'visible' if get_status_color(item['value'], item['norm']) in ['blue', 'red'] else 'collapse',
#                                                     'marginLeft': '4px' if get_status_color(item['value'], item['norm']) in ['red', 'blue'] else '0px'
#                                                 }
#                                             )
#                                         ]
#                                     ),
                                    
#                                     html.Div(
#                                         style={
#                                             'gridColumn': 'span 1',
#                                             'textAlign': 'center',
#                                             'justifySelf': 'center',
#                                         },
#                                         children=html.Span(
#                                             get_status_text(item["value"], item["norm"]),
#                                             style={
#                                                 'padding': '3px 8px',
#                                                 'borderRadius': '12px',
#                                                 'fontSize': '14px',
#                                                 'fontWeight': '500',
#                                                 'backgroundColor': {
#                                                     'blue': '#e7f1ff',
#                                                     'red': '#f8d7da',
#                                                     'green': '#e6f7ee'
#                                                 }[get_status_color(item["value"], item["norm"])],
#                                                 'color': {
#                                                     'blue': '#2563eb',
#                                                     'red': '#dc3545',
#                                                     'green': '#198754'
#                                                 }[get_status_color(item["value"], item["norm"])]
#                                             }
#                                         )
#                                     ),
#                                     html.Div(
#                                         f"{item['norm']}",
#                                         style={
#                                             'gridColumn': 'span 2',
#                                             'textAlign': 'center',
                                            
#                                             'fontSize': '14px',
#                                             'color': '#6c757d',
#                                             'alignItems': 'center'
#                                         }
#                                     ),
#                                     html.Div(
#                                         item["description"],
#                                         style={
#                                             'gridColumn': 'span 5',
#                                             'color': '#6c757d',
#                                             'lineHeight': '1.4',
#                                             'fontSize': '14px'
#                                         }
#                                     ),
#                                 ]
#                             )
#                             for item in vascular_data
#                         ],
#                     ]
#                 ),
                
                
#             ]
#         )
#     ]
# ),  
#                            render_page_footer(page_number=10),
#     render_page_header(date=date, name=name),

    
#     html.Div(
#     style={
#         'width': '100%',
#         'fontFamily': 'Calibri',
#         'padding': '5px'
#     },
#     children=[
#         # Main Card
#         html.Div(
#             style={
#                 'backgroundColor': 'white',
#                 'borderRadius': '5px',
#                 'overflow': 'hidden'
#             },
#             children=[
#                 # Section Header
#                 html.Div([
#                     html.H3(
#                         children='9. Энергетический обмен, цикл Кребса и баланс аминокислот', 
#                         style={
#                             'textAlign': 'center',
#                             'margin': '0px',
#                             'lineHeight': 'normal',
#                             'display': 'inline-block',
#                             'verticalAlign': 'center',
#                             'fontWeight': '600',
#                             'fontSize': '19px'
#                         }
#                     )],
#                     style={
#                         'width': '100%',
#                         'backgroundColor': '#2563eb',
#                         'borderRadius': '5px 5px 0px 0px', 
#                         'color': 'white',
#                         'fontFamily': 'Calibri',
#                         'margin': '0px',
#                         'height': '35px',
#                         'lineHeight': '35px',
#                         'textAlign': 'center',
#                         'marginTop': '0px'
#                     }
#                 ),
                
#                 # Table Content
#                 html.Div(
#                     style={'padding': '10px 0px'},
#                     children=[
#                         # Table Headers
#                         html.Div(
#                             style={
#                                 'display': 'grid',
#                                 'gridTemplateColumns': 'repeat(13, minmax(0, 1fr))',
#                                 'gap': '10px',
#                                 'fontWeight': '500',
#                                 'color': "#4D5052",
#                                 'backgroundColor': '#f8f9fa',
#                                 'padding': '8px',
#                                 'borderRadius': '5px',
#                                 'margin': '0px',
#                                 'fontSize': '14px',
#                                 'fontFamily': 'Calibri'
#                             },
#                             children=[
#                                 html.Div("Показатель", style={'gridColumn': 'span 3'}),
#                                 html.Div("Результат", style={'gridColumn': 'span 2', 'textAlign': 'center'}),
#                                 html.Div("Статус", style={'gridColumn': 'span 1', 'textAlign': 'center'}),
#                                 html.Div("Норма", style={'gridColumn': 'span 2', 'textAlign': 'center'}),
#                                 html.Div("Что это отражает?", style={'gridColumn': 'span 5'}),
#                             ]
#                         ),
                        
#                         # Data Rows
#                         *[
#                             html.Div(
#                                 style={
#                                     'display': 'grid',
#                                     'gridTemplateColumns': 'repeat(13, minmax(0, 1fr))',
#                                     'gap': '10px',
#                                     'padding': '8px 10px',
#                                     'alignItems': 'center',
#                                     'borderBottom': '1px solid #e9ecef',
#                                     'fontFamily': 'Calibri'
#                                 },
#                                 children=[
#                                     html.Div(
#                                         item["name"],
#                                         style={
#                                             'gridColumn': 'span 3',
#                                             'fontWeight': '600',
                                            
#                                             'fontSize': '14px',
#                                             'color': '#212529'
#                                         }
#                                     ),
#                                     html.Div(
#                                         style={
#                                             'gridColumn': 'span 2',
#                                             'display': 'flex',
#                                             'alignItems': 'center',
#                                             'justifyContent': 'center',
#                                             'gap': '4px'
#                                         },
#                                         children=[
#                                             html.Div(
#                                                 f"{item['value']}",
#                                                 style={
#                                                     'fontWeight': 'bold',
#                                                     'fontSize': '15px',
#                                                     'color': {
#                                                         'blue': '#2563eb',
#                                                         'red': '#dc3545',
#                                                         'green': '#212529'
#                                                         }[get_status_color(item["value"], item["norm"])]
#                                                 }
#                                             ),
#                                             html.Div(
#                                                 style={
#                                                     'width': '0',
#                                                     'height': '0',
#                                                     'borderLeft': '5px solid transparent',
#                                                     'borderRight': '5px solid transparent',
#                                                     'borderTop': '8px solid #2563eb' if get_status_color(item['value'], item['norm']) == 'blue' else 'none',
#                                                     'borderBottom': '8px solid #dc3545' if get_status_color(item['value'], item['norm']) == 'red' else 'none',
#                                                     'visibility': 'visible' if get_status_color(item['value'], item['norm']) in ['blue', 'red'] else 'collapse',
#                                                     'marginLeft': '4px' if get_status_color(item['value'], item['norm']) in ['red', 'blue'] else '0px'
#                                                 }
#                                             )
#                                         ]
#                                     ),
                                    
#                                     html.Div(
#                                         style={
#                                             'gridColumn': 'span 1',
#                                             'textAlign': 'center',
#                                             'justifySelf': 'center',
#                                         },
#                                         children=html.Span(
#                                             get_status_text(item["value"], item["norm"]),
#                                             style={
#                                                 'padding': '3px 8px',
#                                                 'borderRadius': '12px',
#                                                 'fontSize': '14px',
#                                                 'fontWeight': '500',
#                                                 'backgroundColor': {
#                                                     'blue': '#e7f1ff',
#                                                     'red': '#f8d7da',
#                                                     'green': '#e6f7ee'
#                                                 }[get_status_color(item["value"], item["norm"])],
#                                                 'color': {
#                                                     'blue': '#2563eb',
#                                                     'red': '#dc3545',
#                                                     'green': '#198754'
#                                                 }[get_status_color(item["value"], item["norm"])]
#                                             }
#                                         )
#                                     ),
#                                     html.Div(
#                                         f"{item['norm']}",
#                                         style={
#                                             'gridColumn': 'span 2',
#                                             'textAlign': 'center',
                                            
#                                             'fontSize': '14px',
#                                             'color': '#6c757d',
#                                             'alignItems': 'center'
#                                         }
#                                     ),
#                                     html.Div(
#                                         item["description"],
#                                         style={
#                                             'gridColumn': 'span 5',
#                                             'color': '#6c757d',
#                                             'lineHeight': '1.4',
#                                             'fontSize': '14px'
#                                         }
#                                     ),
#                                 ]
#                             )
#                             for item in energy_metabolism_data
#                         ],
#                     ]
#                 ),
                
                
#             ]
#         )
#     ]
# ),
                                 
#                     render_page_footer(page_number=11),
    
#     render_page_header(date=date, name=name),

                                 
# html.Div(
#     style={
#         'width': '100%',
#         'fontFamily': 'Calibri',
#         'padding': '5px'
#     },
#     children=[
#         # Main Card
#         html.Div(
#             style={
#                 'backgroundColor': 'white',
#                 'borderRadius': '5px',
#                 'overflow': 'hidden'
#             },
#             children=[
#                 # Section Header
#                 html.Div([
#                     html.H3(
#                         children='10. Здоровье митохондрий и β-окисление жирных кислот', 
#                         style={
#                             'textAlign': 'center',
#                             'margin': '0px',
#                             'lineHeight': 'normal',
#                             'display': 'inline-block',
#                             'verticalAlign': 'center',
#                             'fontWeight': '600',
#                             'fontSize': '19px'
#                         }
#                     )],
#                     style={
#                         'width': '100%',
#                         'backgroundColor': '#2563eb',
#                         'borderRadius': '5px 5px 0px 0px', 
#                         'color': 'white',
#                         'fontFamily': 'Calibri',
#                         'margin': '0px',
#                         'height': '35px',
#                         'lineHeight': '35px',
#                         'textAlign': 'center',
#                         'marginTop': '0px'
#                     }
#                 ),
                
#                 # Table Content
#                 html.Div(
#                     style={'padding': '10px 0px'},
#                     children=[
#                         # Table Headers
#                         html.Div(
#                             style={
#                                 'display': 'grid',
#                                 'gridTemplateColumns': 'repeat(13, minmax(0, 1fr))',
#                                 'gap': '10px',
#                                 'fontWeight': '500',
#                                 'color': "#4D5052",
#                                 'backgroundColor': '#f8f9fa',
#                                 'padding': '8px',
#                                 'borderRadius': '5px',
#                                 'margin': '0px',
#                                 'fontSize': '14px',
#                                 'fontFamily': 'Calibri'
#                             },
#                             children=[
#                                 html.Div("Показатель", style={'gridColumn': 'span 3'}),
#                                 html.Div("Результат", style={'gridColumn': 'span 2', 'textAlign': 'center'}),
#                                 html.Div("Статус", style={'gridColumn': 'span 1', 'textAlign': 'center'}),
#                                 html.Div("Норма", style={'gridColumn': 'span 2', 'textAlign': 'center'}),
#                                 html.Div("Что это отражает?", style={'gridColumn': 'span 5'}),
#                             ]
#                         ),
                        
#                         # Data Rows
#                         *[
#                             html.Div(
#                                 style={
#                                     'display': 'grid',
#                                     'gridTemplateColumns': 'repeat(13, minmax(0, 1fr))',
#                                     'gap': '10px',
#                                     'padding': '8px 10px',
#                                     'alignItems': 'center',
#                                     'borderBottom': '1px solid #e9ecef',
#                                     'fontFamily': 'Calibri'
#                                 },
#                                 children=[
#                                     html.Div(
#                                         item["name"],
#                                         style={
#                                             'gridColumn': 'span 3',
#                                             'fontWeight': '600',
                                            
#                                             'fontSize': '14px',
#                                             'color': '#212529'
#                                         }
#                                     ),
#                                     html.Div(
#                                         style={
#                                             'gridColumn': 'span 2',
#                                             'display': 'flex',
#                                             'alignItems': 'center',
#                                             'justifyContent': 'center',
#                                             'gap': '4px'
#                                         },
#                                         children=[
#                                             html.Div(
#                                                 f"{item['value']}",
#                                                 style={
#                                                     'fontWeight': 'bold',
#                                                     'fontSize': '15px',
#                                                     'color': {
#                                                         'blue': '#2563eb',
#                                                         'red': '#dc3545',
#                                                         'green': '#212529'
#                                                         }[get_status_color(item["value"], item["norm"])]
#                                                 }
#                                             ),
#                                             html.Div(
#                                                 style={
#                                                     'width': '0',
#                                                     'height': '0',
#                                                     'borderLeft': '5px solid transparent',
#                                                     'borderRight': '5px solid transparent',
#                                                     'borderTop': '8px solid #2563eb' if get_status_color(item['value'], item['norm']) == 'blue' else 'none',
#                                                     'borderBottom': '8px solid #dc3545' if get_status_color(item['value'], item['norm']) == 'red' else 'none',
#                                                     'visibility': 'visible' if get_status_color(item['value'], item['norm']) in ['blue', 'red'] else 'collapse',
#                                                     'marginLeft': '4px' if get_status_color(item['value'], item['norm']) in ['red', 'blue'] else '0px'
#                                                 }
#                                             )
#                                         ]
#                                     ),
                                    
#                                     html.Div(
#                                         style={
#                                             'gridColumn': 'span 1',
#                                             'textAlign': 'center',
#                                             'justifySelf': 'center',
#                                         },
#                                         children=html.Span(
#                                             get_status_text(item["value"], item["norm"]),
#                                             style={
#                                                 'padding': '3px 8px',
#                                                 'borderRadius': '12px',
#                                                 'fontSize': '14px',
#                                                 'fontWeight': '500',
#                                                 'backgroundColor': {
#                                                     'blue': '#e7f1ff',
#                                                     'red': '#f8d7da',
#                                                     'green': '#e6f7ee'
#                                                 }[get_status_color(item["value"], item["norm"])],
#                                                 'color': {
#                                                     'blue': '#2563eb',
#                                                     'red': '#dc3545',
#                                                     'green': '#198754'
#                                                 }[get_status_color(item["value"], item["norm"])]
#                                             }
#                                         )
#                                     ),
#                                     html.Div(
#                                         f"{item['norm']}",
#                                         style={
#                                             'gridColumn': 'span 2',
#                                             'textAlign': 'center',
                                            
#                                             'fontSize': '14px',
#                                             'color': '#6c757d',
#                                             'alignItems': 'center'
#                                         }
#                                     ),
#                                     html.Div(
#                                         item["description"],
#                                         style={
#                                             'gridColumn': 'span 5',
#                                             'color': '#6c757d',
#                                             'lineHeight': '1.4',
#                                             'fontSize': '14px'
#                                         }
#                                     ),
#                                 ]
#                             )
#                             for item in mitochondrial_data
#                         ],
#                     ]
#                 ),
                
                
#             ]
#         )
#     ]
# ),
#                        render_page_footer(page_number=12),
                
    
#     render_page_header(date=date, name=name),
   
                                            
#                 # Table Content
#                 html.Div(
#                     style={'padding': '10px 0px'},
#                     children=[
#                         # Table Headers
#                         html.Div(
#                             style={
#                                 'display': 'grid',
#                                 'gridTemplateColumns': 'repeat(13, minmax(0, 1fr))',
#                                 'gap': '10px',
#                                 'fontWeight': '500',
#                                 'color': "#4D5052",
#                                 'backgroundColor': '#f8f9fa',
#                                 'padding': '8px',
#                                 'borderRadius': '5px',
#                                 'margin': '0px',
#                                 'fontSize': '14px',
#                                 'fontFamily': 'Calibri'
#                             },
#                             children=[
#                                 html.Div("Показатель", style={'gridColumn': 'span 3'}),
#                                 html.Div("Результат", style={'gridColumn': 'span 2', 'textAlign': 'center'}),
#                                 html.Div("Статус", style={'gridColumn': 'span 1', 'textAlign': 'center'}),
#                                 html.Div("Норма", style={'gridColumn': 'span 2', 'textAlign': 'center'}),
#                                 html.Div("Что это отражает?", style={'gridColumn': 'span 5'}),
#                             ]
#                         ),
                        
#                         # Data Rows
#                         *[
#                             html.Div(
#                                 style={
#                                     'display': 'grid',
#                                     'gridTemplateColumns': 'repeat(13, minmax(0, 1fr))',
#                                     'gap': '10px',
#                                     'padding': '8px 10px',
#                                     'alignItems': 'center',
#                                     'borderBottom': '1px solid #e9ecef',
#                                     'fontFamily': 'Calibri'
#                                 },
#                                 children=[
#                                     html.Div(
#                                         item["name"],
#                                         style={
#                                             'gridColumn': 'span 3',
#                                             'fontWeight': '600',
                                            
#                                             'fontSize': '14px',
#                                             'color': '#212529'
#                                         }
#                                     ),
#                                     html.Div(
#                                         style={
#                                             'gridColumn': 'span 2',
#                                             'display': 'flex',
#                                             'alignItems': 'center',
#                                             'justifyContent': 'center',
#                                             'gap': '4px'
#                                         },
#                                         children=[
#                                             html.Div(
#                                                 f"{item['value']}",
#                                                 style={
#                                                     'fontWeight': 'bold',
#                                                     'fontSize': '15px',
#                                                     'color': {
#                                                         'blue': '#2563eb',
#                                                         'red': '#dc3545',
#                                                         'green': '#212529'
#                                                         }[get_status_color(item["value"], item["norm"])]
#                                                 }
#                                             ),
#                                             html.Div(
#                                                 style={
#                                                     'width': '0',
#                                                     'height': '0',
#                                                     'borderLeft': '5px solid transparent',
#                                                     'borderRight': '5px solid transparent',
#                                                     'borderTop': '8px solid #2563eb' if get_status_color(item['value'], item['norm']) == 'blue' else 'none',
#                                                     'borderBottom': '8px solid #dc3545' if get_status_color(item['value'], item['norm']) == 'red' else 'none',
#                                                     'visibility': 'visible' if get_status_color(item['value'], item['norm']) in ['blue', 'red'] else 'collapse',
#                                                     'marginLeft': '4px' if get_status_color(item['value'], item['norm']) in ['red', 'blue'] else '0px'
#                                                 }
#                                             )
#                                         ]
#                                     ),
                                    
#                                     html.Div(
#                                         style={
#                                             'gridColumn': 'span 1',
#                                             'textAlign': 'center',
#                                             'justifySelf': 'center',
#                                         },
#                                         children=html.Span(
#                                             get_status_text(item["value"], item["norm"]),
#                                             style={
#                                                 'padding': '3px 8px',
#                                                 'borderRadius': '12px',
#                                                 'fontSize': '14px',
#                                                 'fontWeight': '500',
#                                                 'backgroundColor': {
#                                                     'blue': '#e7f1ff',
#                                                     'red': '#f8d7da',
#                                                     'green': '#e6f7ee'
#                                                 }[get_status_color(item["value"], item["norm"])],
#                                                 'color': {
#                                                     'blue': '#2563eb',
#                                                     'red': '#dc3545',
#                                                     'green': '#198754'
#                                                 }[get_status_color(item["value"], item["norm"])]
#                                             }
#                                         )
#                                     ),
#                                     html.Div(
#                                         f"{item['norm']}",
#                                         style={
#                                             'gridColumn': 'span 2',
#                                             'textAlign': 'center',
                                            
#                                             'fontSize': '14px',
#                                             'color': '#6c757d',
#                                             'alignItems': 'center'
#                                         }
#                                     ),
#                                     html.Div(
#                                         item["description"],
#                                         style={
#                                             'gridColumn': 'span 5',
#                                             'color': '#6c757d',
#                                             'lineHeight': '1.4',
#                                             'fontSize': '14px'
#                                         }
#                                     ),
#                                 ]
#                             )
#                             for item in mytochondrial_data_2
#                         ],
#                     ]
#                 ),
                                                       
                    
                    render_page_footer(page_number=13),


                # Header section

                
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
                    style={'color':'#3d1502','font-family':'Calibri','font-size':'13px','text-align':"left", 'margin': '0px !important'}),
            ], style={'display': 'flex','margin-top':'10px','margin-bottom':'10px', 'flex-direction': 'row','align-items': 'center', 'width':'fit-content', "borderRadius": "0.5rem", 'padding': '5px 7px 5px 15px', 'background-color': '#fee4cf'}),
 
            
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
                    
              render_page_footer(page_number=14),

                # Header section
render_page_header(date=date, name=name),
                
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
                    style={'color':'#3d1502','font-family':'Calibri','font-size':'13px','text-align':"left", 'margin': '0px !important'}),
            ], style={'display': 'flex','margin-top':'10px','margin-bottom':'10px', 'flex-direction': 'row','align-items': 'center', 'width':'fit-content', "borderRadius": "0.5rem", 'padding': '5px 7px 5px 15px', 'background-color': '#fee4cf'}),
 
            
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
                       render_page_footer(page_number=15),
                
                # Header section
render_page_header(date=date, name=name),
                
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