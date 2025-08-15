import pandas as pd

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os
import base64
from io import BytesIO

# Get the directory where your script is located
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def smart_round(value, default_decimals=0, ref_stats_entry=None):
    """
    Rounds a number considering significant digits, accounting for the norm format in ref_stats_entry
    
    :param value: input value (number or string)
    :param default_decimals: default decimal places
    :param ref_stats_entry: dictionary with 'norm' field in format "0.01 - 0.05" or "< 0.04"
    :return: rounded value
    """
    try:
        num = float(value)
    except (ValueError, TypeError):
        return 0.0

    if num == 0:
        return 0.0

    decimals = default_decimals

    if ref_stats_entry and isinstance(ref_stats_entry, dict) and 'norm' in ref_stats_entry:
        norm_str = ref_stats_entry['norm']
        
        # Parse norm string into min and max values
        min_val = max_val = None
        if ' - ' in norm_str:
            parts = norm_str.split(' - ', 1)
            try:
                min_val, max_val = float(parts[0].strip()), float(parts[1].strip())
            except ValueError:
                pass
        elif norm_str.startswith(('<', '>')):
            try:
                val = float(norm_str[1:].strip())
                if norm_str.startswith('<'):
                    min_val, max_val = 0.0, val
                else:
                    min_val, max_val = val, None
            except ValueError:
                pass

        # Count decimal places in a number
        def count_decimals(x):
            if x is None:
                return 0
            s = f"{x:.5f}".rstrip('0').rstrip('.')
            return len(s.split('.')[1]) if '.' in s else 0

        decimals = max(
            count_decimals(min_val),
            count_decimals(max_val),
            default_decimals
        )

    # First rounding attempt
    rounded = round(num, decimals)

    # If non-zero, return it
    if rounded != 0:
        return rounded

    # Find first non-zero digit if rounded to zero
    abs_num = abs(num)
    precision = decimals
    while precision <= 10:
        if round(abs_num, precision) != 0:
            return round(num, precision)
        precision += 1

    return round(num, 10)

def create_ref_stats_from_excel(excel_path):
    # Read Excel with explicit handling of decimal commas
    df = pd.read_excel(excel_path)

    # Transpose to metabolites-as-rows format
    df = df.set_index('metabolite').T.reset_index()
    df.columns.name = None

    ref_stats = {}

    def format_number(value):
        """Format number to remove .0 for integers"""
        try:
            num = float(value)
            if num.is_integer():
                return int(num)
            return num
        except (ValueError, TypeError):
            return value

    for _, row in df.iterrows():
        try:
            metabolite = row['index']
            data = {
                'mean': float(str(row['mean']).replace(',', '.')),
                'sd': float(str(row['sd']).replace(',', '.')),
                'ref_min': (
                    float(str(row['ref_min']).replace(',', '.'))
                    if pd.notna(row['ref_min'])
                    else None
                ),
                'ref_max': (
                    float(str(row['ref_max']).replace(',', '.'))
                    if pd.notna(row['ref_max'])
                    else None
                ),
                'name_view': row['name_view'],
                'name_short_view': row['name_short_view']
            }

            # Generate norm string with clean formatting
            if data['ref_min'] is not None and data['ref_max'] is not None:
                min_val = format_number(data['ref_min'])
                max_val = format_number(data['ref_max'])
                
                if min_val == 0:
                    data['norm'] = f"< {max_val}"
                else:
                    data['norm'] = f"{min_val} - {max_val}"

            ref_stats[metabolite] = {k: v for k, v in data.items() if v is not None}

        except Exception as e:
            print(f"Error processing {row.get('index', 'unknown')}: {str(e)}")
            continue
    return ref_stats

def plot_metabolite_z_scores(metabolite_concentrations, group_title, norm_ref=[-1.54, 1.54], ref_stats={}):
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
        display_name = ref_data.get("name_short_view", original_name)
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
            if abs(z_score) > 1.96:  # Significant deviation
                color = "#dc2626"  # red
            elif 1.54 <= abs(z_score) <= 1.96:  # Moderate deviation
                color = "#feb61d"  # orange
            else:  # Normal range
                color = "#10b981"  # green

            data.append(
                {
                    "original_name": original_name,
                    "display_name": display_name,
                    "value": z_score,
                    "color": color,
                    "original_value": conc,
                }
            )

        except (TypeError, ValueError):
            missing_metabolites.append(original_name)

    # Create figure - show empty plot if no valid data
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
    if not data:
        ax.text(
            0.5,
            0.5,
            "No valid reference data available\nfor these metabolites",
            ha='center',
            va='center',
            fontsize=14,
            color='#6B7280',
        )
        ax.set_title(group_title, fontsize=20, pad=20, color='#404547', fontweight='bold')
        for spine in ['top', 'right', 'bottom', 'left']:
            ax.spines[spine].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
        plt.tight_layout()
        return fig_to_uri(fig)

    # Create bars using display names
    bars = ax.bar(
        [d["display_name"] for d in data],
        [d["value"] for d in data],
        color=[d["color"] for d in data],
        edgecolor='white',
        linewidth=1,
    )

    # Add value labels on top of bars
    for bar, item in zip(bars, data):
        height = item["value"]
        va = 'bottom' if height >= 0 else 'top'
        y = height + 0.05 if height >= 0 else height - 0.05

        # Determine text color - green if in highlight list, otherwise black
        text_color = '#10b981' if item["display_name"] in highlight_green_metabolites else 'black'

        # Adjust fontsize based on number of labels
        fontsize = 11 if len(data) > 15 else 14

        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            y,
            f'{height:.2f}',
            ha='center',
            va=va,
            fontsize=fontsize,
            fontweight='bold',
            color=text_color,
        )

    # Add horizontal lines
    ax.axhline(0, color='#374151', linewidth=1)
    ax.axhline(norm_ref[1], color='#6B7280', linestyle='--', linewidth=1)
    ax.axhline(norm_ref[0], color='#6B7280', linestyle='--', linewidth=1)
    ax.axhline(1.96, color='#6B7280', linestyle=':', linewidth=1, alpha=0.5)
    ax.axhline(-1.96, color='#6B7280', linestyle=':', linewidth=1, alpha=0.5)

    # Set title and labels
    ax.set_title(group_title, fontsize=22, pad=20, color='#404547', fontweight='bold')
    ax.set_ylabel(
        f"Отклонение от состояния ЗДОРОВЫЙ, норма от {norm_ref[0]} до {norm_ref[1]}",
        fontsize=14,
        labelpad=15,
    )

    # Set y-axis scale with appropriate steps
    y_min = round(min(-1.5, min([d["value"] for d in data])) - 0.2, 1)
    y_max = round(max(1.5, max([d["value"] for d in data])) + 0.2, 1)
    ax.set_ylim(y_min, y_max)

    y_range = max(abs(y_min), abs(y_max))
    step = (
        5.0
        if y_range > 15
        else 2.5
        if y_range > 12
        else 2.0
        if y_range > 10
        else 1.0 
        if y_range > 7 
        else 0.75 
        if y_range > 5 
        else 0.5
    )
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
        fontsize = 13.5 if len(display_name) > 20 else 15 if len(display_name) > 12 else 15.5
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

        warning_text = f"Missing data for:\n{', '.join(missing_display_names[:3])}" + (
            "..." if len(missing_display_names) > 3 else ""
        )

        ax.text(
            1.02,
            0.95,
            warning_text,
            transform=ax.transAxes,
            fontsize=10,
            color='#dc2626',
            ha='left',
            va='top',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='#fecaca', pad=4),
        )

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
            return "red"  # Above normal range
        else:
            return "green"  # Within normal range

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
            return "Повышен"  # Above normal range
        else:
            return "Норма"  # Within normal range

    except (ValueError, AttributeError):
        # Handle cases where norm_str is not in expected format
        return "Не определено"  # Default text for invalid format





def get_color_age(n):
    if n <= 0:
        return "#10b98158"
    if n <= 10:
        return "#10b96251"  # Light green (similar to 9-10)
    elif n <= 20:
        return "#50c15051"  # Light yellow (similar to 7-8)
    elif n <= 30:
        return "#50c15055"  # Light orange (similar to 5-6)
    elif n <= 40:
        return "#a0d04754"  # Light orange (similar to 5-6)
    elif n <= 50:
        return "#a0d04752"  # Light orange (similar to 5-6)
    elif n <= 60:
        return "#b9d04753"  # Light orange (similar to 5-6)
    elif n <= 70:
        return "#feb71d4f"  # Light orange (similar to 5-6)
    elif n <= 80:
        return "#fe991d50"  # Light orange (similar to 5-6)
    else:
        return "#f23b0854"  # Orange-red (similar to 3-4)


def get_color_age_border(n):
    if n <= 0:
        return '#0e924e'
    if n <= 10:
        return "#0e924e"  # Light green (similar to 9-10)
    elif n <= 20:
        return "#3f993f"  # Light yellow (similar to 7-8)
    elif n <= 30:
        return "#3f993f"  # Light orange (similar to 5-6)
    elif n <= 40:
        return "#80a639"  # Light orange (similar to 5-6)
    elif n <= 50:
        return '#80a639'  # Light orange (similar to 5-6)
    elif n <= 60:
        return "#92a437"  # Light orange (similar to 5-6)
    elif n <= 70:
        return "#c08a16"  # Light orange (similar to 5-6)
    elif n <= 80:
        return "#c57717"  # Light orange (similar to 5-6)
    else:
        return "#c6340b"  # Orange-red (similar to 3-4)


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
    elif value < ref_min:
        return '#dc3545'
    else:
        return '#404547'


def heighlight_out_of_range(value: float, ref_stats_entry: str):
    ref_min, ref_max = get_ref_min_max(ref_stats_entry)
    if value > ref_max:
        return '#f8d7da'
    elif value < ref_min:
        return '#f8d7da'
    else:
        return 'white'


import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def normal_dist(N: int, a: float, value: float) -> str:
    """
    Generate a colored normal distribution curve with a vertical line at the specified percentage value.
    
    Args:
        N: Number of points in the distribution
        a: Range of the distribution (-a to a)
        value: Position to mark (0-100 scale)
        
    Returns:
        str: Path to the saved image
    """
    # Generate normal distribution data
    x = np.linspace(-a, a, N)
    y = (1 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * x**2)
    
    # Create figure with transparent background
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_alpha(0)
    ax.set_facecolor('none')
    
    # Set limits and remove axes
    ax.set_ylim(min(y), max(y) + 0.001)
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Remove borders
    for pos in ['top', 'bottom', 'left', 'right']:
        ax.spines[pos].set_visible(False)
    
    # Exact color list as specified
    color_spectrum = [
        '#10b981',  # 0
        '#10b962',  # 1-10
        '#50c150',  # 11-20
        "#55d047",  # 21-30
        '#9fd047',  # 31-40
        "#b5d047",  # 41-50
        "#d0a747",  # 51-60
        "#d08c47",  # 61-70
        "#d06947",  # 71-80
        "#d04947"   # 81+
    ]
    
    # Create colormap with precise color positions
    cmap = mpl.colors.LinearSegmentedColormap.from_list(
        "aging_spectrum", 
        color_spectrum, 
        N=len(color_spectrum)
    )
    
    # Fill the distribution with gradient colors
    for i in range(N - 1):
        # Normalize position to [0,1] for colormap
        norm_pos = (x[i] + a) / (2 * a)
        ax.fill_between(
            [x[i], x[i + 1]], 
            [0, 0], 
            [y[i], y[i + 1]], 
            color=cmap(norm_pos)
        )
    
    # Add the distribution line
    ax.plot(x, y, color='#666666', linewidth=1.2, alpha=0.8)
    
    # Convert percentage (0-100) to x-axis position (-a to a)
    line_pos = np.interp(value, [0, 100], [-a, a])
    
    # Add vertical line
    ax.axvline(
        line_pos,  # Use the converted position
        ymin=0,  # Start slightly above bottom
        ymax=0.95,  # End slightly below top
        color='#2563eb',
        linestyle='-',
        linewidth=3.5,
        alpha=0.9,
        clip_on=True
    )
    
    # Save with transparent background
    output_path =  base_dir + '\\assets' + '\\normal.png'
    plt.savefig(
        output_path, 
        format='png', 
        dpi=200, 
        bbox_inches='tight', 
        pad_inches=0,
        transparent=True
    )
    plt.close()
    
    return output_path


def procent_validator(n):
    """
    A function that validates and formats a given number as a percentage.

    Parameters:
    n (int): The number to be validated and formatted as a percentage.

    Returns:
    str: A string representing the formatted percentage.
    """
    if n > 100:
        return '100%'
    else:
        return f'{n}%'


def get_color_under_normal_dist(n):
    if n <= 0:
        return '#10b981'
    if n <= 10:
        return '#10b962'  # Light green (similar to 9-10)
    elif n <= 20:
        return '#50c150'  # Light yellow (similar to 7-8)
    elif n <= 30:
        return '#9fd047'  # Light orange (similar to 5-6)
    elif n <= 40:
        return '#feb61d'  # Light orange (similar to 5-6)
    elif n <= 50:
        return '#fe991d'  # Light orange (similar to 5-6)
    elif n <= 60:
        return '#f25708'  # Light orange (similar to 5-6)
    elif n <= 70:
        return "#f23b08"  # Light orange (similar to 5-6)
    elif n <= 80:
        return '#f21e08'  # Light orange (similar to 5-6)
    else:
        return '#c90909'  # Orange-red (similar to 3-4)


def get_status_level(n):
    if n <= 10:
        return 'Отлично'  # Light green (similar to 9-10)
    elif n <= 20:
        return 'Хорошо'  # Light yellow (similar to 7-8)
    elif n <= 30:
        return 'Хорошо'  # Light orange (similar to 5-6)
    elif n <= 40:
        return 'Требуется коррекция'  # Light orange (similar to 5-6)
    elif n <= 50:
        return 'Требуется коррекция'  # Light orange (similar to 5-6)

    elif n <= 70:
        return 'Серьезные нарушения'  # Light orange (similar to 5-6)
    else:
        return 'Серьезные нарушения'  # Orange-red (similar to 3-4)


def get_text_from_procent(n):
    if n < 30:
        return 'Замедленный темп'
    elif n < 60:
        return 'Оптимальный темп'
    elif n < 80:
        return 'Умеренно ускоренный темп'
    else:
        return 'Сильно ускоренный темп'