import json
import streamlit as st
import os
import tempfile
import time
from datetime import datetime
import base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import subprocess
import sys
import logging
import requests
import psutil
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from config_ml import (
    metabolites_selected_onco, metabolites_selected_CVD,
    metabolites_selected_Liv, metabolites_selected_PULM,
    metabolites_selected_RA, thresholds, TRAIN_PARAMS
)
import joblib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='report_generator.log'
)

def setup_chrome_driver():
    """Configure Chrome WebDriver with extended timeout settings"""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(55)
    driver.set_script_timeout(40)
    return driver

def is_dash_process(process):
    """Check if process is our Dash application"""
    try:
        cmdline = ' '.join(process.cmdline()).lower()
        return ('main.py' in cmdline or 'dash' in cmdline) and 'python' in process.name().lower()
    except (psutil.NoSuchProcess, psutil.AccessDenied, AttributeError):
        return False

def kill_dash_app(port=8050):
    """Kill only the Dash app running on specified port"""
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # Cross-platform way to check connections
            connections = proc.net_connections()
            for conn in connections:
                if conn.laddr.port == port and is_dash_process(proc):
                    try:
                        proc.terminate()
                        proc.wait(timeout=5)
                    except (psutil.NoSuchProcess, psutil.TimeoutExpired):
                        try:
                            proc.kill()
                        except:
                            pass
                    break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.Error):
            continue

def wait_for_dash_app(timeout=45):
    """Wait for Dash app to become ready with content verification"""
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            # First check if port is in use
            port_in_use = False
            for proc in psutil.process_iter(['pid']):
                try:
                    for conn in proc.connections():
                        if conn.laddr.port == 8050:
                            port_in_use = True
                            break
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.Error):
                    continue
            
            if not port_in_use:
                time.sleep(2)
                continue
                
            # Then check health endpoint
            health_response = requests.get("http://localhost:8050/_alive", timeout=5)
            if health_response.status_code == 200:
                content_response = requests.get("http://localhost:8050", timeout=10)
                if "Patient Report" in content_response.text:
                    return True
        except requests.exceptions.RequestException:
            time.sleep(3)
    
    return False
import pandas as pd

def calculate_metabolite_ratios(metabolomic_data):
    """Calculate all metabolite ratios from raw metabolomic data"""
    # Read data
    data = pd.read_excel(metabolomic_data)
    
    # Replace all negative values with 0 in the entire DataFrame
    data = data.map(lambda x: 0 if isinstance(x, (int, float)) and x < 0 else x)
    
    try:
        # Prepare all new columns in a dictionary first
        new_columns = {}
        
        # Acylcarnitines
        new_columns['(C2+C3)/C0'] = (data['C2'] + data['C3']) / data['C0']
        new_columns['CACT Deficiency (NBS)'] = data['C0'] / (data['C16'] + data['C18'])
        new_columns['CPT-1 Deficiency (NBS)'] = (data['C16'] + data['C18']) / data['C0']
        new_columns['CPT-2 Deficiency (NBS)'] = (data['C16'] + data['C18']) / data['C2']
        new_columns['EMA (NBS)'] = data['C4'] / data['C8']
        new_columns['IBD Deficiency (NBS)'] = data['C4'] / data['C2']
        new_columns['IVA (NBS)'] = data['C5'] / data['C2']
        new_columns['LCHAD Deficiency (NBS)'] = data['C16-OH'] / data['C16']
        new_columns['MA (NBS)'] = data['C3'] / data['C2']
        new_columns['MC Deficiency (NBS)'] = data['C16'] / data['C3']
        new_columns['MCAD Deficiency (NBS)'] = data['C8'] / data['C2']
        new_columns['MCKAT Deficiency (NBS)'] = data['C8'] / data['C10']
        new_columns['MMA (NBS)'] = data['C3'] / data['C0']
        new_columns['PA (NBS)'] = data['C3'] / data['C16']
        new_columns['С2/С0'] = data['C2'] / data['C0']
        new_columns['Ratio of Acetylcarnitine to Carnitine'] = data['C2'] / data['C0']
        
        # Calculate sums once to reuse
        sum_AC_OHs = (data['C5-OH'] + data['C14-OH'] + data['C16-1-OH'] + 
                     data['C16-OH'] + data['C18-1-OH'] + data['C18-OH'])
        sum_ACs = (data['C0'] + data['C10'] + data['C10-1'] + data['C10-2'] + 
                  data['C12'] + data['C12-1'] + data['C14'] + data['C14-1'] + 
                  data['C14-2'] + data['C16'] + data['C16-1'] + data['C18'] + 
                  data['C18-1'] + data['C18-2'] + data['C2'] + data['C3'] + 
                  data['C4'] + data['C5'] + data['C5-1'] + data['C5-DC'] + 
                  data['C6'] + data['C6-DC'] + data['C8'] + data['C8-1'])
        
        new_columns['Ratio of AC-OHs to ACs'] = sum_AC_OHs / sum_ACs
        
        СДК = (data['C14'] + data['C14-1'] + data['C14-2'] + data['C14-OH'] + 
               data['C16'] + data['C16-1'] + data['C16-1-OH'] + data['C16-OH'] + 
               data['C18'] + data['C18-1'] + data['C18-1-OH'] + data['C18-2'] + 
               data['C18-OH'])
        ССК = (data['C6'] + data['C6-DC'] + data['C8'] + data['C8-1'] + 
               data['C10'] + data['C10-1'] + data['C10-2'] + data['C12'] + 
               data['C12-1'])
        СКК = (data['C2'] + data['C3'] + data['C4'] + data['C5'] + data['C5-1'] + 
               data['C5-DC'] + data['C5-OH'])
        
        new_columns['СДК'] = СДК
        new_columns['ССК'] = ССК
        new_columns['СКК'] = СКК
        new_columns['Ratio of Medium-Chain to Long-Chain ACs'] = ССК / СДК
        new_columns['Ratio of Short-Chain to Long-Chain ACs'] = СКК / СДК
        new_columns['Ratio of Short-Chain to Medium-Chain ACs'] = СКК / ССК
        new_columns['SBCAD Deficiency (NBS)'] = data['C5'] / data['C0']
        new_columns['SCAD Deficiency (NBS)'] = data['C4'] / data['C3']
        new_columns['Sum of ACs'] = sum_AC_OHs + sum_ACs - data['C0']  # Subtract C0 since it's included in sum_ACs
        new_columns['Sum of ACs + С0'] = sum_AC_OHs + sum_ACs
        new_columns['Sum of ACs/C0'] = (sum_AC_OHs + sum_ACs - data['C0']) / data['C0']
        
        new_columns['Sum of MUFA-ACs'] = (data['C16-1-OH'] + data['C18-1-OH'] + 
                                        data['C10-1'] + data['C12-1'] + 
                                        data['C14-1'] + data['C16-1'] + 
                                        data['C18-1'] + data['C8-1'] + 
                                        data['C5-1'])
        new_columns['Sum of PUFA-ACs'] = data['C10-2'] + data['C14-2'] + data['C18-2']
        new_columns['TFP Deficiency (NBS)'] = data['C16'] / data['C16-OH']
        new_columns['VLCAD Deficiency (NBS)'] = data['C14-1'] / data['C16']
        new_columns['(C6+C8+C10)/C2'] = (data['C6'] + data['C8'] + data['C10']) / data['C2']
        new_columns['2MBG (NBS)'] = data['C5'] / data['C3']
        new_columns['Carnitine Uptake Defect (NBS)'] = (data['C0'] + data['C2'] + data['C3'] + 
                                                       data['C16'] + data['C18'] + 
                                                       data['C18-1']) / data['Citrulline']

        new_columns['C2 / C3'] = data['C2'] / data['C3']
        # NO- and urea cycle
        new_columns['GABR'] = data['Arginine'] / (data['Ornitine'] + data['Citrulline'])
        new_columns['Orn Synthesis'] = data['Ornitine'] / data['Arginine']
        new_columns['AOR'] = data['Arginine'] / data['Ornitine']
        new_columns['ADMA/(Adenosin+Arginine)'] = data['ADMA'] / (data['Adenosin'] + data['Arginine'])
        new_columns["Asymmetrical Arg Methylation"] = data['ADMA'] / data['Arginine']
        new_columns['Symmetrical Arg Methylation'] = data['TotalDMA (SDMA)'] / data['Arginine']
        new_columns['(Arg+HomoArg)/ADMA'] = (data['Arginine'] + data['Homoarginine']) / data['ADMA']
        new_columns['ADMA / NMMA'] = data['ADMA'] / data['NMMA']
        new_columns['NO-Synthase Activity'] = data['Citrulline'] / data['Arginine']
        new_columns['OTC Deficiency (NBS)'] = data['Ornitine'] / data['Citrulline']
        new_columns['Ratio of HArg to ADMA'] = data['Homoarginine'] / data['ADMA']
        new_columns['Ratio of HArg to SDMA'] = data['Homoarginine'] / data['TotalDMA (SDMA)']
        new_columns['Sum of Asym. and Sym. Arg Methylation'] = (data['TotalDMA (SDMA)'] + data['ADMA']) / data['Arginine']
        new_columns['Sum of Dimethylated Arg'] = data['TotalDMA (SDMA)'] + data['ADMA']
        new_columns['Cit Synthesis'] = data['Citrulline'] / data['Ornitine']
        new_columns['CPS Deficiency (NBS)'] = data['Citrulline'] / data['Phenylalanine']
        new_columns['HomoArg Synthesis'] = data['Homoarginine'] / (data['Arginine'] + data['Lysine'])
        new_columns['Ratio of Pro to Cit'] = data['Proline'] / data['Citrulline']

        # Tryptophan metabolism
        new_columns['Kynurenine / Trp'] = data['Kynurenine'] / data['Tryptophan']
        new_columns['Serotonin / Trp'] = data['Serotonin'] / data['Tryptophan']
        new_columns['Trp/(Kyn+QA)'] = data['Tryptophan'] / (data['Kynurenine'] + data['Quinolinic acid'])
        new_columns['Kyn/Quin'] = data['Kynurenine'] / data['Quinolinic acid']
        new_columns['Quin/HIAA'] = data['Quinolinic acid'] / data['HIAA']
        new_columns['Tryptamine / IAA'] = data['Tryptamine'] / data['Indole-3-acetic acid']
        new_columns['Kynurenic acid / Kynurenine'] = data['Kynurenic acid'] / data['Kynurenine']

        # Amino acids
        new_columns['Asn Synthesis'] = data['Asparagine'] / data['Aspartic acid']
        new_columns['Glutamine/Glutamate'] = data['Glutamine'] / data['Glutamic acid']
        new_columns['Gly Synthesis'] = data['Glycine'] / data['Serine']
        new_columns['GSG Index'] = data['Glutamic acid'] / (data['Serine'] + data['Glycine'])
        new_columns['Sum of Aromatic AAs'] = data['Phenylalanine'] + data['Tyrosin']
        new_columns['BCAA'] = data['Summ Leu-Ile'] + data['Valine']
        new_columns['BCAA/AAA'] = (data['Valine'] + data['Summ Leu-Ile']) / (data['Phenylalanine'] + data['Tyrosin'])
        new_columns['Alanine / Valine'] = data['Alanine'] / data['Valine']
        new_columns['DLD (NBS)'] = data['Proline'] / data['Phenylalanine']
        new_columns['MTHFR Deficiency (NBS)'] = data['Methionine'] / data['Phenylalanine']
        
        # Calculate sums once for AA ratios
        sum_non_essential = (data['Alanine'] + data['Arginine'] + data['Asparagine'] + 
                           data['Aspartic acid'] + data['Glutamine'] + 
                           data['Glutamic acid'] + data['Glycine'] + data['Proline'] + 
                           data['Serine'] + data['Tyrosin'])
        sum_essential = (data['Histidine'] + data['Summ Leu-Ile'] + data['Lysine'] + 
                        data['Methionine'] + data['Phenylalanine'] + 
                        data['Threonine'] + data['Tryptophan'] + data['Valine'])
        
        new_columns['Ratio of Non-Essential to Essential AAs'] = sum_non_essential / sum_essential
        new_columns['Sum of AAs'] = sum_non_essential + sum_essential
        new_columns['Sum of Essential Aas'] = sum_essential
        new_columns['Sum of Non-Essential AAs'] = sum_non_essential
        new_columns['Sum of Solely Glucogenic AAs'] = (data['Alanine'] + data['Arginine'] + 
                                                     data['Asparagine'] + data['Aspartic acid'] + 
                                                     data['Glutamine'] + data['Glutamic acid'] + 
                                                     data['Glycine'] + data['Histidine'] + 
                                                     data['Methionine'] + data['Proline'] + 
                                                     data['Serine'] + data['Threonine'] + 
                                                     data['Valine'])
        new_columns['Sum of Solely Ketogenic AAs'] = data['Summ Leu-Ile'] + data['Lysine']
        new_columns['Valinemia (NBS)'] = data['Valine'] / data['Phenylalanine']
        new_columns['Carnosine Synthesis'] = data['Carnosine'] / data['Histidine']
        new_columns['Histamine Synthesis'] = data['Histamine'] / data['Histidine']

        # Betaine_choline metabolism
        new_columns['Betaine/choline'] = data['Betaine'] / data['Choline']
        new_columns['Methionine + Taurine'] = data['Methionine'] + data['Taurine']
        new_columns['DMG / Choline'] = data['DMG'] / data['Choline']
        new_columns['TMAO Synthesis'] = data['TMAO'] / (data['Betaine'] + data['C0'] + data['Choline'])
        new_columns['TMAO Synthesis (direct)'] = data['TMAO'] / data['Choline']
        new_columns['Met Oxidation'] = data['Methionine-Sulfoxide'] / data['Methionine']

        # Vitamins
        new_columns['Riboflavin / Pantothenic'] = data['Riboflavin'] / data['Pantothenic']

        # ADDED: Oncology-specific ratios that were missing
        new_columns['Arg/ADMA'] = data['Arginine'] / data['ADMA']
        new_columns['Arg/Orn+Cit'] = data['Arginine'] / (data['Ornitine'] + data['Citrulline'])
        new_columns['Glutamine/Glutamate'] = data['Glutamine'] / data['Glutamic acid']
        new_columns['Pro/Cit'] = data['Proline'] / data['Citrulline']
        new_columns['Kyn/Trp'] = data['Kynurenine'] / data['Tryptophan']
        new_columns['Trp/Kyn'] = data['Tryptophan'] / data['Kynurenine']
        
        # Arthritis
        new_columns['Phe/Tyr'] = data['Phenylalanine'] / data['Tyrosin']
        new_columns['Glycine/Serine'] = data['Glycine'] / data['Serine']
        # Lungs
        new_columns['C4 / C2'] = data['C4'] / data['C2']
        new_columns['Valine / Alanine'] = data['Valine'] / data['Alanine']
        # Liver
        new_columns['C0/(C16+C18)'] = data['C0'] / (data['C16'] + data['C18'])
        new_columns['(Leu+IsL)/(C3+С5+С5-1+C5-DC)'] = (data['Summ Leu-Ile']) / (data['C3'] + data['C5'] + data['C5-1'] + data['C5-DC'])
        new_columns['Val/C4'] = data['Valine'] / data['C4']

        # Convert the dictionary to a DataFrame and concatenate with original data
        new_data = pd.DataFrame(new_columns)
        data = pd.concat([data, new_data], axis=1)

        # Drop Group column if it exists
        if 'Group' in data.columns:
            data = data.drop('Group', axis=1)

        return data

    except Exception as e:
        print(f"Error calculating metabolite ratios: {str(e)}")
        return None

def prepare_final_dataframe(risk_params_data, metabolomic_data_with_ratios):
    # Load the data
    risk_params = pd.read_excel(risk_params_data)
    metabolic_data = pd.read_excel(metabolomic_data_with_ratios)
    
    # Get values for each marker from metabolomic data
    values_conc = []
    for metabolite in risk_params['Маркер / Соотношение']:
        try:
            value = metabolic_data.loc[0, metabolite]
            # Handle negative and infinite values
            if pd.isna(value) or np.isinf(value):
                values_conc.append(np.nan)
            elif value < 0:
                values_conc.append(0)
            else:
                values_conc.append(value)
        except KeyError:
            values_conc.append(np.nan)  # Handle missing metabolites
    
    risk_params['Patient'] = values_conc
    
    # Drop rows with infinite or NaN values in Patient column
    risk_params = risk_params[~risk_params['Patient'].isin([np.inf, -np.inf]) & 
                  ~risk_params['Patient'].isna()].copy()
    
    subgroup_list=[]
    subgroup_scores=[]
    categories=risk_params['Категория'].unique()
    for category in categories:
        data_category=risk_params[risk_params['Категория']==category]
        metabolite_inputs=[]
        for index, row in data_category.iterrows():
            metabolite_input=0
            weight=data_category.loc[index, 'веса']
            patient_value=data_category.loc[index, 'Patient']
            norm_1=data_category.loc[index, 'norm_1']
            norm_2=data_category.loc[index, 'norm_2']
            risk_1=data_category.loc[index, 'High_risk_1']
            risk_2=data_category.loc[index, 'High_risk_2']
            metab_group=data_category.loc[index, 'Группа_метаб']
            if metab_group==0:
                if norm_1<=patient_value<=norm_2:
                    metabolite_input=0
                elif risk_1<=patient_value<norm_1 or norm_2<patient_value<=risk_2:
                    metabolite_input=1
                else:
                    metabolite_input=2
            elif metab_group==1:
                if patient_value<=norm_2:
                    metabolite_input=0
                elif norm_2<patient_value<=risk_2:
                    metabolite_input=1
                else:
                    metabolite_input=2
            else:
                if norm_1<=patient_value:
                    metabolite_input=0
                elif risk_1<=patient_value<norm_1:
                    metabolite_input=1
                else:
                    metabolite_input=2
            metabolite_inputs.append(metabolite_input*weight)
            max_score=data_category['веса'].sum()*2
            subgroup_score=sum(metabolite_inputs)/max_score*100
        subgroup_scores.append(subgroup_score)
        subgroup_list.append(category)
    
    # in risk_params make column Subgroup_score and for each row where [Категория] is in subgroup_list, [Subgroup_score] is subgroup_scores[subgroup_list.index([Категория])]
    risk_params['Subgroup_score'] = np.nan
    for index, row in risk_params.iterrows():
        if row['Категория'] in subgroup_list:
            risk_params.loc[index, 'Subgroup_score'] = subgroup_scores[subgroup_list.index(row['Категория'])]
    
    # in risk_params make column Subgroup_score and for each row where [Категория] is in subgroup_list, [Subgroup_score] is subgroup_scores[subgroup_list.index([Категория])]
    risk_params['Subgroup_score'] = np.nan
    for index, row in risk_params.iterrows():
        if row['Категория'] in subgroup_list:
            risk_params.loc[index, 'Subgroup_score'] = subgroup_scores[subgroup_list.index(row['Категория'])]
    return risk_params


def probability_to_score(prob, threshold):
    prob = min(max(prob, 0), 1)
    if prob < threshold:
        score = 5 * prob / threshold
    else:
        score = 5 + 5 * (prob - threshold) / (1 - threshold)
    return 10- round(score, 0)



def calculate_risks(risk_params_data, metabolic_data_with_ratios):
    """
    Calculate combined risks using:
    - ML models for specific groups (Onco, CVD, Liver, Pulmo, RA)
    - Parameter-based method for other groups
    Returns DataFrame with columns: ['Группа риска', 'Риск-скор', 'Метод оценки']
    """
    # Группы, для которых используем только ML модели
    ml_only_groups = {
        "Оценка пролиферативных процессов",
        "Состояние сердечно-сосудистой системы",
        "Состояние функции печени",
        "Состояние дыхательной системы",
        "Состояние иммунного метаболического баланса"
    }
    
        # --- Part 1: Validate input data indices ---
    def ensure_unique_index(df, df_name):
        if not df.index.is_unique:
            print(f"Предупреждение: Найдены дубликаты в индексе {df_name}. Сбрасываю дубликат.")
            return df[~df.index.duplicated(keep='first')]
        return df
    
    metabolic_data_with_ratios = ensure_unique_index(metabolic_data_with_ratios, "metabolic_data_with_ratios")
    risk_params_data = ensure_unique_index(risk_params_data, "risk_params_data")

    # --- Part 1: Model-based risk calculation ---
    models_info = {
        "Оценка пролиферативных процессов": {
            "model_path": os.path.join(os.path.dirname(__file__), "models", "Onco_healthy_RF_0907.pkl"),
            "features": metabolites_selected_onco
        },
        "Состояние сердечно-сосудистой системы": {
            "model_path": os.path.join(os.path.dirname(__file__), "models", "CVD_healthy_RF_0907.pkl"),
            "features": metabolites_selected_CVD
        },
        "Состояние функции печени": {
            "model_path": os.path.join(os.path.dirname(__file__), "models", "Liver_healthy_RF_0907.pkl"),
            "features": metabolites_selected_Liv
        },
        "Состояние дыхательной системы": {
            "model_path": os.path.join(os.path.dirname(__file__), "models", "Pulmo_healthy_RF_0907.pkl"),
            "features": metabolites_selected_PULM
        },
        "Состояние иммунного метаболического баланса": {
            "model_path": os.path.join(os.path.dirname(__file__), "models", "RA_healthy_RF_0907.pkl"),
            "features": metabolites_selected_RA
        }
    }

    # Initialize results
    results = []

    # Read metabolic data
    row = metabolic_data_with_ratios.iloc[0]  # Assuming single row input

    for idx, row in metabolic_data_with_ratios.iterrows():
        for disease, info in models_info.items():
            try:
                model = joblib.load(info["model_path"])
                threshold = thresholds[disease]
                X_row = pd.DataFrame([row[info["features"]]], columns=info["features"])
                # Clean data - replace inf and large values
                X_row = X_row.replace([np.inf, -np.inf], np.nan)
                X_row = X_row.fillna(0)
                X_row = X_row.clip(-1e10, 1e10)
                
                # Convert to float32 to match typical model expectations
                X_row = X_row.astype(np.float32)
                pred_proba = model.predict_proba(X_row)[0][1]
                score = probability_to_score(pred_proba, threshold)

                results.append({
                    "Группа риска": disease,
                    "Риск-скор": score ,
                    "Метод оценки": "ML модель"
                })

            except Exception as e:
                print(f"Ошибка в модели {disease}: {e}")
                results.append({
                    "Группа риска": disease,
                    "Риск-скор": None,
                    "Метод оценки": "ML модель"
                })
       

    # 2. Process other groups with parameter-based method

    
    # Filter out ML-only groups
    other_groups = set(risk_params_data['Группа_риска'].unique()) - ml_only_groups
    
    if other_groups:
        # Prepare parameter risk_params_data
        values_conc = []
        for metabolite in risk_params_data['Маркер / Соотношение']:
            try:
                value = row[metabolite]
                if pd.isna(value) or np.isinf(value):
                    values_conc.append(np.nan)
                elif value < 0:
                    values_conc.append(0)
                else:
                    values_conc.append(value)
            except KeyError:
                values_conc.append(np.nan)
        
        risk_params_data['Patient'] = values_conc
        risk_params_data = risk_params_data[~risk_params_data['Patient'].isin([np.inf, -np.inf]) & ~risk_params_data['Patient'].isna()].copy()
        
        # Calculate scores for remaining groups
        for risk_group in other_groups:
            risk_params_data_group = risk_params_data[risk_params_data['Группа_риска'] == risk_group]
            if len(risk_params_data_group) == 0:
                continue
                
            metabolite_inputs = []
            for index, row_group in risk_params_data_group.iterrows():
                metabolite_input = 0
                weight = row_group['веса']
                patient_value = row_group['Patient']
                norm_1 = row_group['norm_1']
                norm_2 = row_group['norm_2']
                risk_1 = row_group['High_risk_1']
                risk_2 = row_group['High_risk_2']
                metab_group = row_group['Группа_метаб']
                
                if metab_group == 0:
                    if norm_1 <= patient_value <= norm_2:
                        metabolite_input = 0
                    elif risk_1 <= patient_value < norm_1 or norm_2 < patient_value <= risk_2:
                        metabolite_input = 1
                    else:
                        metabolite_input = 2
                elif metab_group == 1:
                    if patient_value <= norm_2:
                        metabolite_input = 0
                    elif norm_2 < patient_value <= risk_2:
                        metabolite_input = 1
                    else:
                        metabolite_input = 2
                else:
                    if norm_1 <= patient_value:
                        metabolite_input = 0
                    elif risk_1 <= patient_value < norm_1:
                        metabolite_input = 1
                    else:
                        metabolite_input = 2
                
                metabolite_inputs.append(metabolite_input * weight)
            
            max_score = risk_params_data_group['веса'].sum() * 2
            group_score = 10 - sum(metabolite_inputs) / max_score * 10
            results.append({
                "Группа риска": risk_group,
                "Риск-скор": np.round(group_score, 0),
                "Метод оценки": "Параметры"
            })

    # Create final DataFrame
    result_df = pd.DataFrame(results)
    
    # Sort by risk score (descending) and group name
    result_df.sort_values(['Группа риска'], ascending=True, inplace=True)
    
    return result_df[['Группа риска', 'Риск-скор', 'Метод оценки']].reset_index(drop=True)



def generate_pdf_report(patient_info, risk_scores_path, risk_params_exp_path, metabolomic_data_with_ratios_path, output_dir):
    """Generate PDF report with proper error handling"""
    dash_process = None
    driver = None
    
    try:
        
        # Clean up any existing Dash instance
        kill_dash_app(8050)
        time.sleep(2)
        
        # Start new Dash process with all needed data
        dash_command = [
            sys.executable,
            "main.py",
            "--name", patient_info['name'],
            "--age", str(patient_info['age']),
            "--gender", patient_info['gender'],
            "--date", patient_info['date'],
            "--risk_scores", risk_scores_path,
            "--risk_params", risk_params_exp_path,
            "--metabolomic_data", metabolomic_data_with_ratios_path,
        ]
        
        dash_process = subprocess.Popen(
            dash_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for Dash app to be ready
        if not wait_for_dash_app():
            raise Exception("Dash app failed to start or load content")
        
        # Generate PDF
        driver = setup_chrome_driver()
        driver.get("http://localhost:8050")
        time.sleep(5)
        
        pdf_path = os.path.join(output_dir, "report.pdf")
        print_settings = {
            "printBackground": True,
            "paperWidth": 8.3,
            "paperHeight": 11.7,
            "scale": 1.0
        }
        
        pdf_data = driver.execute_cdp_cmd("Page.printToPDF", print_settings)
        with open(pdf_path, "wb") as f:
            f.write(base64.b64decode(pdf_data['data']))
        
        return pdf_path
        
    except Exception as e:
        st.error(f"Report generation failed: {str(e)}")
        logging.error(f"Report generation error: {str(e)}")
        return None
        
    finally:
        # Cleanup resources
        try:
            if driver:
                driver.quit()
        except:
            pass
            
        if dash_process:
            try:
                dash_process.terminate()
                dash_process.wait(timeout=5)
            except:
                try:
                    dash_process.kill()
                except:
                    pass
        
        kill_dash_app(8050)

def wait_for_dash_app(timeout=30):
    """Check if Dash app is ready"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get("http://localhost:8050/_alive", timeout=5)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            time.sleep(2)
    return False


def generate_pdf_file(driver, output_dir):
    """Generate the PDF file with proper settings"""
    print_settings = {
        "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local",
            "account": "",
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2,
        "isHeaderFooterEnabled": False,
        "isLandscapeEnabled": True,
        'printBackground': True,
        'paperHeight': 11.7,
        'paperWidth': 8.3,
        'scale': 1.0
    }
    
    pdf_data = driver.execute_cdp_cmd("Page.printToPDF", print_settings)
    pdf_path = os.path.join(output_dir, "report.pdf")
    
    with open(pdf_path, "wb") as f:
        f.write(base64.b64decode(pdf_data['data']))
    
    return pdf_path

def log_errors(process):
    """Log any errors from the subprocess"""
    if process:
        try:
            stdout, stderr = process.communicate(timeout=5)
            if stdout:
                logging.error(f"Dash stdout: {stdout}")
            if stderr:
                logging.error(f"Dash stderr: {stderr}")
        except subprocess.TimeoutExpired:
            logging.error("Process did not terminate when logging errors")

def cleanup_resources(driver, process):
    """Clean up all resources in proper order"""
    # Close driver first
    if driver:
        try:
            driver.quit()
        except:
            pass
    
    # Then terminate process
    if process:
        try:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        except:
            pass
    
    # Final check to ensure Dash is gone
    kill_dash_app(8050)

def validate_inputs(name, file1, file2):
    """Validate user inputs before processing"""
    if not name.strip():
        st.error("Please enter a valid patient name")
        return False
    if not file1 or not file2:
        st.error("Please upload both data files")
        return False
    
    return True



def main():
    st.set_page_config(
        page_title="Отчет Metaboscan",
        page_icon="🏥",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    with st.form("report_form"):
        st.header("Информация о пациенте")
        
        cols = st.columns(3)
        with cols[0]:
            name = st.text_input("Полное имя (ФИО)", placeholder="Иванов Иван Иванович")
        with cols[1]:
            age = st.number_input("Возраст", min_value=0, max_value=120, value=47)
        with cols[2]:
            gender = st.selectbox("Пол", ("М", "Ж"), index=0)
        
        date = st.date_input("Дата отчета", datetime.now(), format="DD.MM.YYYY")
        
        st.header("Загрузите данные")
        risk_params = st.file_uploader(
            "Параметры риска (Excel)",
            type=["xlsx", "xls", "xlsm"],
            key="risk_params"
        )
        metabolomic_data = st.file_uploader(
            "Метаболомный профиль пациента (Excel)",
            type=["xlsx", "xls"],
            key="metabolomic_data"
        )
        
        submitted = st.form_submit_button("Сформировать отчет", type="primary")
    
    if submitted and validate_inputs(name, risk_params, metabolomic_data):
        patient_info = {
            "name": name.strip(),
            "age": age,
            "date": date.strftime("%d.%m.%Y"),
            "gender": gender,
        }
        
        with st.spinner("🔬 Читаем данные и генерируем отчет. Это займет не больше минуты..."):
            with tempfile.TemporaryDirectory() as temp_dir:
                try:
                    # Save uploaded files temporarily
                    risk_params_path = os.path.join(temp_dir, "risk_params.xlsx")
                    with open(risk_params_path, "wb") as f:
                        f.write(risk_params.getbuffer())

                    # Calculate ratios and risks
                    metabolomic_data_with_ratios = calculate_metabolite_ratios(metabolomic_data)
                    metabolomic_data_with_ratios_path = os.path.join(temp_dir, "metabolomic_data.xlsx")
                    metabolomic_data_with_ratios.to_excel(metabolomic_data_with_ratios_path, index=False)
                    
                    risk_params_exp = prepare_final_dataframe(risk_params_path, metabolomic_data_with_ratios_path)
                    risk_params_exp_path = os.path.join(temp_dir, "risk_exp_params.xlsx")
                    risk_params_exp.to_excel(risk_params_exp_path, index=False)
                        
                    risk_scores = calculate_risks(risk_params_exp, metabolomic_data_with_ratios)
                    st.write(pd.read_excel(risk_params_exp_path))
                    st.write(risk_scores)
                    # Save risk scores as excel in temp_dir
                    risk_scores_path = os.path.join(temp_dir, "risk_scores.xlsx")
                    risk_scores.to_excel(risk_scores_path, index=False)

                    # Generate report
                    report_path = generate_pdf_report(
                        patient_info,
                        risk_scores_path,
                        risk_params_exp_path,
                        metabolomic_data_with_ratios_path,
                        temp_dir
                    )
                    
                    if report_path and os.path.exists(report_path):
                        st.success("✅ Отчет успешно сформирован!")
                        with open(report_path, "rb") as f:
                            st.download_button(
                                label="📥 Скачать отчет",
                                data=f.read(),
                                file_name=f"Report_{name.replace(' ', '_')}_{date.strftime('%Y%m%d')}.pdf",
                                mime="application/pdf",
                            )
                        
                        # with st.expander("📄 Report Preview", expanded=True):
                        #     base64_pdf = base64.b64encode(open(report_path, "rb").read()).decode('utf-8')
                        #     st.markdown(
                        #         f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" style="border:none;"></iframe>',
                        #         unsafe_allow_html=True
                                
                        #     )
                        
                    else:
                        st.error("Failed to generate report. Please check the console for errors.")
                        
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()