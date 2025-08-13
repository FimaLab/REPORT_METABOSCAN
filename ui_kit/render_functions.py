import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dash import dcc
from dash import html
import os
from ui_kit.dash_utilit import *


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)  # Parent folder of the project

app = None

def render_page_layout(header=None, content=None, footer=None):
    """
    Creates a standardized page layout with:
    - Header fixed at top
    - Footer fixed at bottom
    - Content filling remaining space
    
    Args:
        header (dash.html.Component): Header component (optional)
        content (dash.html.Component): Main content component (optional)
        footer (dash.html.Component): Footer component (optional)
    
    Returns:
        html.Div: Complete page layout container
    """
    # Default empty components if none provided
    header = header if header is not None else html.Div()
    content = content if content is not None else html.Div()
    footer = footer if footer is not None else html.Div()
    
    return html.Div(
        [
            # Header section (fixed at top)
            html.Div(
                header,
                style={
                    'width': '100%',
                    'position': 'sticky',
                    'top': '0',
                    'zIndex': '100',
                    'background': 'white'  # Ensure header is visible
                }
            ),
            
            # Content section (fills available space)
            html.Div(
                content,
                style={
                    'width': '100%',
                    'flex': '1',
                    'padding': '0'   # Vertical padding only
                }
            ),
            
            # Footer section (fixed at bottom)
            html.Div(
                footer,
                style={
                    'width': '100%',
                    'position': 'sticky',
                    'bottom': '0',
                    'zIndex': '100',
                    'background': 'white'  # Ensure footer is visible
                }
            )
        ],
        style={
            'display': 'flex',
            'flexDirection': 'column',
            'height': '1180px',
            'width': '100%',
            'padding': '0',  # No padding on container
            'fontFamily': 'Calibri',
            'overflow': 'hidden'  # Prevents double scrollbars
        }
    )


def render_main_header_report(name, date, age, gender):
    """Render the main header section for the report.
    
    Args:
        name (str): Patient name
        date (str): Report date
        age (str): Patient age
        gender (str): Patient gender
        
    Returns:
        html.Div: The complete header component
    """
    return html.Div(
        [
            html.Div(
                [
                    html.Img(
                        src=app.get_asset_url('logo-sechenov.png'),
                        style={
                            'width': '100%',
                            'object-fit': 'contain',
                        },
                    )
                ],
                style={
                    'width': '25%',
                    'height': 'auto',
                    'margin': '0px',
                    'display': 'flex',
                    'justify-content': 'left',
                    'align-items': 'center',
                },
            ),
            html.Div(
                [
                    html.Img(
                        src=app.get_asset_url('logo_inst_tox.png'),
                        style={
                            'width': '100%',
                            'object-fit': 'contain',
                        },
                    )
                ],
                style={
                    'width': '20%',
                    'height': 'auto',
                    'margin': '0px',
                    'display': 'flex',
                    'justify-content': 'left',
                    'align-items': 'center',
                },
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.P('ФИО:', style={'margin': '0px'}),
                                    html.B(
                                        f'{name}',
                                        style={
                                            'margin': '0px',
                                            'margin-left': '5px',
                                        },
                                    ),
                                ],
                                style={
                                    'margin': '0px',
                                    'display': 'flex',
                                    'justify-content': 'left',
                                    'width': '40%',
                                },
                            ),
                            html.Div(
                                [
                                    html.P('Дата:', style={'margin': '0px'}),
                                    html.B(
                                        f'{date}',
                                        style={
                                            'margin': '0px',
                                            'margin-left': '5px',
                                        },
                                    ),
                                ],
                                style={
                                    'margin': '0px',
                                    'display': 'flex',
                                    'justify-content': 'left',
                                    'width': '40%',
                                },
                            ),
                            html.Div(
                                [
                                    html.P('Возраст:', style={'margin': '0px'}),
                                    html.B(
                                        f'{age}',
                                        style={
                                            'margin': '0px',
                                            'margin-left': '5px',
                                        },
                                    ),
                                ],
                                style={
                                    'margin': '0px',
                                    'display': 'flex',
                                    'justify-content': 'left',
                                    'width': '40%',
                                },
                            ),
                            html.Div(
                                [
                                    html.P('Пол:', style={'margin': '0px'}),
                                    html.B(
                                        f'{gender}',
                                        style={
                                            'margin': '0px',
                                            'margin-left': '5px',
                                        },
                                    ),
                                ],
                                style={
                                    'margin': '0px',
                                    'display': 'flex',
                                    'justify-content': 'left',
                                    'width': '40%',
                                },
                            ),
                        ],
                        style={
                            'margin-top': '10px',
                            'margin-left': '35px',
                            'color': 'black',
                            'font-family': 'Calibri',
                            'font-size': '14px',
                        },
                    ),
                ],
                style={
                    'width': '60%',
                    'height': '100px',
                    'color': 'white',
                    'margin': '0px',
                    'background-image': 'url("/assets/rHeader_2.png")',
                    'background-repeat': 'no-repeat',
                    'background-size': '100%',
                    'background-position': 'center',
                },
            ),
        ],
        style={
            'display': 'flex',
            'justify-content': 'right',
            'width': '100%',
            'height': '100px',
            'margin-bottom': '10px',
        },
    )


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
        '#10b981',  # 10 баллов
    ]

    # Fill between levels with the specified colors
    levels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for i in range(len(levels) - 1):
        ax.fill_between(angles, levels[i], levels[i + 1], color=colors[i], alpha=0.3)

    # Plot data with blue markers and white borders
    ax.fill(angles, risk_levels, color='#2563eb', alpha=0.25)
    ax.plot(
        angles,
        risk_levels,
        color='#2563eb',
        linewidth=2,
        marker='o',
        markersize=8,
        markerfacecolor='#2563eb',
        markeredgecolor='white',
        markeredgewidth=1.5,
    )

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=12, color='#404547')

    # Label adjustments
    for label, angle in zip(ax.get_xticklabels(), angles[:-1]):
        label.set_rotation_mode('anchor')
        if np.pi / 2 < angle < 3 * np.pi / 2:
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


# [template_elements_img/group_params.png]
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
        header = html.Div(
            [
                # Header container
                html.Div(
                    [
                        html.Div(
                            [
                                html.P(
                                    f"{group_number}.",
                                    style={
                                        'margin': '0px',
                                        'font-weight': 'bold',
                                        'margin-right': '5px',
                                        'color': '#404547',
                                        'font-size': '0.9rem',
                                    },
                                ),
                                html.P(
                                    group_risk_name,
                                    style={
                                        'margin': '0px',
                                        'margin-bottom': '1px',
                                        'width': '200px',
                                        'font-weight': 'bold',
                                        'color': '#404547',
                                        'font-size': '0.9rem',
                                    },
                                ),
                            ],
                            style={
                                'display': 'flex',
                                'justify-content': 'left',
                                'width': 'auto',
                                'height': '18px',
                            },
                        ),
                        # Score container
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [],
                                            style={
                                                'width': f"{overall_score * 10}%",
                                                'background-color': get_color_under_normal_dist(
                                                    100 - (overall_score * 10)
                                                ),
                                                'border-radius': '2px',
                                                'height': '13px',
                                                'line-height': 'normal',
                                                'display': 'inline-block',
                                                'vertical-align': 'center',
                                            },
                                        ),
                                    ],
                                    style={
                                        'display': 'flex',
                                        'align-self': 'center',
                                        'width': '70px',
                                        'height': '13px',
                                        'line-height': 'normal',
                                        'border-radius': '2px',
                                        'background-color': 'lightgrey',
                                        'margin-left': '5px',
                                        'margin-right': '5px',
                                    },
                                ),
                                html.B(
                                    f"{overall_score} из 10",
                                    style={'margin': '0px', 'color': '#404547'},
                                ),
                            ],
                            style={
                                'display': 'flex',
                                'flex-direction': 'row',
                                'flex-wrap': 'nowrap',
                                'align-items': 'center',
                            },
                        ),
                    ],
                    style={
                        'color': 'black',
                        'font-family': 'Calibri',
                        'font-size': '16px',
                        'margin': '0px',
                        'display': 'flex',
                        'justify-content': 'space-between',
                        'margin-bottom': '15px',
                    },
                )
            ]
        )
    else:
        # Standard header for short names
        header = html.Div(
            [
                html.P(
                    f"{group_number}. {group_risk_name}",
                    style={
                        'margin': '0px',
                        'margin-bottom': '1px',
                        'font-weight': 'bold',
                        'color': '#404547',
                        'font-size': '0.9rem',
                    },
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [],
                                    style={
                                        'width': f"{overall_score * 10}%",
                                        'background-color': get_color_under_normal_dist(
                                            100 - (overall_score * 10)
                                        ),
                                        'border-radius': '2px',
                                        'height': '13px',
                                        'line-height': 'normal',
                                        'display': 'inline-block',
                                        'vertical-align': 'center',
                                    },
                                ),
                            ],
                            style={
                                'display': 'flex',
                                'align-self': 'center',
                                'width': '70px',
                                'height': '13px',
                                'line-height': 'normal',
                                'border-radius': '2px',
                                'background-color': 'lightgrey',
                                'margin-left': '5px',
                                'margin-right': '5px',
                            },
                        ),
                        html.B(
                            f"{overall_score} из 10", style={'margin': '0px', 'color': '#404547'}
                        ),
                    ],
                    style={'display': 'flex', 'flex-direction': 'row', 'flex-wrap': 'nowrap'},
                ),
            ],
            style={
                'color': 'black',
                'font-family': 'Calibri',
                'font-size': '16px',
                'margin': '0px',
                'display': 'flex',
                'justify-content': 'space-between',
                'margin-bottom': '0px',
            },
        )

    # Create the HTML structure
    return html.Div(
        [
            # Header
            header,
            # Divider line
            html.Div(
                [],
                style={
                    'width': "100%",
                    'background-color': "#2563eb",
                    'height': '2px',
                    'line-height': 'normal',
                    'display': 'inline-block',
                    'vertical-align': 'center',
                    'margin-bottom': '2px',
                },
            ),
            # Parameters list
            *[
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [],
                                    style={
                                        'width': f'{max(10, 100 - score)}%',
                                        'background-color': get_color_under_normal_dist(score),
                                        'border-radius': '5px',
                                        'height': '10px',
                                        'line-height': 'normal',
                                        'display': 'inline-block',
                                        'vertical-align': 'center',
                                    },
                                ),
                            ],
                            style={
                                'width': '23%',
                                'height': '18px',
                                'line-height': '18px',
                                'margin-right': '5px',
                            },
                        ),
                        html.Div(
                            [
                                html.P(
                                    param_name,
                                    style={
                                        'margin': '0px',
                                        'font-size': '14px',
                                        'font-family': 'Calibri',
                                        'height': '18px',
                                        'margin-left': '3px',
                                    },
                                )
                            ],
                            style={'width': '75%'},
                        ),
                    ],
                    style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'width': '100%',
                        'height': '18px',
                    },
                )
                for param_name, score in param_scores.items()
            ],
        ],
        style={'width': '100%', 'height': 'fit-content'},
    )


# [template_elements_img/ml_card.png]
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
        score = int(
            round(risk_scores.loc[risk_scores["Группа риска"] == title, "Риск-скор"].values[0], 0)
        )
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
            "alignItems": "center",
        },
    )

    # Score visualization components
    score_circle = dcc.Graph(
        figure={
            "data": [
                {
                    "type": "pie",
                    "values": [score, 10 - score],
                    "hole": 0.8,
                    "marker": {"colors": [score_color, "#e5e7eb"]},
                    "rotation": 90,
                    "direction": "clockwise",
                    "showlegend": False,
                    "textinfo": "none",
                    "hoverinfo": "none",
                }
            ],
            "layout": {
                "width": 70,
                "height": 70,
                "margin": {"l": 0, "r": 0, "b": 0, "t": 0},
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
            },
        },
        config={"staticPlot": True},
        style={"position": "absolute", "zIndex": 1},
    )

    score_display = html.Div(
        style={
            "position": "absolute",
            "top": "50%",
            "left": "50%",
            "transform": "translate(-50%, -50%)",
            "textAlign": "center",
            "zIndex": 2,
            "width": "100%",
        },
        children=[
            html.Div(
                f"{score}",
                style={
                    "fontSize": "1.4rem",
                    "fontWeight": "bold",
                    "color": "#111827",
                    "lineHeight": "1",
                },
            ),
            html.Div("/10", style={"fontSize": "0.7rem", "color": "#6b7280", "lineHeight": "100%"}),
        ],
    )

    # Left section (30% width)
    left_section = html.Div(
        style={
            "flex": "0 0 29%",
            "display": "flex",
            "flexDirection": "column",
            "alignItems": "center",
            "paddingRight": "10px",
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
                    "textAlign": "left",
                },
            ),
            html.Div(
                [score_circle, score_display],
                style={
                    "position": "relative",
                    "width": "70px",
                    "height": "70px",
                    "marginBottom": "0.25rem",
                },
            ),
            status_display,
        ],
    )

    # Right section (70% width)
    metrics_display = [
        html.Div(
            [html.Span(f"{key}: "), html.Span(value, style={"fontWeight": "bold"})],
            style={"fontSize": "0.75rem", "color": "#111827"},
        )
        for key, value in metrics.items()
    ]

    right_section = html.Div(
        style={"flex": "1", "paddingLeft": "10px", "borderLeft": "1px solid #e5e7eb"},
        children=[
            html.H3(
                subtitle,
                style={
                    "fontSize": "0.8rem",
                    "fontWeight": "600",
                    "color": "#111827",
                    "marginBottom": "0.5rem",
                },
            ),
            html.P(
                description,
                style={
                    "color": "#374151",
                    "fontSize": "0.75rem",
                    "lineHeight": "1.4",
                    "marginBottom": "0.75rem",
                },
            ),
            html.Div(
                metrics_display,
                style={
                    "display": "flex",
                    "gap": "0.75rem",
                    "flexWrap": "wrap",
                    "marginTop": "0.25rem",
                },
            ),
        ],
    )

    # Main card container
    return html.Div(
        style={
            "flex": "0 0 49%",
            "backgroundColor": "white",
            "border": "1px solid #e5e7eb",
            "borderRadius": "0.5rem",
            "padding": "0.25rem 1rem 0.75rem 1rem",
            "boxSizing": "border-box",
            "fontFamily": "Calibri",
        },
        children=[
            html.Div(
                [left_section, right_section],
                style={"display": "flex"},
            )
        ],
    )


# [template_elements_img/metabolite_row.png]
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

    progress_img = app.get_asset_url('progress.png')
    progress_left_img = app.get_asset_url( 'progress_left.png')
    pointer_img = app.get_asset_url('pointer.png')

    return html.Div(
        style={'margin': '0px'},
        children=[
            html.Div(
                style={'margin': '0px'},
                children=[
                    html.Div(
                        style={
                            'width': '100%',
                            'display': 'flex',
                            'justify-content': 'space-between',
                            'height': (
                                '45px' if not show_subtitle else '52px'
                            ),  # Adjust height based on subtitle
                            'margin-left': '5px',
                        },
                        children=[
                            # Title and subtitle column (39%)
                            html.Div(
                                style={
                                    'width': '39%',
                                    'height': '45px' if not show_subtitle else '52px',
                                    'margin': '0px',
                                    'font-size': '15px',
                                    'font-family': 'Calibri',
                                    'color': 'black',
                                    'display': 'flex',
                                    'flex-direction': 'column',
                                    'justify-content': 'center',  # Center vertically
                                },
                                children=[
                                    html.B(ref_stats_entry["name_view"], style={'height': '20px'}),
                                    (
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
                                                'display': (
                                                    'none' if not show_subtitle else 'block'
                                                ),  # Hide if no subtitle
                                            },
                                        )
                                        if subtitle
                                        else None
                                    ),  # Don't render at all if no subtitle
                                ],
                            ),
                            # Concentration value column (8%)
                            html.Div(
                                style={
                                    'width': '8%',
                                    'height': '45px' if not show_subtitle else '52px',
                                    'margin': '0px',
                                    'font-size': '15px',
                                    'font-family': 'Calibri',
                                    'color': color_text_ref(
                                        concentration, ref_stats_entry=ref_stats_entry
                                    ),
                                    'display': 'flex',
                                    'align-items': 'center',
                                    'justify-content': 'center',
                                },
                                children=[
                                    html.Div(
                                        html.B(
                                            smart_round(
                                                concentration, ref_stats_entry=ref_stats_entry
                                            ),
                                            style={
                                                'text-align': 'center',
                                                'background-color': heighlight_out_of_range(
                                                    concentration, ref_stats_entry=ref_stats_entry
                                                ),
                                                'padding': '3px 8px',
                                                'borderRadius': '12px',
                                            },
                                        )
                                    )
                                ],
                            ),
                            # Progress bar column (27%)
                            html.Div(
                                style={
                                    'width': '27%',
                                    'height': '45px' if not show_subtitle else '52px',
                                    'margin': '0px',
                                    'font-size': '15px',
                                    'font-family': 'Calibri',
                                    'color': '#2563eb',
                                    'display': 'flex',
                                    'align-items': 'center',
                                    'position': 'relative',
                                },
                                children=[
                                    html.Div(
                                        style={'width': '100%', 'position': 'relative'},
                                        children=[
                                            # Progress bar
                                            html.Img(
                                                src=(
                                                    progress_img
                                                    if ref_stats_entry["ref_min"] != 0
                                                    else progress_left_img
                                                ),
                                                style={
                                                    'width': '100%',
                                                    'height': '18px',
                                                    'line-height': 'normal',
                                                    'display': 'inline-block',
                                                    'vertical-align': 'center',
                                                },
                                            ),
                                            # Pointer (arrow)
                                            html.Img(
                                                src=pointer_img,
                                                style={
                                                    'position': 'absolute',
                                                    'height': '38px',
                                                    'width': '4px',
                                                    'left': f'{calculate_pointer_position(concentration, ref_stats_entry=ref_stats_entry)}%',
                                                    'top': '50%',
                                                    'transform': 'translate(-50%, -50%)',
                                                },
                                            ),
                                        ],
                                    )
                                ],
                            ),
                            # Reference range column (21%)
                            html.Div(
                                style={
                                    'width': '21%',
                                    'height': '45px' if not show_subtitle else '52px',
                                    'margin': '0px',
                                    'font-size': '15px',
                                    'font-family': 'Calibri',
                                    'color': 'black',
                                    'display': 'flex',
                                    'align-items': 'center',
                                    'justify-content': 'center',
                                },
                                children=[
                                    html.P(
                                        ref_stats_entry["norm"],
                                        style={
                                            'height': '20px',
                                            'line-height': 'normal',
                                            'display': 'inline-block',
                                            'vertical-align': 'center',
                                            'margin': '0',
                                        },
                                    )
                                ],
                            ),
                        ],
                    )
                ],
            )
        ],
    )


def render_category_header(order_number, title):
    """
    Render a category header with blue background and white text

    Parameters:
    - order_number: The number to display before title (optional, can be None or empty string)
    - title: The header text to display (e.g., "Метаболизм жирных кислот")
    """
    header_text = f"{order_number}. {title}" if order_number else title

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
            'margin-top': '5px',
        },
        children=[
            html.H3(
                children=header_text,
                style={
                    'textAlign': 'center',
                    'margin': '0px',
                    'line-height': 'normal',
                    'display': 'inline-block',
                    'vertical-align': 'center',
                },
            )
        ],
    )


def render_metabolite_category_header(title):
    """
    Render a metabolite category header with title, scale markers, and reference label

    Parameters:
    - title: The category title to display (e.g., "Индоловый путь")
    """
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.B(
                                        title,
                                        style={
                                            'height': '20px',
                                            'line-height': 'normal',
                                            'display': 'inline-block',
                                            'vertical-align': 'center',
                                        },
                                    )
                                ],
                                style={
                                    'width': '39%',
                                    'height': '35px',
                                    'margin': '0px',
                                    'font-size': '16px',
                                    'font-family': 'Calibri',
                                    'color': '#2563eb',
                                    'line-height': '30px',
                                },
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        'Результат',
                                        style={
                                            'display': 'inline-block',
                                            'fontSize': '14px',
                                            'color': '#4D5052',
                                            'fontWeight': '500',
                                        },
                                    )
                                ],
                                style={
                                    'width': '7%',
                                    'height': '20px',
                                    'margin': '0px',
                                    'font-size': '15px',
                                    'font-family': 'Calibri',
                                    'color': 'black',
                                    'text-align': 'center',
                                },
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Span(
                                                '20%',
                                                style={
                                                    'display': 'inline-block',
                                                    'width': '25%',
                                                    'text-align': 'center',
                                                },
                                            ),
                                            html.Span(
                                                '40%',
                                                style={
                                                    'display': 'inline-block',
                                                    'width': '25%',
                                                    'text-align': 'center',
                                                },
                                            ),
                                            html.Span(
                                                '60%',
                                                style={
                                                    'display': 'inline-block',
                                                    'width': '25%',
                                                    'text-align': 'center',
                                                },
                                            ),
                                            html.Span(
                                                '80%',
                                                style={
                                                    'display': 'inline-block',
                                                    'width': '25%',
                                                    'text-align': 'center',
                                                },
                                            ),
                                        ],
                                        style={
                                            'width': '100%',
                                            'display': 'flex',
                                            'justify-content': 'space-between',
                                            'font-family': 'Calibri',
                                            'color': '#4D5052',
                                            'font-size': '13px',
                                            'padding': '4px 8px',
                                        },
                                    )
                                ],
                                style={'width': '27%', 'margin': '0px'},
                            ),
                            html.Div(
                                [html.Div('Норма, мкмоль/л')],
                                style={
                                    'width': '21%',
                                    'height': '20px',
                                    'margin': '0px',
                                    'font-size': '14px',
                                    'font-family': 'Calibri',
                                    'color': '#4D5052',
                                    'text-align': 'center',
                                },
                            ),
                        ],
                        style={
                            'width': '100%',
                            'display': 'flex',
                            'alignItems': 'center',
                            'justify-content': 'space-between',
                            'height': '30px',
                        },
                    ),
                ],
                style={'margin': '0px', 'margin-left': '20px'},
            )
        ]
    )


def render_page_header(date, name, logo_height='45px'):
    """
    Render the main header with date/name on left and logo on right

    Parameters:
    - date: Date string to display
    - name: Patient name string to display
    - logo_height: Height of the logo image (default '53px')
    """

    logo_img = app.get_asset_url('logo.jpg')

    return html.Div(
        style={
            'display': 'flex',
            'justify-content': 'space-between',
            'width': '100%',
            'height': '45px',
            'color': '#2563eb',
        },
        children=[
            # Left section with date and name
            html.Div(
                style={'width': '50%'},
                children=[
                    html.B(
                        f"Дата: {date}",
                        style={'margin': '0px', 'font-size': '16px', 'font-family': 'Calibri'},
                    ),
                    html.Div(
                        style={'margin-top': '2px'},
                        children=[
                            html.B(
                                f'Пациент: {name}',
                                style={
                                    'margin': '0px',
                                    'font-size': '16px',
                                    'font-family': 'Calibri',
                                },
                            )
                        ],
                    ),
                ],
            ),
            # Right section with logo
            html.Div(
                style={'width': '50%', 'text-align': 'right'},
                children=[html.Img(src=logo_img, style={'height': logo_height, 'float': 'right'})],
            ),
        ],
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
            'margin-top': '3px',
            'display': 'flex',
            'justify-content': 'space-between',
            'width': '100%',
        },
        children=[
            # Disclaimer text
            html.P(
                'Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
                style={
                    'color': 'black',
                    'font-family': 'Calibri',
                    'font-size': '13px',
                    'margin': '0px',
                    'text-align': "left",
                    'font-style': 'italic',
                    'width': '85%',
                },
            ),
            # Page number
            html.P(
                f'|{page_number}',
                style={
                    'color': 'black',
                    'font-family': 'Calibri',
                    'font-size': '13px',
                    'margin': '0px',
                    'text-align': "right",
                    'font-style': 'italic',
                    'margin-top': '15px',  # Note: Overrides the 5px from parent
                    'width': '10%',
                },
            ),
        ],
    )


def render_radial_diagram_legend():
    # Common styles
    score_style = {
        'borderRadius': '6px',
        'padding': '0px 10px',
        'fontSize': '0.7rem',
        'fontWeight': 'bold',
        'minWidth': '50px',
        'textAlign': 'center',
    }

    label_style = {
        'borderLeft': 'none',
        'padding': '0px 10px',
        'fontSize': '0.7rem',
        'color': "#404547",
        'flexGrow': '1',
    }

    row_style = {'display': 'flex', 'marginBottom': '2px'}

    return html.Div(
        style={
            'fontFamily': 'Calibri',
            'width': 'fit-content',
            'height': 'fit-content',
            'margin': '0 auto',
            'borderRadius': '5px',
            'overflow': 'hidden',
        },
        children=[
            # Optimal (9-10)
            html.Div(
                style=row_style,
                children=[
                    html.Span(
                        "9-10",
                        style={
                            **score_style,
                            'backgroundColor': "#10b9815b",
                            'color': "#12a070",
                        },
                    ),
                    html.Span(
                        "Метаболическая ось в хорошем или оптимальном состоянии", style=label_style
                    ),
                ],
            ),
            # Slight deviations (7-8)
            html.Div(
                style=row_style,
                children=[
                    html.Span(
                        "7-8",
                        style={
                            **score_style,
                            'backgroundColor': "#a0d04772",
                            'color': "#709e19",
                        },
                    ),
                    html.Span(
                        "Незначительные отклонения, компенсаторные механизмы работают",
                        style=label_style,
                    ),
                ],
            ),
            # Moderate issues (5-6)
            html.Div(
                style=row_style,
                children=[
                    html.Span(
                        "5-6",
                        style={
                            **score_style,
                            'backgroundColor': 'rgba(255,225,175,255)',
                            'color': "#e07d04",
                        },
                    ),
                    html.Span(
                        "Умеренные нарушения — не критично, но уже требует коррекции",
                        style=label_style,
                    ),
                ],
            ),
            # Significant changes (3-4)
            html.Div(
                style=row_style,
                children=[
                    html.Span(
                        "3-4",
                        style={
                            **score_style,
                            'backgroundColor': 'rgb(234, 102, 25, 0.3)',
                            'color': "#c7631b",
                        },
                    ),
                    html.Span(
                        "Существенные изменения — снижен резерв, хроническая нагрузка",
                        style=label_style,
                    ),
                ],
            ),
            # Severe issues (1-2)
            html.Div(
                style=row_style,
                children=[
                    html.Span(
                        "1-2",
                        style={
                            **score_style,
                            'backgroundColor': 'rgb(234, 25, 25, 0.3)',
                            'color': "#b63e3a",
                        },
                    ),
                    html.Span(
                        "Выраженные патологии, декомпенсация, высокий риск",
                        style={**label_style, 'color': "#2C2C2C"},
                    ),
                ],
            ),
        ],
    )


def render_ratios_header(order_number, title):
    """Render header for ratios section with order number, title, and column headers"""
    return html.Div(
        [
            # Title Section
            html.Div(
                html.H3(
                    children=f'{order_number}. {title}',
                    style={
                        'textAlign': 'center',
                        'margin': '0px',
                        'lineHeight': 'normal',
                        'display': 'inline-block',
                        'verticalAlign': 'center',
                        'fontWeight': '600',
                        'fontSize': '19px',
                    },
                ),
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
                    'marginTop': '20px',
                },
            ),
            # Column Headers
            html.Div(
                style={
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(12, minmax(0, 1fr))',
                    'gap': '10px',
                    'fontWeight': '500',
                    'color': "#4D5052",
                    'backgroundColor': '#f8f9fa',
                    'padding': '8px',
                    'borderRadius': '0px 0px 5px 5px',
                    'marginTop': '5px',
                    'fontSize': '14px',
                    'fontFamily': 'Calibri',
                },
                children=[
                    html.Div('Показатель', style={'gridColumn': 'span 2'}),
                    html.Div('Результат', style={'gridColumn': 'span 2', 'textAlign': 'center'}),
                    html.Div('Статус', style={'gridColumn': 'span 1', 'textAlign': 'center'}),
                    html.Div('Норма', style={'gridColumn': 'span 2', 'textAlign': 'center'}),
                    html.Div('Что это отражает?', style={'gridColumn': 'span 5'}),
                ],
            ),
        ]
    )


def render_ratios_row(value, ref_stats_entry, description):
    """Render single ratio row with data from metabolite_data and ref_stats"""
    norm = ref_stats_entry["norm"]
    status_color = get_status_color(value, norm)

    return html.Div(
        style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(12, minmax(0, 1fr))',
            'padding': '8px 10px',
            'alignItems': 'center',
            'borderBottom': '1px solid #e9ecef',
            'fontFamily': 'Calibri',
        },
        children=[
            # Parameter name
            html.Div(
                ref_stats_entry["name_view"],
                style={
                    'gridColumn': 'span 2',
                    'fontWeight': '600',
                    'fontSize': '14px',
                    'color': '#212529',
                },
            ),
            # Value with indicator - now properly centered
            html.Div(
                style={
                    'gridColumn': 'span 2',
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'gap': '4px',
                    'margin': '0 auto',  # Ensures centering within grid cell
                    'width': 'fit-content',  # Prevents full-width stretching
                },
                children=[
                    html.Div(
                        smart_round(value, ref_stats_entry=ref_stats_entry),
                        style={
                            'fontWeight': 'bold',
                            'fontSize': '15px',
                            'color': {'blue': '#2563eb', 'red': '#dc3545', 'green': '#212529'}[status_color],
                        },
                    ),
                    # Status indicator (only for blue/red)
                    html.Div(
                        style={
                            'width': '0',
                            'height': '0',
                            'borderLeft': '5px solid transparent',
                            'borderRight': '5px solid transparent',
                            'borderTop': '8px solid #2563eb' if status_color == 'blue' else 'none',
                            'borderBottom': '8px solid #dc3545' if status_color == 'red' else 'none',
                            'marginLeft': '4px' if status_color == 'red' else '0',
                        }
                    ) if status_color in ['blue', 'red'] else None,
                ],
            ),
            # Status badge
            html.Div(
                style={'gridColumn': 'span 1', 'textAlign': 'center'},
                children=html.Span(
                    get_status_text(value, norm),
                    style={
                        'padding': '3px 8px',
                        'borderRadius': '12px',
                        'fontSize': '14px',
                        'fontWeight': '500',
                        'backgroundColor': {
                            'blue': '#e7f1ff',
                            'red': '#f8d7da',
                            'green': '#e6f7ee',
                        }[status_color],
                        'color': {'blue': '#2563eb', 'red': '#dc3545', 'green': '#198754'}[
                            status_color
                        ],
                    },
                ),
            ),
            # Reference range
            html.Div(
                norm,
                style={
                    'gridColumn': 'span 2',
                    'textAlign': 'center',
                    'fontSize': '14px',
                    'color': '#6c757d',
                },
            ),
            # Description
            html.Div(
                description,
                style={
                    'gridColumn': 'span 5',
                    'color': '#6c757d',
                    'lineHeight': '1.4',
                    'fontSize': '14px',
                },
            ),
        ],
    )


def render_coridor_plot(title, metabolites_dict, ref_stats):
    fig_coridor = plot_metabolite_z_scores(
        metabolite_concentrations=metabolites_dict, group_title=title, ref_stats=ref_stats
    )
    return html.Img(
        src=fig_coridor,
        style={
            'height': 'fit-content',
            'width': '99%',
            'object-fit': 'contain',
            'border': '1px solid #e5e7eb',
            'borderRadius': '12px',
            'padding': '10px 5px',
        },
    )


def render_questions_dialog():

    # Questions and answers content
    qa_pairs = [
        {
            'question': "На чём основаны выводы и рекомендации, представленные в отчёте?",
            'answer': [
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
                ".",
            ],
        },
        {
            'question': "Что именно оценивает система Метабоскан?",
            'answer': [
                "Система Метабоскан предназначена для оценки ",
                html.B("текущего функционального состояния организма на молекулярном уровне"),
                ". Она ",
                html.B("не предназначена"),
                " для определения предрасположенности к заболеваниям или для ",
                html.B("самостоятельной диагностики"),
                ".",
            ],
        },
        {
            'question': "Что показывает метаболомный анализ?",
            'answer': [
                "Метаболомный анализ отражает ",
                html.B("текущие биохимические процессы"),
                " в организме и выявляет ",
                html.B("изменения обмена веществ"),
                ", которые могут быть связаны с вашими индивидуальными особенностями, хроническими заболеваниями, образом жизни и внешними факторами.",
            ],
        },
        {
            'question': "Может ли метаболомный анализ заменить полноценное медицинское обследование?",
            'answer': [
                html.B("Нет."),
                " Данный подход ",
                html.B("не заменяет медицинского обследования"),
                " и не учитывает в полной мере анамнез, приём лекарственных препаратов, БАДов и все аспекты внешней среды, включая особенности питания.",
            ],
        },
        {
            'question': "Для кого и зачем предназначена система Метабоскан?",
            'answer': [
                "Метабоскан — ",
                html.B("навигационный инструмент"),
                " для тех, кто решил взять своё здоровье под контроль. С его помощью вы можете ",
                html.B("отслеживать изменения"),
                " функционального состояния организма на молекулярном уровне, ",
                html.B("своевременно замечать"),
                " положительные или отрицательные последствия различных воздействий и ",
                html.B("оперативно принимать меры"),
                ".",
            ],
        },
        {
            'question': "Что делать, если я хочу правильно понять результаты анализа?",
            'answer': [
                "Для ",
                html.B("корректной интерпретации"),
                " результатов метаболомного анализа необходима ",
                html.B("консультация врача"),
                " с учётом полного анамнеза и вашего образа жизни.",
            ],
        },
    ]

    def create_question_bubble(question_text):
        return html.Div(
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
                        'alignItems': 'center',
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
                                'alignItems': 'center',
                            },
                            children=html.Img(
                                src=app.get_asset_url('person.svg'),
                                style={
                                    'width': '16px',
                                    'height': '16px',
                                },
                            ),
                        ),
                        html.Div(
                            "",
                            style={
                                'fontSize': '12px',
                                'color': '#6b7280',
                                'marginTop': '4px',
                                'font-family': 'Calibri',
                            },
                        ),
                    ],
                ),
                html.Div(
                    style={
                        'width': 'fit-content',
                        'height': 'fit-content',
                        'backgroundColor': '#fee4cf',
                        'borderRadius': '16px',
                        'borderTopLeftRadius': '4px',
                        'padding': '7px 16px',
                        'cursor': 'pointer',
                    },
                    children=[
                        html.Div(
                            style={
                                'display': 'flex',
                                'justifyContent': 'space-between',
                                'alignItems': 'center',
                            },
                            children=[
                                html.Div(
                                    question_text,
                                    style={
                                        'color': '#3d1502',
                                        'fontSize': '13px',
                                        'fontWeight': '500',
                                        'margin': '0',
                                        'font-family': 'Calibri',
                                    },
                                )
                            ],
                        )
                    ],
                ),
            ],
        )

    def create_answer_bubble(answer_content):
        return html.Div(
            style={
                'display': 'flex',
                'gap': '12px',
                'justifyContent': 'flex-end',
                'margin-top': '10px',
            },
            children=[
                html.Div(
                    style={'width': 'fit-content', 'height': 'fit-content', 'maxWidth': '80%'},
                    children=html.Div(
                        style={
                            'backgroundColor': '#dbeafe',
                            'borderRadius': '16px',
                            'borderTopRightRadius': '4px',
                            'padding': '8px 16px',
                        },
                        children=[
                            html.Div(
                                answer_content,
                                style={
                                    'color': '#150c77',
                                    'fontSize': '13px',
                                    'margin': '0',
                                    'lineHeight': '1.5',
                                    'font-family': 'Calibri',
                                },
                            )
                        ],
                    ),
                ),
                html.Div(
                    style={
                        'flexShrink': '0',
                        'display': 'flex',
                        'flexDirection': 'column',
                        'alignItems': 'center',
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
                                'alignItems': 'center',
                            },
                            children=html.Img(
                                src=app.get_asset_url('person.svg'),
                                style={
                                    'width': '16px',
                                    'height': '16px',
                                },
                            ),
                        ),
                        html.Div(
                            "Метабоскан",
                            style={
                                'fontSize': '12px',
                                'color': '#6b7280',
                                'marginTop': '4px',
                                'font-family': 'Calibri',
                                'whiteSpace': 'nowrap',
                            },
                        ),
                    ],
                ),
            ],
        )

    # Generate all question-answer pairs
    qa_elements = []
    for i, pair in enumerate(qa_pairs):
        # Create fresh components
        question = create_question_bubble(pair['question'])
        answer = create_answer_bubble(pair['answer'])

        # Adjust padding for first element
        padding = '15px 0px 0px 0px' if i == 0 else '10px 0px 0px 0px'

        qa_elements.append(
            html.Div(
                style={
                    'padding': padding,
                    'backgroundColor': 'white',
                    'borderTop': 'none',
                },
                children=[question, answer],
            )
        )

    # Create the final two special messages
    final_message1 = html.Div(
        style={'display': 'flex', 'gap': '12px', 'justifyContent': 'flex-end', 'marginTop': '5px'},
        children=[
            html.Div(
                style={'width': 'fit-content', 'height': 'fit-content', 'maxWidth': '80%'},
                children=html.Div(
                    style={
                        'backgroundColor': '#dbeafe',
                        'borderRadius': '16px',
                        'borderTopRightRadius': '8px',
                        'borderBottomRightRadius': '8px',
                        'padding': '8px 16px',
                    },
                    children=[
                        html.Div(
                            [
                                "Больше информации Вы найдете на сайте Центра ",
                                html.B("metaboscan.ru"),
                                ", а также рекомендуем Вам научно-популярные статьи о метаболомике в Telegram-канале ",
                                html.B("@metaboscan"),
                                ".",
                            ],
                            style={
                                'color': '#150c77',
                                'fontSize': '13px',
                                'lineHeight': '1.5',
                                'font-family': 'Calibri',
                            },
                        )
                    ],
                ),
            ),
            html.Div(
                    style={
                        'flexShrink': '0',
                        'display': 'flex',
                        'flexDirection': 'column',
                        'alignItems': 'center',
                    },
                    children=[
                        html.Div(
                            style={
                                'width': '26px',
                                'height': '26px',
                                'backgroundColor': "#ffffff",
                                'borderRadius': '50%',
                                'display': 'flex',
                                'justifyContent': 'center',
                                'alignItems': 'center',
                            },
                            children=html.Img(
                                src=app.get_asset_url('person.svg'),
                                style={
                                    'width': '16px',
                                    'height': '16px',
                                },
                            ),
                        ),
                        html.Div(
                            "Метабоскан",
                            style={
                                'fontSize': '12px',
                                'color': "#ffffff",
                                'marginTop': '4px',
                                'font-family': 'Calibri',
                                'whiteSpace': 'nowrap',
                            },
                        ),
                    ],
                ),
        ],
    )

    final_message2 = html.Div(
        style={'display': 'flex', 'gap': '12px', 'justifyContent': 'flex-end', 'marginTop': '5px'},
        children=[
            html.Div(
                style={'width': 'fit-content', 'height': 'fit-content', 'maxWidth': '80%'},
                children=html.Div(
                    style={
                        'backgroundColor': '#dbeafe',
                        'borderRadius': '16px',
                        'borderTopRightRadius': '8px',
                        'padding': '7px 16px',
                    },
                    children=html.Div(
                        children=[
                            html.B("Желаем вам крепкого здоровья и хорошего самочувствия!"),
                            "❤️",
                        ],
                        style={
                            'color': '#150c77',
                            'fontSize': '13px',
                            'margin': '0',
                            'lineHeight': '1.5',
                            'font-family': 'Calibri',
                        },
                    ),
                ),
            ),html.Div(
                    style={
                        'flexShrink': '0',
                        'display': 'flex',
                        'flexDirection': 'column',
                        'alignItems': 'center',
                    },
                    children=[
                        html.Div(
                            style={
                                'width': '26px',
                                'height': '26px',
                                'backgroundColor': "#ffffff",
                                'borderRadius': '50%',
                                'display': 'flex',
                                'justifyContent': 'center',
                                'alignItems': 'center',
                            },
                            children=html.Img(
                                src=app.get_asset_url('person.svg'),
                                style={
                                    'width': '16px',
                                    'height': '16px',
                                },
                            ),
                        ),
                        html.Div(
                            "Метабоскан",
                            style={
                                'fontSize': '12px',
                                'color': "#ffffff",
                                'marginTop': '4px',
                                'font-family': 'Calibri',
                                'whiteSpace': 'nowrap',
                            },
                        ),
                    ],
                ),
        ],
    )

    return html.Div(children=[*qa_elements, final_message1, final_message2])


def render_qr_codes():
    return html.Div(
        style={
            'display': 'flex',
            'flexDirection': 'column',
            'alignItems': 'center',
            'justifyContent': 'center',
            'gap': '10px',
            'padding': '30px 0px 0px 0px',
            'backgroundColor': 'white',
        },
        children=[
            # QR Codes Row
            html.Div(
                style={
                    'display': 'flex',
                    'flexDirection': 'row',
                    'justifyContent': 'center',
                    'gap': '40px',
                    'flexWrap': 'wrap',
                },
                children=[
                    # Telegram QR Code
                    html.Div(
                        style={
                            'display': 'flex',
                            'flexDirection': 'column',
                            'alignItems': 'center',
                            'gap': '8px',
                        },
                        children=[
                            html.Img(
                                src=app.get_asset_url('telegram_qr_link.png'),
                                style={'width': '100px', 'height': '100px', 'borderRadius': '8px'},
                            ),
                            html.Div(
                                "Наш Telegram-канал",
                                style={
                                    'fontFamily': 'Calibri',
                                    'fontSize': '14px',
                                    'color': '#4b5563',
                                },
                            ),
                        ],
                    ),
                    # Website QR Code
                    html.Div(
                        style={
                            'display': 'flex',
                            'flexDirection': 'column',
                            'alignItems': 'center',
                            'gap': '8px',
                        },
                        children=[
                            html.Img(
                                src=app.get_asset_url('web_qr_link.png'),
                                style={'width': '100px', 'height': '100px', 'borderRadius': '8px'},
                            ),
                            html.Div(
                                "https://metaboscan.ru/",
                                style={
                                    'fontFamily': 'Calibri',
                                    'fontSize': '14px',
                                    'color': '#4b5563',
                                    'textDecoration': 'none',
                                },
                            ),
                        ],
                    ),
                ],
            ),
            # Optional description
            html.Div(
                "Отсканируйте QR-код для перехода",
                style={
                    'fontFamily': 'Calibri',
                    'fontSize': '12px',
                    'color': '#6b7280',
                    'marginTop': '5px',
                },
            ),
        ],
    )

def render_stats_legend():
    """Returns a styled table component explaining statistical metrics"""
    # Define common styles
    table_style = {
        'width': 'fit-content',
        'borderCollapse': 'collapse',
        'fontFamily': 'Calibri',
        'fontSize': '12px'
    }

    container_style = {
        'display': 'flex',
        'color': '#150c77',
        'marginTop': '1rem',
        'marginBottom': '5px',
        'flexDirection': 'row',
        'alignItems': 'center',
        'width': 'fit-content',
        'borderRadius': '0.5rem',
        'padding': '3px 15px',
        'backgroundColor': '#dbeafe'
    }

    # Metric definitions
    metrics = [
        ("Acc", "Точность (диагностическая ценность метода)"),
        ("Se", "Чувствительность (вероятность истинного 'положительного теста')"),
        ("Sp", "Специфичность (вероятность истинного 'отрицательного теста')"),
        ("+PV", "Прогностичность положительного результата (вероятность того, что заболевание присутствует, когда тест положительный)"),
        ("-PV", "Прогностичность отрицательного результата (вероятность того, что заболевание отсутствует, когда тест отрицательный)")
    ]

    # Generate table rows
    table_rows = [
        html.Tr(
            html.Td([
                html.B(f"{abbr}: "),
                html.Span(description)
            ]),
            style={'borderBottom': '1px solid #e5e7eb'} if i < len(metrics)-1 else None
        )
        for i, (abbr, description) in enumerate(metrics)
    ]

    return html.Div(
        style=container_style,
        children=[
            html.Div(
                style={'marginBottom': '5px'},
                children=[
                    html.Table(
                        children=table_rows,
                        style=table_style
                    )
                ]
            )
        ]
    )
    
def render_info_message(message=""):
    return  html.Div(
                        [
                            html.Img(
                                src=app.get_asset_url('info_icon.png'),
                                style={
                                    'width': '20px',
                                    'height': '20px',
                                    'margin-right': '15px',
                                },
                            ),
                            html.Div(
                                message,
                                style={
                                    'color': '#3d1502',
                                    'font-family': 'Calibri',
                                    'font-size': '13px',
                                    'text-align': "left",
                                    'margin': '0px !important',
                                },
                            ),
                        ],
                        style={
                            'display': 'flex',
                            'margin-top': '10px',
                            'margin-bottom': '10px',
                            'flex-direction': 'row',
                            'align-items': 'center',
                            "borderRadius": "0.5rem",
                            'padding': '5px 7px 5px 15px',
                            'background-color': '#fee4cf',
                        },
                    )

def render_age_bell(age_score=0):
    speed_labels=["медленно", "нормально", "быстро"]
    procent_speed = (10 - age_score) * 10
    N = 1000
    a = 3.5
    normal_dist(N, a, procent_speed)
    status_text = get_text_from_procent(procent_speed)
    text_color= get_color_age_border(procent_speed)
    status_color= get_color_age(procent_speed)
    
    
    return html.Div([
        html.Div([
            html.Div([
                # Image container
                html.Div([
                    html.Img(
                        src=app.get_asset_url('normal.png'),
                        style={'width': '100%'}
                    )
                ], style={'height': 'fit-content'}),
                
                # Speed labels
                html.Div([
                    html.P(speed_labels[0], style={
                        'margin': '0px',
                        'display': 'inline-block',
                        'background-color': "#e3e3e3",
                        'border-radius': '5px',
                        'padding': '2px 6px',
                        'width': 'fit-content',
                        'text-align': 'center'
                    }),
                    html.P(speed_labels[1], style={
                        'margin': '0px',
                        'display': 'inline-block',
                        'background-color': "#e3e3e3",
                        'border-radius': '5px',
                        'padding': '2px 6px',
                        'width': 'fit-content',
                    }),
                    html.P(speed_labels[2], style={
                        'margin': '0px',
                        'display': 'inline-block',
                        'background-color': "#e3e3e3",
                        'border-radius': '5px',
                        'padding': '3px 6px',
                        'width': 'fit-content',
                        'text-align': 'center'
                    }),
                ], style={
                    'width': '100%',
                    'color': "#696969",
                    'font-family': 'Calibri',
                    'font-size': '12px',
                    'margin-top': '5px',
                    'display': 'flex',
                    'text-align': 'center',
                    'justify-content': 'space-between'
                }),
                
                # Status box
                html.Div([
                    html.P(
                        status_text,
                        style={
                            'margin': '0',
                            'padding': '5px 10px',
                            'font-size': '15px',
                            'color': text_color,
                            'font-family': 'Calibri',
                            'text-align': 'center'
                        }
                    ),
                ], style={
                    'background-color': status_color,
                    'border-radius': '8px',
                    'margin-top': '10px',
                    'justify-self': 'center',
                    'width': 'fit-content'
                }),
            ], style={'width': '100%'}),
        ])
    ], style={
        'width': '100%',
        'display': 'inline-block',
        'padding': '10px'
    })


def render_metabolism_score(risk_scores):
    """
    Renders the metabolism score assessment component.
    
    Args:
        risk_scores (pd.DataFrame): DataFrame containing 'Риск-скор' column with risk scores
        width (str): Width of the component container
        
    Returns:
        html.Div: The complete metabolism score component
    """
    # Calculate total score (0-100 scale)
    number_of_groups = len(risk_scores['Группа риска'].unique())
    total_score = int(round(pd.to_numeric(risk_scores['Риск-скор'], errors='coerce').sum() * 100 / (number_of_groups * 10), 0))
    
    # Determine rating category and colors
    if total_score >= 90:
        rating = 'Отлично'
        rating_bg = '#e8f5e9'
        rating_color = '#50c150'
    elif total_score >= 67:
        rating = 'Хорошо'
        rating_bg = '#fff3e0'
        rating_color = '#fe991d'
    elif total_score >= 50:
        rating = 'Требуется коррекция'
        rating_bg = '#ffebee'
        rating_color = '#f25708'
    else:
        rating = 'Серьезные нарушения'
        rating_bg = '#ffcdd2'
        rating_color = '#f21f08'
    
    return html.Div(
        style={
            'width': '100%',
            'height': 'fit-content',
            'maxWidth': 'auto'
        },
        children=[
            # Header
            html.Div(
                style={
                    'backgroundColor': '#2563eb',
                    'color': 'white',
                    'padding': '5px 15px',
                    'borderTopLeftRadius': '4px',
                    'borderTopRightRadius': '4px',
                    'marginTop': '20px'
                },
                children=[
                    html.H2(
                        'Общая оценка метаболизма', 
                        style={
                            'margin': '0', 
                            'fontFamily': 'Calibri', 
                            'fontSize': '16px'
                        }
                    )
                ]
            ),
            
            # Main content
            html.Div(
                style={
                    'border': '1px solid #ddd',
                    'padding': '8px 8px 8px 20px',
                    'borderBottomLeftRadius': '4px',
                    'borderBottomRightRadius': '4px'
                },
                children=[
                    html.Div(
                        style={
                            'display': 'flex', 
                            'marginBottom': '7px'
                        },
                        children=[
                            # Left side - Rating boxes
                            html.Div(
                                style={'flex': '1'},
                                children=[
                                    # Excellent
                                    html.Div(
                                        style={
                                            'backgroundColor': '#e8f5e9',
                                            'padding': '4px 8px',
                                            'marginBottom': '10px',
                                            'borderRadius': '4px',
                                            'fontFamily': 'Calibri', 
                                            'fontSize': '14px'
                                        },
                                        children=[
                                            html.Span('Отлично'),
                                            html.Span('90 +', style={'float': 'right'})
                                        ]
                                    ),
                                    
                                    # Good
                                    html.Div(
                                        style={
                                            'backgroundColor': '#fff3e0',
                                            'padding': '4px 8px',
                                            'marginBottom': '10px',
                                            'borderRadius': '4px',
                                            'fontFamily': 'Calibri', 
                                            'fontSize': '14px'
                                        },
                                        children=[
                                            html.Span('Хорошо'),
                                            html.Span('67 +', style={'float': 'right'})
                                        ]
                                    ),
                                    
                                    # Needs correction
                                    html.Div(
                                        style={
                                            'backgroundColor': '#ffebee',
                                            'padding': '4px 8px',
                                            'marginBottom': '10px',
                                            'borderRadius': '4px',
                                            'fontFamily': 'Calibri', 
                                            'fontSize': '14px'
                                        },
                                        children=[
                                            html.Span('Требуется коррекция'),
                                            html.Span('50 +', style={'float': 'right'})
                                        ]
                                    ),
                                    
                                    # Serious pathologies
                                    html.Div(
                                        style={
                                            'backgroundColor': '#ffcdd2',
                                            'padding': '4px 8px',
                                            'borderRadius': '4px',
                                            'fontFamily': 'Calibri', 
                                            'fontSize': '14px'
                                        },
                                        children=[
                                            html.Span('Серьезные нарушения'),
                                            html.Span('<50', style={'float': 'right'})
                                        ]
                                    )
                                ]
                            ),
                            
                            # Right side - Score display
                            html.Div(
                                style={
                                    'flex': '0.8',
                                    'display': 'flex',
                                    'justifyContent': 'center',
                                    'alignItems': 'center'
                                },
                                children=[
                                    html.Div(
                                        style={'textAlign': 'center'},
                                        children=[
                                            html.Div(
                                                style={
                                                    'fontSize': '32px',
                                                    'fontWeight': 'bold',
                                                    'marginBottom': '5px',
                                                    'fontFamily': 'Calibri' 
                                                },
                                                children=[
                                                    f"{total_score}",
                                                    html.Span(
                                                        '/100%',
                                                        style={
                                                            'fontSize': '16px',
                                                            'color': '#666',
                                                            'marginLeft': '5px',
                                                            'fontFamily': 'Calibri' 
                                                        }
                                                    )
                                                ]
                                            ),
                                            html.Div(
                                                children=[html.Span(rating)],
                                                style={
                                                    'backgroundColor': rating_bg,
                                                    'color': rating_color,
                                                    'padding': '5px 15px',
                                                    'borderRadius': '15px',
                                                    'display': 'inline-block',
                                                    'fontFamily': 'Calibri',
                                                    'fontWeight': 'bold',
                                                    'margin': '0px 10px'
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
        ]
    )