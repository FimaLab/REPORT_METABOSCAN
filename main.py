import json
from dash import Dash, html, dcc
import os
import pandas as pd
from ui_kit.render_functions import *
from ui_kit.dash_utilit import *
from ui_kit import render_functions
from report_layouts.basic_layout import *
from report_layouts.recomendation_layout import *
from report_layouts import recomendation_layout
from report_layouts import basic_layout
import traceback
import argparse
import signal
import sys

app_pid = os.getpid()

app = Dash(__name__)

render_functions.app = app



def shutdown_handler(signum, frame):
    sys.exit(0)


signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)

def get_layout(layout_type, **kwargs):
    """Factory function to return the appropriate layout based on type"""
    if layout_type == 'basic':
        basic_layout.app = app
        # Удаляем ненужные аргументы для basic_layout
        filtered_kwargs = {k: v for k, v in kwargs.items() 
                         if k not in ['patient_message', 'doctor_message']}
        return basic_layout.create_layout(**filtered_kwargs)
        
    elif layout_type == 'recommendation':
        recomendation_layout.app = app
        return recomendation_layout.create_layout(**kwargs)
        
    else:
        raise ValueError(f"Unknown layout type: {layout_type}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--age', required=True)
    parser.add_argument('--gender', required=True)
    parser.add_argument('--date', required=True)
    parser.add_argument('--layout', required=True, choices=['basic', 'recommendation']),
    parser.add_argument('--metabolomic_data', required=True)
    parser.add_argument('--risk_scores', required=True)
    parser.add_argument('--risk_params', required=True)
    parser.add_argument('--ref_stats', required=True)
    parser.add_argument('--patient_message', default="")
    parser.add_argument('--doctor_message', default="")
    parser.add_argument('--metrics', required=True)
    args = parser.parse_args()
    # Register shutdown handler
    signal.signal(signal.SIGTERM, shutdown_handler)
    

    try:
        # Update global variables from command line args
        name = args.name
        age = args.age
        gender = args.gender
        date = args.date
        patient_message = args.patient_message
        doctor_messsage = args.doctor_message
        metabolomic_data_path = args.metabolomic_data
        risk_scores_path = args.risk_scores
        risk_params_path = args.risk_params

        # Process files with safety checks
        metabolite_data = safe_parse_metabolite_data(metabolomic_data_path)

        risk_scores = pd.read_excel(risk_scores_path)
        ref_params = pd.read_excel(risk_params_path)
        ref_stats = create_ref_stats_from_excel(args.ref_stats)
        
        metrics = pd.read_excel(args.metrics)
        # Convert to the desired JSON structure
        metrics_dict = {}
        for _, row in metrics.iterrows():
            metrics_dict[row['group_name']] = {
                "Acc": f"{row['Acc']}%",
                "Se": f"{row['Se']}%",
                "Sp": f"{row['Sp']}%",
                "+PV": f"{row['Pos_PV']}%",
                "-PV": f"{row['Neg_PV']}%"
            }

        # Generate radial diagram
        radial_path = os.path.join('assets', "radial_diagram.png")
        generate_radial_diagram(risk_scores, radial_path)
        footer_gen = page_footer_generator()

        
         # Prepare layout arguments
        layout_args = {
            'name': name,
            'age': age,
            'date': date,
            'gender': gender,
            'patient_message': patient_message,
            'doctor_message': doctor_messsage,
            'metrics_dict': metrics_dict,
            'footer_gen': footer_gen,
            'ref_stats': ref_stats,
            'risk_scores': risk_scores,
            'ref_params': ref_params,
            'metabolite_data': metabolite_data
        }

        # Get the appropriate layout
        app.layout = get_layout(args.layout, **layout_args)


        print("Starting Dash server...")
        app.run(
            debug=False,
            port=8050,
            host='0.0.0.0',
            dev_tools_serve_dev_bundles=False,
        )
    
    except Exception as e:
        error_msg = f"DASH_APP_ERROR:{type(e).__name__}:{str(e)}"
        print(error_msg, file=sys.stderr)
        print(f"Stack trace:\n{traceback.format_exc()}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()