import pandas as pd
import json
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os
import base64
from io import BytesIO

# Get the directory where your script is located
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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
                'smart_round': int(row['smart_round']),
                'name_view': row['name_view'],
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


ref_path = os.path.join(base_dir, 'Ref.xlsx')
ref_stats = create_ref_stats_from_excel(ref_path)


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
            elif abs(z_score) > 1:  # Moderate deviation
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
        ax.set_title(group_title, fontsize=22, pad=20, color='#404547', fontweight='bold')
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
    ax.axhline(1.2, color='#6B7280', linestyle=':', linewidth=1, alpha=0.5)
    ax.axhline(-1.2, color='#6B7280', linestyle=':', linewidth=1, alpha=0.5)

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
        3.0
        if y_range > 15
        else 1.5 if y_range > 10 else 1.0 if y_range > 7 else 0.75 if y_range > 5 else 0.5
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

                decimals = max(count_decimals(ref_min), count_decimals(ref_max), default_decimals)
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
        return "#96c93881"  # Light yellow (similar to 7-8)
    elif n <= 30:
        return "#b2d04785"  # Light orange (similar to 5-6)
    elif n <= 40:
        return "#cfdc4081"  # Light orange (similar to 5-6)
    elif n <= 50:
        return "#cfdc407c"  # Light orange (similar to 5-6)
    elif n <= 60:
        return "#fef31d80"  # Light orange (similar to 5-6)
    elif n <= 70:
        return "#f290087c"  # Light orange (similar to 5-6)
    elif n <= 80:
        return "#f2620881"  # Light orange (similar to 5-6)
    else:
        return "#c93c0979"  # Orange-red (similar to 3-4)


def get_color_age_border(n):
    if n <= 10:
        return "#327a32"  # Light green (similar to 9-10)
    elif n <= 20:
        return "#577520"  # Light yellow (similar to 7-8)
    elif n <= 30:
        return "#697a2a"  # Light orange (similar to 5-6)
    elif n <= 40:
        return "#6c7222"  # Light orange (similar to 5-6)
    elif n <= 50:
        return "#7a8228"  # Light orange (similar to 5-6)
    elif n <= 60:
        return "#928C1E"  # Light orange (similar to 5-6)
    elif n <= 70:
        return "#865004"  # Light orange (similar to 5-6)
    elif n <= 80:
        return "#843606"  # Light orange (similar to 5-6)
    else:
        return "#762407"  # Orange-red (similar to 3-4)


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


def normal_dist(N: int, a: float, value: float):
    x = np.linspace(-a, a, N)
    y = (1 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * x**2)  # Формула для нормального распределения

    cmap = mpl.colors.LinearSegmentedColormap.from_list(
        "", ["#0db350", "#edd30e", "#ff051e"], gamma=1.2
    )

    plt.figure(figsize=(10, 5))

    plt.ylim(min(y), max(y) + 0.001)

    plt.xticks([])  # Убрать деления по оси X
    plt.yticks([])  # Убрать деления по оси Y

    for pos in ['top', 'bottom', 'left', 'right']:
        plt.gca().spines[pos].set_visible(False)

    # print(x[1], len(y))

    for i in range(N - 1):
        plt.fill_between(
            [x[i], x[i + 1]], [0, 0], [y[i], y[i + 1]], color=cmap((x[i] + a) * N / (a * 2) / N)
        )

    plt.plot(x, y, color='grey')

    checked_value = 0
    if value < 0:
        checked_value = 0
    elif value > 100:
        checked_value = 100
    else:
        checked_value = value

    line = 2 * a * checked_value / 100 - a

    plt.axvline(
        line,
        ymin=min(y) * 1 / max(y),
        ymax=1,
        color='#356ba6',
        linestyle='-',
        linewidth=3,
        clip_on=True,
    )

    return 'normal.png'


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
        return 'Замедленный'
    elif n < 60:
        return 'Нормальный'
    elif n < 80:
        return 'Умеренно ускоренный'
    else:
        return 'Сильно ускоренный'
