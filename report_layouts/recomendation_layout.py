from dash import Dash, html
from ui_kit.render_functions import *
from ui_kit.dash_utilit import *

app = None

def create_layout(name, age, gender, date, patient_message, doctor_message, metrics_dict, footer_gen, ref_stats, risk_scores, ref_params, metabolite_data):   
    layout = html.Div(
                [
                    render_page_layout(
                        header=render_main_header_report(name, date, age, gender),
                                       content = html.Div([
                    html.Div(
                        [
                            html.Div(
                                children='Панорамный метаболомный обзор',
                                style={'textAlign': 'center', 'margin': '0px', 'fontSize': '18px', 'fontWeight': '600'},
                            ),
                        ],
                        style={
                            'width': '100%',
                            'background-color': '#2563eb',
                            'border-radius': '5px 5px 0px 0px',
                            "padding": '5px',
                            'color': 'white',
                            'font-family': 'Calibri',
                            'margin': '0px',
                        },
                    ),
                    html.Img(
                        src=app.get_asset_url('radial_diagram.png'),
                        style={
                            'height': '380px',
                            'width': 'auto',  # This maintains aspect ratio
                            'max-width': '100%',  # Ensures it doesn't overflow container
                            'object-fit': 'contain',  # Prevents distortion
                            'margin-top': '6px',
                            'margin-bottom': '2px',
                            'display': 'block',  # Ensures proper margin handling
                            'margin-left': 'auto',
                            'margin-right': 'auto',  # Centers the image
                        },
                    ),
                    render_radial_diagram_legend(),
                    # Plot risk_scores table
                    html.Div(
                        [
                            html.Div(
                                render_category_params(
                                    '1',
                                    'Метаболическая детоксикация',
                                    risk_scores,
                                    ref_params,
                                ),
                                style={'width': '50%'},
                            ),
                            
                            html.Div(
                                render_category_params(
                                    '2',
                                    'Метаболическая адаптация и стрессоустойчивость',
                                    risk_scores,
                                    ref_params,
                                ),
                                style={'width': '50%'},
                            ),
                        ],
                        style={
                            'width': '100%',
                            'gap': '20px',
                            'margin-top': '10px',
                            'display': 'flex',
                            'justify-content': 'space-between',
                            'height': 'fit-content',
                        },
                    ),
                    # Plot risk_scores table
                    html.Div(
                        [
                            html.Div(
                                render_category_params(
                                    '3',
                                    'Воспаление и иммунная активация',
                                    risk_scores,
                                    ref_params,
                                ),
                                style={'width': '50%'},
                            ),
                            html.Div(
                                render_category_params(
                                    '4',
                                    'Цикл Кребса и баланс аминокислот',
                                    risk_scores,
                                    ref_params,
                                ),
                                style={'width': '50%'},
                            ),
                        ],
                        style={
                            'width': '100%',
                            'gap': '20px',
                            'margin-top': '10px',
                            'display': 'flex',
                            'justify-content': 'space-between',
                            'height': 'fit-content',
                        },
                    ),
                    # Plot risk_scores table
                    html.Div(
                        [
                            
                            html.Div(
                                [
                                    render_category_params(
                                        '5',
                                        'Статус микробиоты',
                                        risk_scores,
                                        ref_params,
                                    ),
                                ],
                                style={
                                    'width': '50%',
                                    'display': 'flex',
                                    'flex-direction': 'column',
                                },
                            ),
                            
                            html.Div(
                                render_category_params(
                                    '6',
                                    'Здоровье митохондрий',
                                    risk_scores,
                                    ref_params,
                                ),
                                style={'width': '50%'},
                            ),
                        ],
                        style={
                            'width': '100%',
                            'gap': '20px',
                            'margin-top': '10px',
                            'margin-bottom': '25px',
                            'display': 'flex',
                            'height': 'fit-content',
                        },
                        
                    ), 
                    render_recomendation_message(title="Вывод о состоянии организма:", message=patient_message)
                                ]), footer= next(footer_gen)),
                    
                    render_page_layout(
                        header=render_page_header(date=date, name=name),
                        content=html.Div(
                            [
                                render_info_message(
                                    "Данные по оценке состояния организма получены из экспериментальных данных образцов биобанка Центра биофармацевтического анализа и метаболомных исследований Сеченовского университета."
                                ),
                                # Main container with all score cards
                                html.Div(
                                    style={
                                        "width": "100%",
                                        "margin": "0 auto",
                                        "marginTop": "10px",
                                        "fontFamily": "Calibri, Arial, sans-serif",
                                        "display": "flex",
                                        "flexWrap": "wrap",
                                    },
                                    children=[
                                        # First row of cards
                                        html.Div(
                                            style={
                                                "width": "100%",
                                                "display": "flex",
                                                "gap": "1rem",
                                            },
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
                                                    metrics=metrics_dict["Состояние сердечно-сосудистой системы"],
                                                    risk_scores=risk_scores,
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
                                                    metrics=metrics_dict["Оценка пролиферативных процессов"],
                                                    risk_scores=risk_scores,
                                                ),
                                            ],
                                        ),
                                        # Second row of cards
                                        html.Div(
                                            style={
                                                "width": "100%",
                                                "display": "flex",
                                                "gap": "1rem",
                                                "marginTop": "1rem",
                                            },
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
                                                    metrics=metrics_dict["Состояние функции печени"],
                                                    risk_scores=risk_scores,
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
                                                    metrics=metrics_dict["Состояние дыхательной системы"],
                                                    risk_scores=risk_scores,
                                                ),
                                            ],
                                        ),
                                        # Third row (single card)
                                        html.Div(
                                            style={
                                                "width": "100%",
                                                "display": "flex",
                                                "gap": "1rem",
                                                "marginTop": "1rem",
                                            },
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
                                                    metrics=metrics_dict["Состояние иммунного метаболического баланса"],
                                                    risk_scores=risk_scores,
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                render_stats_legend(),
                            ]
                        ),
                        footer=next(footer_gen),
                    ),

                    render_page_layout(
                        header=render_page_header(date=date, name=name),
                        content=[
                            # Health corridor title
                            render_category_header(order_number=None, title="Коридор здоровья"),
                            render_info_message(
                                "Данные по оценке стандартного отклонения от средних показателей здоровых людей получены из экспериментальных данных образцов биобанка Центра биофармацевтического анализа и метаболомных исследований Сеченовского университета."
                            ),
                            # First row - Phenylalanine and Histidine metabolism
                                         html.B(
                                        "Метаболизм фенилаланина",
                                        style={
                                            'font-size': '15px',
                                            'font-family': 'Calibri',
                                            'color': '#2563eb',
                                            "justify-content": "start"
                                        },
                                    ),
                                            render_coridor_plot(
                                                "Метаболизм фенилаланина",
                                                {
                                                    "Phenylalanine": metabolite_data["Phenylalanine"],
                                                    "Tyrosin": metabolite_data["Tyrosin"],
                                                    "Summ Leu-Ile": metabolite_data["Summ Leu-Ile"],
                                                    "Valine": metabolite_data["Valine"],
                                                    "BCAA": metabolite_data["BCAA"],
                                                    "BCAA/AAA": metabolite_data["BCAA/AAA"],
                                                    "Phe/Tyr": metabolite_data["Phe/Tyr"],
                                                    "Val/C4": metabolite_data["Val/C4"],
                                                    "(Leu+IsL)/(C3+С5+С5-1+C5-DC)": metabolite_data[
                                                        "(Leu+IsL)/(C3+С5+С5-1+C5-DC)"
                                                    ],
                                                },
                                                ref_stats=ref_stats,
                                            ),
                                        html.B(
                                        "Метаболизм гистидина",
                                        style={
                                            'font-size': '15px',
                                            'font-family': 'Calibri',
                                            'color': '#2563eb',
                                            "justify-content": "start"
                                        },
                                    ),
                                            render_coridor_plot(
                                                "Метаболизм гистидина",
                                                {
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
                                                    
                                                    "Carnosine": metabolite_data["Carnosine"],
                                                    "GSG Index": metabolite_data["GSG Index"],
                                                },
                                                ref_stats=ref_stats,
                                            ),
                                
                            # Second row - Methionine and Kynurenine pathways
                                        html.B(
                                        "Метаболизм метионина",
                                        style={
                                            'font-size': '15px',
                                            'font-family': 'Calibri',
                                            'color': '#2563eb',
                                            "justify-content": "start"
                                        },
                                    ),
                                            render_coridor_plot(
                                                "Метаболизм метионина",
                                                {
                                                    "Methionine": metabolite_data["Methionine"],
                                                    "Methionine-Sulfoxide": metabolite_data["Methionine-Sulfoxide"],
                                                    "Taurine": metabolite_data["Taurine"],
                                                    "Betaine": metabolite_data["Betaine"],
                                                    "Choline": metabolite_data["Choline"],
                                                    "TMAO": metabolite_data["TMAO"],
                                                    
                                                    "Methionine + Taurine": metabolite_data["Methionine + Taurine"],
                                                    "Betaine/choline": metabolite_data["Betaine/choline"],
                                                    "Met Oxidation": metabolite_data["Met Oxidation"],
                                                    "TMAO Synthesis": metabolite_data["TMAO Synthesis"],
                                                    "DMG / Choline": metabolite_data["DMG / Choline"],
                                                },
                                                ref_stats=ref_stats,
                                            ),
                                            html.B(
                                        "Кинурениновый путь",
                                        style={
                                            'font-size': '15px',
                                            'font-family': 'Calibri',
                                            'color': '#2563eb',
                                            "justify-content": "start"
                                        },
                                    ),
                                            render_coridor_plot(
                                                "Кинурениновый путь",
                                                {
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
                                                ref_stats=ref_stats,
                                            ),
                                
                            

                        ],
                        footer=next(footer_gen),
                    ),

                    render_page_layout(
                        header=render_page_header(date=date, name=name),
                        content=[
                            render_category_header(order_number=None, title="Коридор здоровья"),
                            render_info_message(
                                "Данные по оценке стандартного отклонения от средних показателей здоровых людей получены из экспериментальных данных образцов биобанка Центра биофармацевтического анализа и метаболомных исследований Сеченовского университета."
                            ),
                            # Third row - Serotonin and Indole pathways
                                        html.B(
                                        "Серотониновый путь",
                                        style={
                                            'font-size': '15px',
                                            'font-family': 'Calibri',
                                            'color': '#2563eb',
                                            "justify-content": "start"
                                        },
                                    ),
                                            render_coridor_plot(
                                                "Серотониновый путь",
                                                {
                                                    "Serotonin": metabolite_data["Serotonin"],
                                                    "HIAA": metabolite_data["HIAA"],
                                                    "5-hydroxytryptophan": metabolite_data["5-hydroxytryptophan"],
                                                    "Serotonin / Trp": metabolite_data["Serotonin / Trp"],
                                                },
                                                ref_stats=ref_stats,
                                            ),
                                            html.B(
                                        "Индоловый путь",
                                        style={
                                            'font-size': '15px',
                                            'font-family': 'Calibri',
                                            'color': '#2563eb',
                                            "justify-content": "start"
                                        },
                                    ),
                                            render_coridor_plot(
                                                "Индоловый путь",
                                                {
                                                    "Indole-3-acetic acid": metabolite_data["Indole-3-acetic acid"],
                                                    "Indole-3-lactic acid": metabolite_data["Indole-3-lactic acid"],
                                                    "Indole-3-carboxaldehyde": metabolite_data[
                                                        "Indole-3-carboxaldehyde"
                                                    ],
                                                    "Indole-3-propionic acid": metabolite_data[
                                                        "Indole-3-propionic acid"
                                                    ],
                                                    "Indole-3-butyric": metabolite_data["Indole-3-butyric"],
                                                    "Tryptamine": metabolite_data["Tryptamine"],
                                                    "Tryptamine / IAA": metabolite_data["Tryptamine / IAA"],
                                                },
                                                ref_stats=ref_stats,
                                            ),
                                            html.B(
                                        "Метаболизм аргинина",
                                        style={
                                            'font-size': '15px',
                                            'font-family': 'Calibri',
                                            'color': '#2563eb',
                                            "justify-content": "start"
                                        },
                                    ),
                                            render_coridor_plot(
                                                "Метаболизм аргинина",
                                                {
                                                    "Proline": metabolite_data["Proline"],
                                                    "Hydroxyproline": metabolite_data["Hydroxyproline"],
                                                    
                                                    "Arginine": metabolite_data["Arginine"],
                                                    "ADMA": metabolite_data["ADMA"],
                                                    "Arg/ADMA": metabolite_data["Arg/ADMA"],
                                                    "NMMA": metabolite_data["NMMA"],
                                                    "TotalDMA (SDMA)": metabolite_data["TotalDMA (SDMA)"],
                                                    "(Arg+HomoArg)/ADMA": metabolite_data["(Arg+HomoArg)/ADMA"],
                                                    "Homoarginine": metabolite_data["Homoarginine"],
                                        
                                                    
                                                    "Citrulline": metabolite_data["Citrulline"],
                                                    "Ornitine": metabolite_data["Ornitine"],
                                                    "Aspartic acid": metabolite_data["Aspartic acid"],
                                                    "Asparagine": metabolite_data["Asparagine"],
                                                    
                                                    
                                                    "Creatinine": metabolite_data["Creatinine"],
                                                    
                                                    "Arg/Orn+Cit": metabolite_data["Arg/Orn+Cit"],
                                                    "ADMA/(Adenosin+Arginine)": metabolite_data[
                                                        "ADMA/(Adenosin+Arginine)"
                                                    ],
                                                    
                                                    "Sum of Dimethylated Arg": metabolite_data[
                                                        "Sum of Dimethylated Arg"
                                                    ],
                                                    "Symmetrical Arg Methylation": metabolite_data[
                                                        "Symmetrical Arg Methylation"
                                                    ],
                                                    "Ratio of Pro to Cit": metabolite_data["Ratio of Pro to Cit"],
                                                    "Cit Synthesis": metabolite_data["Cit Synthesis"],
                                                },ref_stats=ref_stats,
                                            ),
                                    html.B(
                                        "Метаболизм ацилкарнитинов (соотношения)",
                                        style={
                                            'font-size': '15px',
                                            'font-family': 'Calibri',
                                            'color': '#2563eb',
                                            "justify-content": "start"
                                        },
                                    ),
                                            render_coridor_plot(
                                                "Метаболизм ацилкарнитинов (соотношения)",
                                                {
                                                    "Alanine": metabolite_data["Alanine"],
                                                    "C0": metabolite_data["C0"],
                                                    "Ratio of AC-OHs to ACs": metabolite_data["Ratio of AC-OHs to ACs"],
                                                    "СДК": metabolite_data["СДК"],
                                                    "ССК": metabolite_data["ССК"],
                                                    "СКК": metabolite_data["СКК"],
                                                    "C0/(C16+C18)": metabolite_data["C0/(C16+C18)"],
                                                    "Ratio of Short-Chain to Long-Chain ACs": metabolite_data[
                                                        "Ratio of Short-Chain to Long-Chain ACs"
                                                    ],
                                                    "С2/С0": metabolite_data["С2/С0"],
                                                    "CPT-2 Deficiency (NBS)": metabolite_data["CPT-2 Deficiency (NBS)"],
                                                    
                                                    "Ratio of Medium-Chain to Long-Chain ACs": metabolite_data[
                                                        "Ratio of Medium-Chain to Long-Chain ACs"
                                                    ],
                                                    "Ratio of Short-Chain to Medium-Chain ACs": metabolite_data[
                                                        "Ratio of Short-Chain to Medium-Chain ACs"
                                                    ],
                                                    "Sum of ACs": metabolite_data["Sum of ACs"],
                                                    "Sum of ACs + С0": metabolite_data["Sum of ACs + С0"],
                                                    "Sum of ACs/C0": metabolite_data["Sum of ACs/C0"],
                                                },
                                                ref_stats=ref_stats,
                                            ),
                            # Second row - Short-chain and Medium-chain Acylcarnitines
                            
                        ],
                        footer=next(footer_gen),
                    ),

                    render_page_layout(
                        header=render_page_header(date=date, name=name),
                        content=[
                           render_category_header(order_number=None, title="Коридор здоровья"),
                            render_info_message(
                                "Данные по оценке стандартного отклонения от средних показателей здоровых людей получены из экспериментальных данных образцов биобанка Центра биофармацевтического анализа и метаболомных исследований Сеченовского университета."
                            ),
                            html.B(
                                        "Короткоцепочечные ацилкарнитины",
                                        style={
                                            'font-size': '15px',
                                            'font-family': 'Calibri',
                                            'color': '#2563eb',
                                            "justify-content": "start"
                                        },
                                    ),
                                            render_coridor_plot(
                                                "Короткоцепочечные ацилкарнитины",
                                                {
                                                    "C2": metabolite_data["C2"],
                                                    "C3": metabolite_data["C3"],
                                                    "C4": metabolite_data["C4"],
                                                    "C5": metabolite_data["C5"],
                                                    "C5-1": metabolite_data["C5-1"],
                                                    "C5-DC": metabolite_data["C5-DC"],
                                                    "C5-OH": metabolite_data["C5-OH"],
                                                },
                                                ref_stats=ref_stats,
                                            ),
                                    html.B(
                                        "Среднецепочечные ацилкарнитины",
                                        style={
                                            'font-size': '15px',
                                            'font-family': 'Calibri',
                                            'color': '#2563eb',
                                            "justify-content": "start"
                                        },
                                    ),
                                            render_coridor_plot(
                                                "Среднецепочечные ацилкарнитины",
                                                {
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
                                                ref_stats=ref_stats,
                                            ),
                            # Third row - Long-chain Acylcarnitines and Other Metabolites
                          html.B(
                                        "Длинноцепочечные ацилкарнитины",
                                        style={
                                            'font-size': '15px',
                                            'font-family': 'Calibri',
                                            'color': '#2563eb',
                                            "justify-content": "start"
                                        },
                                    ),
                                            render_coridor_plot(
                                                "Длинноцепочечные ацилкарнитины",
                                                {
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
                                                ref_stats=ref_stats,
                                            ),
                                            html.B(
                                        "Другие метаболиты",
                                        style={
                                            'font-size': '15px',
                                            'font-family': 'Calibri',
                                            'color': '#2563eb',
                                            "justify-content": "start"
                                        },
                                    ),
                                            render_coridor_plot(
                                                "Другие метаболиты",
                                                {
                                                    "Pantothenic": metabolite_data["Pantothenic"],
                                                    "Riboflavin": metabolite_data["Riboflavin"],
                                                    "Melatonin": metabolite_data["Melatonin"],
                                                    "Uridine": metabolite_data["Uridine"],
                                                    "Adenosin": metabolite_data["Adenosin"],
                                                    "Cytidine": metabolite_data["Cytidine"],
                                                    "Cortisol": metabolite_data["Cortisol"],
                                                    "Histamine": metabolite_data["Histamine"],
                                                },
                                                ref_stats=ref_stats,
                                            ),
                        ],
                        footer=next(footer_gen),
                    ),

                    render_page_layout(
                        header=render_page_header(date=date, name=name),
                        content=html.Div(
                            [
                                render_category_header(order_number='1', title='Аминокислоты'),
                                # Metabolism of Phenylalanine
                                render_metabolite_category_header(title="Метаболизм фенилаланина"),
                                # Phenylalanine (Phe)
                                render_metabolite_row(
                                    concentration=metabolite_data["Phenylalanine"],
                                    ref_stats_entry=ref_stats["Phenylalanine"],
                                    subtitle="Незаменимая глюко-, кетогенная аминокислота",
                                ),
                                # Tyrosine (Tyr)
                                render_metabolite_row(
                                    concentration=metabolite_data["Tyrosin"],
                                    ref_stats_entry=ref_stats["Tyrosin"],
                                    subtitle="Заменимая глюко-, кетогенная аминокислота",
                                ),
                                # Leucine + Isoleucine (Leu+Ile)
                                render_metabolite_row(
                                    concentration=metabolite_data["Summ Leu-Ile"],
                                    ref_stats_entry=ref_stats["Summ Leu-Ile"],
                                    subtitle="Незаменимая глюко-, кетогенная аминокислота",
                                ),
                                # Valine (Val)
                                render_metabolite_row(
                                    concentration=metabolite_data["Valine"],
                                    ref_stats_entry=ref_stats["Valine"],
                                    subtitle="Незаменимая глюкогенная аминокислота",
                                ),
                                # Histidine metabolism header
                                render_metabolite_category_header(title="Метаболизм гистидина"),
                                # Histidine (His)
                                render_metabolite_row(
                                    concentration=metabolite_data["Histidine"],
                                    ref_stats_entry=ref_stats["Histidine"],
                                    subtitle="Незаменимая глюкогенная аминокислота",
                                ),
                                # Methylhistidine (MH)
                                render_metabolite_row(
                                    concentration=metabolite_data["Methylhistidine"],
                                    ref_stats_entry=ref_stats["Methylhistidine"],
                                    subtitle="Метаболит карнозина",
                                ),
                                # Threonine (Thr)
                                render_metabolite_row(
                                    concentration=metabolite_data["Threonine"],
                                    ref_stats_entry=ref_stats["Threonine"],
                                    subtitle="Незаменимая глюкогенная аминокислота",
                                ),
                                # Carnosine (Car)
                                render_metabolite_row(
                                    concentration=metabolite_data["Carnosine"],
                                    ref_stats_entry=ref_stats["Carnosine"],
                                    subtitle="Дипептид, состоящий из аланина и гистидина",
                                ),
                                # Glycine (Gly)
                                render_metabolite_row(
                                    concentration=metabolite_data["Glycine"],
                                    ref_stats_entry=ref_stats["Glycine"],
                                    subtitle="Заменимая глюкогенная аминокислота",
                                ),
                                # Dimethylglycine (DMG)
                                render_metabolite_row(
                                    concentration=metabolite_data["DMG"],
                                    ref_stats_entry=ref_stats["DMG"],
                                    subtitle="Промежуточный продукт синтеза глицина",
                                ),
                                # Serine (Ser)
                                render_metabolite_row(
                                    concentration=metabolite_data["Serine"],
                                    ref_stats_entry=ref_stats["Serine"],
                                    subtitle="Заменимая глюкогенная аминокислота",
                                ),
                                # Lysine (Lys)
                                render_metabolite_row(
                                    concentration=metabolite_data["Lysine"],
                                    ref_stats_entry=ref_stats["Lysine"],
                                    subtitle="Незаменимая кетогенная аминокислота",
                                ),
                                # Glutamic acid (Glu)
                                render_metabolite_row(
                                    concentration=metabolite_data["Glutamic acid"],
                                    ref_stats_entry=ref_stats["Glutamic acid"],
                                    subtitle="Заменимая глюкогенная аминокислота",
                                ),
                                # Glutamine (Gln)
                                render_metabolite_row(
                                    concentration=metabolite_data["Glutamine"],
                                    ref_stats_entry=ref_stats["Glutamine"],
                                    subtitle="Заменимая глюкогенная аминокислота",
                                ),
                                # Methionine metabolism header
                                render_metabolite_category_header(title="Метаболизм метионина"),
                                # Methionine (Met)
                                render_metabolite_row(
                                    concentration=metabolite_data["Methionine"],
                                    ref_stats_entry=ref_stats["Methionine"],
                                    subtitle="Незаменимая глюкогенная аминокислота",
                                ),
                                # Methionine sulfoxide (MetSO)
                                render_metabolite_row(
                                    concentration=metabolite_data["Methionine-Sulfoxide"],
                                    ref_stats_entry=ref_stats["Methionine-Sulfoxide"],
                                    subtitle="Продукт окисления метионина",
                                ),
                                # Taurine (Tau)
                                render_metabolite_row(
                                    concentration=metabolite_data["Taurine"],
                                    ref_stats_entry=ref_stats["Taurine"],
                                    subtitle="Заменимая глюкогенная аминокислота",
                                ),
                                # Betaine (Bet)
                                render_metabolite_row(
                                    concentration=metabolite_data["Betaine"],
                                    ref_stats_entry=ref_stats["Betaine"],
                                    subtitle="Продукт метаболизма холина",
                                ),
                                
                            # Choline (Chl)
                            render_metabolite_row(
                                concentration=metabolite_data["Choline"],
                                ref_stats_entry=ref_stats["Choline"],
                                subtitle="Компонент мембран клеток, источник ацетилхолина",
                            ),
                            # Trimethylamine N-oxide (TMAO)
                            render_metabolite_row(
                                concentration=metabolite_data["TMAO"],
                                ref_stats_entry=ref_stats["TMAO"],
                                subtitle="Продукт метаболизма холина, бетаина и др. бактериями ЖКТ",
                            ),
                            ]
                        ),
                        footer=next(footer_gen),
                    ),

                    render_page_layout(
                        header=render_page_header(date=date, name=name),
                        content=[
                            render_category_header(
                                order_number='2',
                                title='Метаболизм триптофана',
                            ),
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
                                subtitle="Продукт метаболизма триптофана по кинурениновому пути",
                            ),
                            # Anthranilic acid (Ant)
                            render_metabolite_row(
                                concentration=metabolite_data["Antranillic acid"],
                                ref_stats_entry=ref_stats["Antranillic acid"],
                                subtitle="Продукт метаболизма кинуренина",
                            ),
                            # Quinolinic acid (QA)
                            render_metabolite_row(
                                concentration=metabolite_data["Quinolinic acid"],
                                ref_stats_entry=ref_stats["Quinolinic acid"],
                                subtitle="Продукт метаболизма 3-гидроксиантраниловой кислоты",
                            ),
                            # Xanthurenic acid (Xnt)
                            render_metabolite_row(
                                concentration=metabolite_data["Xanthurenic acid"],
                                ref_stats_entry=ref_stats["Xanthurenic acid"],
                                subtitle="Продукт метаболизма кинуренина",
                            ),
                            render_metabolite_row(
                                concentration=metabolite_data["Kynurenic acid"],
                                ref_stats_entry=ref_stats["Kynurenic acid"],
                                subtitle="Продукт метаболизма триптофана по кинурениновому пути",
                            ),
                            render_metabolite_category_header(title="Серотониновый путь"),
                            # Serotonin (Ser)
                            render_metabolite_row(
                                concentration=metabolite_data["Serotonin"],
                                ref_stats_entry=ref_stats["Serotonin"],
                                subtitle="Нейромедиатор",
                            ),
                            # 5-Hydroxyindoleacetic acid (5-HIAA)
                            render_metabolite_row(
                                concentration=metabolite_data["HIAA"],
                                ref_stats_entry=ref_stats["HIAA"],
                                subtitle="Метаболит серотонина",
                            ),
                            # 5-Hydroxytryptophan (5-HTP)
                            render_metabolite_row(
                                concentration=metabolite_data["5-hydroxytryptophan"],
                                ref_stats_entry=ref_stats["5-hydroxytryptophan"],
                                subtitle="Прекурсор серотонина",
                            ),
                            render_metabolite_category_header(title="Индоловый путь"),
                            # 3-Indoleacetic acid (IAA)
                            render_metabolite_row(
                                concentration=metabolite_data["Indole-3-acetic acid"],
                                ref_stats_entry=ref_stats["Indole-3-acetic acid"],
                                subtitle="Продукт катаболизма триптофана кишечной микробиотой",
                            ),
                            # 3-Indolelactic acid (ILA)
                            render_metabolite_row(
                                concentration=metabolite_data["Indole-3-lactic acid"],
                                ref_stats_entry=ref_stats["Indole-3-lactic acid"],
                                subtitle="Продукт катаболизма триптофана кишечной микробиотой",
                            ),
                            # ICAA
                            render_metabolite_row(
                                concentration=metabolite_data["Indole-3-carboxaldehyde"],
                                ref_stats_entry=ref_stats["Indole-3-carboxaldehyde"],
                                subtitle="Продукт катаболизма триптофана кишечной микробиотой",
                            ),
                            # IPA
                            render_metabolite_row(
                                concentration=metabolite_data["Indole-3-propionic acid"],
                                ref_stats_entry=ref_stats["Indole-3-propionic acid"],
                                subtitle="Продукт катаболизма триптофана кишечной микробиотой",
                            ),
                            # IBA
                            render_metabolite_row(
                                concentration=metabolite_data["Indole-3-butyric"],
                                ref_stats_entry=ref_stats["Indole-3-butyric"],
                                subtitle="Продукт катаболизма триптофана кишечной микробиотой",
                            ),
                            # TA
                            render_metabolite_row(
                                concentration=metabolite_data["Tryptamine"],
                                ref_stats_entry=ref_stats["Tryptamine"],
                                subtitle="Продукт катаболизма триптофана кишечной микробиотой, прекурсор для нейромедиаторов",
                            ),
                            # Arginine Metabolism Section
                            render_category_header(
                                order_number='3',
                                title='Метаболизм аргинина',
                            ),
                            render_metabolite_category_header('Метаболизм аргинина'),
                            # Pro
                            render_metabolite_row(
                                concentration=metabolite_data["Proline"],
                                ref_stats_entry=ref_stats["Proline"],
                                subtitle="Заменимая глюкогенная аминокислота",
                            ),
                            # Hyp
                            render_metabolite_row(
                                concentration=metabolite_data["Hydroxyproline"],
                                ref_stats_entry=ref_stats["Hydroxyproline"],
                                subtitle="Источник коллагена",
                            ),
                            # ADMA
                            render_metabolite_row(
                                concentration=metabolite_data["ADMA"],
                                ref_stats_entry=ref_stats["ADMA"],
                                subtitle="Эндогенный ингибитор синтазы оксида азота",
                            ),
                            # MMA
                            render_metabolite_row(
                                concentration=metabolite_data["NMMA"],
                                ref_stats_entry=ref_stats["NMMA"],
                                subtitle="Эндогенный ингибитор синтазы оксида азота",
                            ),
                        ],
                        footer=next(footer_gen),
                    ),

                    render_page_layout(
                        header=render_page_header(date=date, name=name),
                        content=[
                            
                            # Arginine Metabolism Section
                            render_category_header(
                                order_number='3',
                                title='Метаболизм аргинина',
                            ),
                            
                            # SDMA
                            render_metabolite_row(
                                concentration=metabolite_data["TotalDMA (SDMA)"],
                                ref_stats_entry=ref_stats["TotalDMA (SDMA)"],
                                subtitle="Продукт метаболизма аргинина, выводится с почками",
                            ),
                            # HomoArg
                            render_metabolite_row(
                                concentration=metabolite_data["Homoarginine"],
                                ref_stats_entry=ref_stats["Homoarginine"],
                                subtitle="Субстрат для синтазы оксида азота",
                            ),
                            # Arg
                            render_metabolite_row(
                                concentration=metabolite_data["Arginine"],
                                ref_stats_entry=ref_stats["Arginine"],
                                subtitle="Незаменимая глюкогенная аминокислота",
                            ),
                            # Cit
                            render_metabolite_row(
                                concentration=metabolite_data["Citrulline"],
                                ref_stats_entry=ref_stats["Citrulline"],
                                subtitle="Метаболит цикла мочевины",
                            ),
                            # Orn
                            render_metabolite_row(
                                concentration=metabolite_data["Ornitine"],
                                ref_stats_entry=ref_stats["Ornitine"],
                                subtitle="Метаболит цикла мочевины",
                            ),
                            # Asn
                            render_metabolite_row(
                                concentration=metabolite_data["Asparagine"],
                                ref_stats_entry=ref_stats["Asparagine"],
                                subtitle="Заменимая глюкогенная аминокислота",
                            ),
                            # Asp
                            render_metabolite_row(
                                concentration=metabolite_data["Aspartic acid"],
                                ref_stats_entry=ref_stats["Aspartic acid"],
                                subtitle="Заменимая глюкогенная аминокислота",
                            ),
                            # Cr
                            render_metabolite_row(
                                concentration=metabolite_data["Creatinine"],
                                ref_stats_entry=ref_stats["Creatinine"],
                                subtitle="Продукт метаболизма аргинина",
                            ),
                            # Metabolism of Carbohydrates
                            render_category_header(
                                order_number='4',
                                title='Метаболизм жирных кислот',
                            ),
                            # Acylcarnitine Metabolism
                            render_metabolite_category_header('Метаболизм ацилкарнитинов'),
                            # Alanine
                            render_metabolite_row(
                                concentration=metabolite_data["Alanine"],
                                ref_stats_entry=ref_stats["Alanine"],
                                subtitle="Заменимая глюкогенная аминокислота",
                            ),
                            # Carnitine (C0)
                            render_metabolite_row(
                                concentration=metabolite_data["C0"],
                                ref_stats_entry=ref_stats["C0"],
                                subtitle="Основа для ацилкарнитинов, транспорт жирных кислот",
                            ),
                            # Acetylcarnitine (C2)
                            render_metabolite_row(
                                concentration=metabolite_data["C2"],
                                ref_stats_entry=ref_stats["C2"],
                                subtitle="",
                            ),
                            # Short-chain acylcarnitines
                            render_metabolite_category_header('Короткоцепочечные ацилкарнитины'),
                            # Propionylcarnitine (C3)
                            render_metabolite_row(
                                concentration=metabolite_data["C3"],
                                ref_stats_entry=ref_stats["C3"],
                                subtitle="",
                            ),
                            # Butyrylcarnitine (C4)
                            render_metabolite_row(
                                concentration=metabolite_data["C4"],
                                ref_stats_entry=ref_stats["C4"],
                                subtitle="",
                            ),
                            # Isovalerylcarnitine (C5)
                            render_metabolite_row(
                                concentration=metabolite_data["C5"],
                                ref_stats_entry=ref_stats["C5"],
                                subtitle="",
                            ),
                            
                            # Tiglylcarnitine (C5-1)
                            render_metabolite_row(
                                concentration=metabolite_data["C5-1"],
                                ref_stats_entry=ref_stats["C5-1"],
                                subtitle="",
                            ),
                            # Glutarylcarnitine (C5-DC)
                            render_metabolite_row(
                                concentration=metabolite_data["C5-DC"],
                                ref_stats_entry=ref_stats["C5-DC"],
                                subtitle="",
                            ),
                            # Hydroxyisovalerylcarnitine (C5-OH)
                            render_metabolite_row(
                                concentration=metabolite_data["C5-OH"],
                                ref_stats_entry=ref_stats["C5-OH"],
                                subtitle="",
                            ),
                                                        render_metabolite_category_header('Среднецепочечные ацилкарнитины'),
                            # Hexanoylcarnitine (C6)
                            render_metabolite_row(
                                concentration=metabolite_data["C6"],
                                ref_stats_entry=ref_stats["C6"],
                                subtitle="",
                            ),
                            # Adipoylcarnitine (C6-DC)
                            render_metabolite_row(
                                concentration=metabolite_data["C6-DC"],
                                ref_stats_entry=ref_stats["C6-DC"],
                                subtitle="",
                            ),
                            # Octanoylcarnitine (C8)
                            render_metabolite_row(
                                concentration=metabolite_data["C8"],
                                ref_stats_entry=ref_stats["C8"],
                                subtitle="",
                            ),
                            # Octenoylcarnitine (C8-1)
                            render_metabolite_row(
                                concentration=metabolite_data["C8-1"],
                                ref_stats_entry=ref_stats["C8-1"],
                                subtitle="",
                            ),
                        ],
                        footer=next(footer_gen),
                    ),

                    render_page_layout(
                        header=render_page_header(date=date, name=name),
                        content=[
                            # Medium-chain acylcarnitines
                            render_metabolite_category_header('Среднецепочечные ацилкарнитины'),

                            # Decanoylcarnitine (C10)
                            render_metabolite_row(
                                concentration=metabolite_data["C10"],
                                ref_stats_entry=ref_stats["C10"],
                                subtitle="",
                            ),
                            # Decenoylcarnitine (C10-1)
                            render_metabolite_row(
                                concentration=metabolite_data["C10-1"],
                                ref_stats_entry=ref_stats["C10-1"],
                                subtitle="",
                            ),
                            # Decadienoylcarnitine (C10-2)
                            render_metabolite_row(
                                concentration=metabolite_data["C10-2"],
                                ref_stats_entry=ref_stats["C10-2"],
                                subtitle="",
                            ),
                            # Dodecanoylcarnitine (C12)
                            render_metabolite_row(
                                concentration=metabolite_data["C12"],
                                ref_stats_entry=ref_stats["C12"],
                                subtitle="",
                            ),
                            # Dodecenoylcarnitine (C12-1)
                            render_metabolite_row(
                                concentration=metabolite_data["C12-1"],
                                ref_stats_entry=ref_stats["C12-1"],
                                subtitle="",
                            ),
                            # Long-chain acylcarnitines
                            render_metabolite_category_header('Длинноцепочечные ацилкарнитины'),
                            # Tetradecanoylcarnitine (C14)
                            render_metabolite_row(
                                concentration=metabolite_data["C14"],
                                ref_stats_entry=ref_stats["C14"],
                                subtitle="",
                            ),
                            # Tetradecenoylcarnitine (C14:1)
                            render_metabolite_row(
                                concentration=metabolite_data["C14-1"],
                                ref_stats_entry=ref_stats["C14-1"],
                                subtitle="",
                            ),
                            # Tetradecadienoylcarnitine (C14:2)
                            render_metabolite_row(
                                concentration=metabolite_data["C14-2"],
                                ref_stats_entry=ref_stats["C14-2"],
                                subtitle="",
                            ),
                            # Hydroxytetradecanoylcarnitine (C14-OH)
                            render_metabolite_row(
                                concentration=metabolite_data["C14-OH"],
                                ref_stats_entry=ref_stats["C14-OH"],
                                subtitle="",
                            ),
                            # Palmitoylcarnitine (C16)
                            render_metabolite_row(
                                concentration=metabolite_data["C16"],
                                ref_stats_entry=ref_stats["C16"],
                                subtitle="",
                            ),
                            # Hexadecenoylcarnitine (C16:1)
                            render_metabolite_row(
                                concentration=metabolite_data["C16-1"],
                                ref_stats_entry=ref_stats["C16-1"],
                                subtitle="",
                            ),
                            # Hydroxyhexadecenoylcarnitine (C16:1-OH)
                            render_metabolite_row(
                                concentration=metabolite_data["C16-1-OH"],
                                ref_stats_entry=ref_stats["C16-1-OH"],
                                subtitle="",
                            ),
                            # Hydroxyhexadecanoylcarnitine (C16-OH)
                            render_metabolite_row(
                                concentration=metabolite_data["C16-OH"],
                                ref_stats_entry=ref_stats["C16-OH"],
                                subtitle="",
                            ),
                            # Stearoylcarnitine (C18)
                            render_metabolite_row(
                                concentration=metabolite_data["C18"],
                                ref_stats_entry=ref_stats["C18"],
                                subtitle="",
                            ),
                            # Oleoylcarnitine (C18:1)
                            render_metabolite_row(
                                concentration=metabolite_data["C18-1"],
                                ref_stats_entry=ref_stats["C18-1"],
                                subtitle="",
                            ),
                            
                            # Hydroxyoctadecenoylcarnitine (C18:1-OH)
                            render_metabolite_row(
                                concentration=metabolite_data["C18-1-OH"],
                                ref_stats_entry=ref_stats["C18-1-OH"],
                                subtitle="",
                            ),
                            # Linoleoylcarnitine (C18:2)
                            render_metabolite_row(
                                concentration=metabolite_data["C18-2"],
                                ref_stats_entry=ref_stats["C18-2"],
                                subtitle="",
                            ),
                            # Hydroxyoctadecanoylcarnitine (C18-OH)
                            render_metabolite_row(
                                concentration=metabolite_data["C18-OH"],
                                ref_stats_entry=ref_stats["C18-OH"],
                                subtitle="",
                            ),
                        ],
                        footer=next(footer_gen),
                    ),

                    render_page_layout(
                        header=render_page_header(date=date, name=name),
                        content=[
                            # Metabolic balance section header
                            render_category_header(
                                order_number='5',
                                title='Метаболический баланс',
                            ),
                            # Vitamins and neurotransmitters
                            render_metabolite_category_header('Витамины и нейромедиаторы'),
                            # Pantothenic acid
                            render_metabolite_row(
                                concentration=metabolite_data["Pantothenic"],
                                ref_stats_entry=ref_stats["Pantothenic"],
                                subtitle="Витамин B5",
                            ),
                            # Riboflavin
                            render_metabolite_row(
                                concentration=metabolite_data["Riboflavin"],
                                ref_stats_entry=ref_stats["Riboflavin"],
                                subtitle="Витамин B2",
                            ),
                            # Melatonin
                            render_metabolite_row(
                                concentration=metabolite_data["Melatonin"],
                                ref_stats_entry=ref_stats["Melatonin"],
                                subtitle="Регулирует циркадные ритмы",
                            ),
                            # Nucleosides
                            render_metabolite_category_header('Нуклеозиды'),
                            # Uridine
                            render_metabolite_row(
                                concentration=metabolite_data["Uridine"],
                                ref_stats_entry=ref_stats["Uridine"],
                                subtitle="",
                            ),
                            # Adenosine
                            render_metabolite_row(
                                concentration=metabolite_data["Adenosin"],
                                ref_stats_entry=ref_stats["Adenosin"],
                                subtitle="",
                            ),
                            # Cytidine
                            render_metabolite_row(
                                concentration=metabolite_data["Cytidine"],
                                ref_stats_entry=ref_stats["Cytidine"],
                                subtitle="",
                            ),
                            # Allergy and stress
                            render_metabolite_category_header('Аллергия и стресс'),
                            # Cortisol
                            render_metabolite_row(
                                concentration=metabolite_data["Cortisol"],
                                ref_stats_entry=ref_stats["Cortisol"],
                                subtitle="",
                            ),
                            # Histamine
                            render_metabolite_row(
                                concentration=metabolite_data["Histamine"],
                                ref_stats_entry=ref_stats["Histamine"],
                                subtitle="",
                            ),
                             # Energy Metabolism Section
                            html.Div(
                                [
                                    render_category_header(
                                        "6", " Энергетический обмен, цикл Кребса и баланс аминокислот"
                                    ),
                                    render_ratios_row(
                                        value=metabolite_data['Glutamine/Glutamate'],
                                        ref_stats_entry=ref_stats["Glutamine/Glutamate"],
                                        description='''Отражает баланс между аминокислотами,
                                                    участвующими в азотном обмене, регуляции
                                                    энергетического метаболизма и
                                                    нейротрансмиттерной активности.
                                                    ''',
                                    ),
                                    render_ratios_row(
                                        value=metabolite_data['Ratio of Pro to Cit'],
                                        ref_stats_entry=ref_stats["Ratio of Pro to Cit"],
                                        description='''Отражает баланс аминокислотного обмена,
                                                связанного с циклом мочевины, синтезом
                                                аргинина и состоянием энергетического и
                                                сосудистого метаболизма организма.''',
                                    ),
                                    render_ratios_row(
                                        value=metabolite_data['Cit Synthesis'],
                                        ref_stats_entry=ref_stats["Cit Synthesis"],
                                        description='''Отражает эффективность процесса синтеза
                                                    цитруллина из орнитина в рамках цикла
                                                    мочевины, а также функциональное состояние
                                                    печени, сосудистого здоровья и обмена азота.''',
                                    ),
                                    render_ratios_row(
                                        value=metabolite_data['BCAA'],
                                        ref_stats_entry=ref_stats["BCAA"],
                                        description="""Отражает общий уровень трёх аминокислот:
                                                валина (Val), лейцина (Leu) и изолейцина (Ile).
                                                Эти аминокислоты важны для оценки
                                                энергетического метаболизма, мышечного и
                                                печёночного обмена, риска развития
                                                метаболического синдрома, диабета и
                                                сердечно-сосудистых заболеваний.""",
                                    ),
                                    render_ratios_row(
                                        value=metabolite_data['BCAA/AAA'],
                                        ref_stats_entry=ref_stats["BCAA/AAA"],
                                        description='''Индекс Фишера, отношение аминокислот с
                                                        разветвлённой цепью к ароматическим
                                                        аминокислотам - отражает баланс между
                                                        группами аминокислот и используется для
                                                        оценки функционального состояния печени,
                                                        метаболического статуса и риска печёночной
                                                        энцефалопатии.
                                                        ''',
                                    ),
                                    render_ratios_row(
                                        value=metabolite_data['Phe/Tyr'],
                                        ref_stats_entry=ref_stats["Phe/Tyr"],
                                        description='''Отражает активность фермента фенилаланингидроксилазы, участвующего в превращении
                                                            фенилаланина в тирозин, и является маркером
                                                            состояния функции печени и процессов
                                                            метаболизма аминокислот.''',
                                    ),
                                    render_ratios_row(
                                        value=metabolite_data['Glycine/Serine'],
                                        ref_stats_entry=ref_stats["Glycine/Serine"],
                                        description='''Отражает баланс между двумя важными
                                                    аминокислотами, участвующими в процессах
                                                    метилирования, антиоксидантной защиты,
                                                    регуляции воспаления и клеточного
                                                    метаболизма.
                                                    ''',
                                    ),
                                    render_ratios_row(
                                        value=metabolite_data['GSG Index'],
                                        ref_stats_entry=ref_stats["GSG Index"],
                                        description='''Отражает баланс между возбуждающей
                                                нейромедиаторной активностью и
                                                антиоксидантной, противовоспалительной
                                                защитой организма.
                                                ''',
                                    ),
                                ]
                            )
                        
                        ],
                        footer=next(footer_gen),
                    ),

                    
                    render_page_layout(
                        header=render_page_header(date=date, name=name),
                        content=[
                            # Mitochondrial Function Section 1
                            html.Div(
                                [
                                    render_category_header("7", "Здоровье митохондрий и β-окисление жирных кислот"),
                                    render_ratios_row(
                                        value=metabolite_data['Ratio of AC-OHs to ACs'],
                                        ref_stats_entry=ref_stats["Ratio of AC-OHs to ACs"],
                                        description='''Отражает эффективность β-окисления жирных
                                                кислот в митохондриях и характеризует
                                                митохондриальную функцию и энергетический
                                                обмен организма.
                                                ''',
                                    ),
                                    render_ratios_row(
                                        value=metabolite_data['Ratio of Medium-Chain to Long-Chain ACs'],
                                        ref_stats_entry=ref_stats["Ratio of Medium-Chain to Long-Chain ACs"],
                                        description='''Отражает эффективность β-окисления жирных
                                                        кислот разной длины цепи в митохондриях, а
                                                        также способность организма эффективно
                                                        использовать жирные кислоты в качестве
                                                        источника энергии.
                                                        ''',
                                    ),
                                    render_ratios_row(
                                        value=metabolite_data['СДК'],
                                        ref_stats_entry=ref_stats["СДК"],
                                        description='''Отражает общий уровень длинноцепочечных
                                                        ацилкарнитинов (С14–С18), которые являются
                                                        промежуточными метаболитами β-окисления
                                                        жирных кислот в митохондриях.
                                                        ''',
                                    ),
                                    render_ratios_row(
                                        value=metabolite_data['ССК'],
                                        ref_stats_entry=ref_stats["ССК"],
                                        description='''Отражает общий уровень среднецепочечных
                                                    ацилкарнитинов (С6–С12), которые являются
                                                    промежуточными метаболитами β-окисления
                                                    жирных кислот средней длины в митохондриях.''',
                                    ),
                                    render_ratios_row(
                                        value=metabolite_data['СКК'],
                                        ref_stats_entry=ref_stats["СКК"],
                                        description='''Отражает общий уровень короткоцепочечных
                                                        ацилкарнитинов (С2–С5), которые являются
                                                        промежуточными метаболитами β-окисления
                                                        короткоцепочечных жирных кислот и
                                                        аминокислотного обмена в митохондриях.''',
                                    ),
                                    render_ratios_row(
                                        value=metabolite_data['C0/(C16+C18)'],
                                        ref_stats_entry=ref_stats["C0/(C16+C18)"],
                                        description='''Отражает баланс между свободным карнитином
                                                        и длинноцепочечными ацилкарнитинами,
                                                        характеризуя способность митохондрий
                                                        эффективно транспортировать и окислять
                                                        длинноцепочечные жирные кислоты.
                                                        ''',
                                    ),
                                    render_ratios_row(
                                        value=metabolite_data['CPT-2 Deficiency (NBS)'],
                                        ref_stats_entry=ref_stats["CPT-2 Deficiency (NBS)"],
                                        description='''Отражает баланс между накоплением
                                                    длинноцепочечных жирных кислот и
                                                    эффективностью финальной стадии их
                                                    окисления до ацетилкарнитина (C2),
                                                    характеризуя общую эффективность
                                                    митохондриального β-окисления жирных
                                                    кислот.''',
                                    ),
                                    render_ratios_row(
                                        value=metabolite_data['С2/С0'],
                                        ref_stats_entry=ref_stats["С2/С0"],
                                        description='''Отражает баланс между ацетилированной
                                                        формой карнитина (ацетилкарнитином),
                                                        образующейся в результате энергетического
                                                        обмена, и свободным карнитином,
                                                        необходимым для транспорта жирных кислот в
                                                        митохондрии.
                                                        ''',
                                    ),
                                    
                                    render_ratios_row(
                                        value=metabolite_data['Ratio of Short-Chain to Long-Chain ACs'],
                                        ref_stats_entry=ref_stats["Ratio of Short-Chain to Long-Chain ACs"],
                                        description='''Отражает баланс между короткоцепочечными и
                                                    длинноцепочечными ацилкарнитинами,
                                                    характеризуя соотношение активности
                                                    окисления короткоцепочечных жирных кислот и
                                                    аминокислот к активности окисления
                                                    длинноцепочечных жирных кислот.
                                                    ''',
                                    ),
                                    render_ratios_row(
                                        value=metabolite_data['Ratio of Short-Chain to Medium-Chain ACs'],
                                        ref_stats_entry=ref_stats["Ratio of Short-Chain to Medium-Chain ACs"],
                                        description='''Отражает баланс между короткоцепочечными и
                                                    среднецепочечными ацилкарнитинами и
                                                    характеризует эффективность
                                                    митохондриального окисления жирных кислот
                                                    разной длины цепи, а также баланс
                                                    аминокислотного обмена.
                                                    ''',
                                    ),
                                    render_ratios_row(
                                        value=metabolite_data['Sum of ACs'],
                                        ref_stats_entry=ref_stats["Sum of ACs"],
                                        description='''Отражает общий уровень ацилкарнитинов
                                                                различной длины цепи (коротко-, средне-,
                                                                длинноцепочечные), являясь интегральным
                                                                маркером состояния митохондриального βокисления жирных кислот и аминокислотного
                                                                обмена.
                                                                ''',
                                    ),
                                    render_ratios_row(
                                        value=metabolite_data['Sum of ACs + С0'],
                                        ref_stats_entry=ref_stats["Sum of ACs + С0"],
                                        description='''Отражает общий пул карнитина в организме,
                                                        включая как свободную форму карнитина (С0),
                                                        так и все связанные формы (ацилкарнитины
                                                        различной длины цепи). Является интегральным
                                                        маркером состояния карнитинового обмена,
                                                        митохондриальной функции и энергетического
                                                        метаболизма.
                                                        ''',
                                    ),
                                    render_ratios_row(
                                        value=metabolite_data['Sum of ACs/C0'],
                                        ref_stats_entry=ref_stats["Sum of ACs/C0"],
                                        description='''Отражает баланс между связанными формами
                                                        карнитина (ацилкарнитины) и свободным
                                                        карнитином (С0), являясь важным интегральным
                                                        индикатором митохондриальной функции,
                                                        карнитинового обмена и общего
                                                        энергетического статуса организма.''',
                                    ),
                                ]
                            )
                        ],
                        footer=next(footer_gen),
                    ),

                    render_page_layout(
                        header=render_page_header(date=date, name=name),
                        content=[
                            # Vascular Health Section
                            html.Div(
                                [
                                    render_category_header("8", "Метилирование, обмен холина и метионина"),
                                    render_ratios_row(
                                        value=metabolite_data['Betaine/choline'],
                                        ref_stats_entry=ref_stats["Betaine/choline"],
                                        description='''Отражает активность обмена холина и степень
                                                        его конверсии в бетаин, характеризуя
                                                        функциональное состояние печени,
                                                        эффективность процессов метилирования и риск
                                                        развития жировой болезни печени (стеатоза).''',
                                    ),
                                    render_ratios_row(
                                        value=metabolite_data['DMG / Choline'],
                                        ref_stats_entry=ref_stats["DMG / Choline"],
                                        description='''Отражает активность пути метилирования,
                                                        эффективность обмена холина и
                                                        функционирование печени.
                                                        ''',
                                    ),
                                    render_ratios_row(
                                        value=metabolite_data['Methionine + Taurine'],
                                        ref_stats_entry=ref_stats["Methionine + Taurine"],
                                        description='''Отражает совокупный запас метаболитов,
                                                        участвующих в антиоксидантной защите,
                                                        детоксикации, метилировании и регуляции
                                                        клеточного метаболизма.
                                                        ''',
                                    ),
                                    render_ratios_row(
                                        value=metabolite_data['Met Oxidation'],
                                        ref_stats_entry=ref_stats["Met Oxidation"],
                                        description='''Отражает степень окисления метионина до его
                                                        окисленного метаболита (метионинсульфоксида), являясь прямым маркером
                                                        оксидативного стресса и антиоксидантной
                                                        защиты организма.
                                                        ''',
                                    ),
                                    render_category_header("9", "Состояние сосудистой системы и эндотелиальной функции"),
                                    render_ratios_row(
                                        value=metabolite_data['Arg/ADMA'],
                                        ref_stats_entry=ref_stats["Arg/ADMA"],
                                        description='''Отражает баланс между доступным для синтеза
                                                        оксида азота (NO) аргинином и ингибитором
                                                        синтеза NO – асимметричным
                                                        диметиларгинином (ADMA).
                                                        ''',
                                    ),
                                    render_ratios_row(
                                        value=metabolite_data['(Arg+HomoArg)/ADMA'],
                                        ref_stats_entry=ref_stats["(Arg+HomoArg)/ADMA"],
                                        description='''Отражает общий баланс сосудорасширяющих
                                                        (вазопротективных) и сосудосуживающих
                                                        (вазопатогенных) факторов, связанных с
                                                        синтезом оксида азота (NO) и эндотелиальной
                                                        функцией.''',
                                    ),
                                    render_ratios_row(
                                        value=metabolite_data['Arg/Orn+Cit'],
                                        ref_stats_entry=ref_stats["Arg/Orn+Cit"],
                                        description='''Отражает активность и баланс обменных
                                                        процессов в цикле мочевины и доступность
                                                        аргинина как субстрата для синтеза оксида азота
                                                        (NO).
                                                        ''',
                                    ),
                                    render_ratios_row(
                                        value=metabolite_data['ADMA/(Adenosin+Arginine)'],
                                        ref_stats_entry=ref_stats["ADMA/(Adenosin+Arginine)"],
                                        description='''Отражает баланс между сосудосуживающими и
                                                        воспалительными влияниями (связанными с
                                                        ADMA) и сосудорасширяющими, защитными
                                                        эффектами, обусловленными аденозином и
                                                        аргинином.
                                                        ''',
                                    ),
                                    render_ratios_row(
                                        value=metabolite_data['Symmetrical Arg Methylation'],
                                        ref_stats_entry=ref_stats["Symmetrical Arg Methylation"],
                                        description='''Отражает степень метилирования аргинина,
                                                        приводящего к образованию симметричного
                                                        диметиларгинина (SDMA), в сравнении с
                                                        доступностью аргинина.''',
                                    ),
                                    render_ratios_row(
                                        value=metabolite_data['Sum of Dimethylated Arg'],
                                        ref_stats_entry=ref_stats["Sum of Dimethylated Arg"],
                                        description='''Отражает общий уровень метилированных
                                                        производных аргинина, связанных с сосудистым
                                                        воспалением, эндотелиальной дисфункцией и
                                                        состоянием почечной фильтрации.
                                                        ''',
                                    ),
                                ]
                            )
                        ],
                        footer=next(footer_gen),
                    ),
                    render_page_layout(
                        header=render_page_header(date=date, name=name),
                        content=[
                            # Inflammation Section
                            html.Div(
                                [
                                    render_category_header(order_number="10", title="Воспаление, стресс и нейромедиаторный баланс"),
                                    render_ratios_row(
                                        value=metabolite_data['Kyn/Trp'],
                                        ref_stats_entry=ref_stats["Kyn/Trp"],
                                        description='''Отражает активность кинуренинового пути
                                                        обмена триптофана, тесно связанного с
                                                        воспалением, состоянием иммунной системы и
                                                        оксидативным стрессом.
                                                        ''',
                                    ),
                                    render_ratios_row(
                                        value=metabolite_data['Trp/(Kyn+QA)'],
                                        ref_stats_entry=ref_stats["Trp/(Kyn+QA)"],
                                        description='''Это соотношение концентрации триптофана к
                                                сумме его метаболитов (кинуренина и
                                                хинолиновой кислоты). Он является важным
                                                маркером воспалительного и нейротоксического
                                                стресса, отражая баланс между доступным
                                                триптофаном и продуктами воспалительного
                                                катаболизма (психоэмоц. статус).
                                                '''
                                    ),
                                    render_ratios_row(
                                        value=metabolite_data['Kyn/Quin'],
                                        ref_stats_entry=ref_stats["Kyn/Quin"],
                                        description='''Отражает баланс между промежуточными
                                                        метаболитами кинуренинового пути:
                                                        относительно нейтральным по действию
                                                        кинуренином и нейротоксичным метаболитом
                                                        хинолиновой кислотой (QА). Этот показатель
                                                        важен для оценки уровня воспаления,
                                                        нейротоксичности и оксидативного стресса.
                                                        '''
                                    ),
                                    render_ratios_row(
                                        value=metabolite_data['Serotonin / Trp'],
                                        ref_stats_entry=ref_stats["Serotonin / Trp"],
                                        description='''Отражает эффективность превращения
                                                        аминокислоты триптофана в нейромедиатор
                                                        серотонин (5-HT), тем самым характеризуя
                                                        функциональное состояние
                                                        серотонинергической системы и баланс
                                                        эмоционального и психического статуса.
                                                        '''
                                    ),
                                    render_ratios_row(
                                        value=metabolite_data['Tryptamine / IAA'],
                                        ref_stats_entry=ref_stats["Tryptamine / IAA"],
                                        description='''Отражает баланс в микробном метаболизме
                                                        триптофана в кишечнике и характеризует
                                                        состояние кишечной микробиоты и кишечного
                                                        барьера.
                                                        '''
                                    ),
                                    render_ratios_row(
                                        value=metabolite_data['TMAO Synthesis'],
                                        ref_stats_entry=ref_stats["TMAO Synthesis"],
                                        description='''Отражает интенсивность образования
                                                        триметиламин-N-оксида (TMAO) из его
                                                        предшественников (бетаина, холина и
                                                        карнитина), характеризуя активность кишечной
                                                        микробиоты и риск воспаления и
                                                        атеросклероза.
                                                        '''
                                    ),
                    render_recomendation_message(title="Информация для лечащего врача:", message=doctor_message),
                                ]
                            )
                        ],
                        footer=next(footer_gen),
                    ),
                    
                    render_page_layout(
                        header=render_page_header(date=date, name=name),
                        content=html.Div(
                            [
                                render_category_header(
                                    order_number=None,
                                    title="Часто задаваемые вопросы",
                                ),
                                render_questions_dialog(),
                            ]
                        ),
                        footer=html.Div([render_qr_codes()]),
                    ),

                ],
                style={'width': '100%', 'height': '100%'},
            )
    return layout
