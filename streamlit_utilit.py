import pandas as pd
import numpy as np
import os
import joblib
import time
import base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service #для корректной работы на сервере
import subprocess
import sys
import logging
import requests
import psutil
from glob import glob



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
        new_columns['GSG_index'] = data['Glutamic acid'] / (data['Serine'] + data['Glycine'])
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
        new_columns['(C16+C18)/C2'] = (data['C16'] + data['C18']) / data['C2']
        new_columns['C3 / C0'] = data['C3'] / data['C0']

        # Convert the dictionary to a DataFrame
        new_data = pd.DataFrame(new_columns)

        # Get columns that exist in both DataFrames
        common_cols = data.columns.intersection(new_data.columns)

        # For overlapping columns, fill NaN in original data with new_data values
        for col in common_cols:
            data[col] = data[col].fillna(new_data[col])

        # Get columns that only exist in new_data
        new_cols_only = new_data.columns.difference(data.columns)

        # Add the new columns
        data = pd.concat([data, new_data[new_cols_only]], axis=1)

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
        score = 4 * prob / threshold
    else:
        score = 4 + 4 * (prob - threshold) / (1 - threshold)
    return 10- round(score, 0)

def classify_onco_pipeline(X_row, onco_model, onco_liver_model):
    """
    Two-stage oncology prediction pipeline
    Returns: (final_probability, final_score, final_diagnosis, source)
    """
    # Configuration
    onco_threshold = 0.6
    liver_threshold = 0.45
    
    # Get features from models
    onco_features = onco_model.feature_names_in_
    liver_features = onco_liver_model.feature_names_in_
    
    # First stage prediction
    X_onco = pd.DataFrame([X_row[onco_features]], columns=onco_features)
    X_onco = X_onco.replace([np.inf, -np.inf], np.nan).fillna(0).clip(-1e10, 1e10).astype(np.float32)
    
    onco_proba = onco_model.predict_proba(X_onco)[0][0]  # class 0 = Onco
    initial_diagnosis = "Onco" if onco_proba >= onco_threshold else "Здоров"
    
    # If first stage is negative, return those results
    if initial_diagnosis == "Здоров":
        return (onco_proba, probability_to_score(onco_proba, onco_threshold), 
                initial_diagnosis, "onco-control модель")
    
    # Second stage prediction
    X_liver = pd.DataFrame([X_row[liver_features]], columns=liver_features)
    X_liver = X_liver.replace([np.inf, -np.inf], np.nan).fillna(0).clip(-1e10, 1e10).astype(np.float32)
    
    liver_proba = onco_liver_model.predict_proba(X_liver)[0][0]  # class 0 = Onco
    final_diagnosis = "Onco" if liver_proba >= liver_threshold else "Здоров"
    
    return (liver_proba, probability_to_score(liver_proba, liver_threshold), 
            final_diagnosis, "onco-liver модель")


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
    
    # First, get all .pkl files in the ONCO folder
    onco_files = glob(os.path.join(os.path.dirname(__file__), "models", "ONCO", "*.pkl"))

    # Separate the files based on their names
    onco_model_path = None
    onco_liver_model_path = None

    for file_path in onco_files:
        if 'liver' in os.path.basename(file_path).lower():
            onco_liver_model_path = file_path
        else:
            onco_model_path = file_path

    # Verify we found both models
    if not onco_model_path or not onco_liver_model_path:
        raise FileNotFoundError(
            "Need both regular and liver models in ONCO folder. "
            f"Found files: {onco_files}"
        )



    # --- Part 1: Model-based risk calculation ---
    models_info = {
        "Оценка пролиферативных процессов": {
            "onco_model_path": onco_model_path,
            "liver_model_path": onco_liver_model_path,
        },
        "Состояние сердечно-сосудистой системы": {
            "model_path": glob(os.path.join(os.path.dirname(__file__), "models", "CVD", "*.pkl"))[0]
        },
        "Состояние функции печени": {
            "model_path": glob(os.path.join(os.path.dirname(__file__), "models", "LIVER", "*.pkl"))[0]
        },
        "Состояние дыхательной системы": {
            "model_path": glob(os.path.join(os.path.dirname(__file__), "models", "PULMO", "*.pkl"))[0]
        },
        "Состояние иммунного метаболического баланса": {
            "model_path": glob(os.path.join(os.path.dirname(__file__), "models", "RA", "*.pkl"))[0]
        }
    }
    
    thresholds = {
            "Состояние сердечно-сосудистой системы": 0.48,
            "Состояние функции печени": 0.45,
            "Состояние дыхательной системы": 0.58,
            "Состояние иммунного метаболического баланса": 0.65
        }

    # Initialize results
    results = []

    # Process each row of metabolic data
    for idx, row in metabolic_data_with_ratios.iterrows():
        # Oncology-specific processing
        if "Оценка пролиферативных процессов" in models_info:
            onco_info = models_info["Оценка пролиферативных процессов"]
            try:
                # Load models if not already loaded
                if "onco_model" not in onco_info:
                    onco_info["onco_model"] = joblib.load(onco_info["onco_model_path"])
                if "liver_model" not in onco_info:
                    onco_info["liver_model"] = joblib.load(onco_info["liver_model_path"])
                
                # Run two-stage prediction
                prob, score, diagnosis, source = classify_onco_pipeline(
                    row,
                    onco_info["onco_model"],
                    onco_info["liver_model"],
                )
                
                results.append({
                    "Группа риска": "Оценка пролиферативных процессов",
                    "Риск-скор": score,
                    "Метод оценки": source,
                    "Диагноз": diagnosis,
                    "Вероятность": prob
                })
                
            except Exception as e:
                print(f"Ошибка в онко-модели: {e}")
                results.append({
                    "Группа риска": "Оценка пролиферативных процессов",
                    "Риск-скор": None,
                    "Метод оценки": f"ML модель (ошибка: {str(e)})",
                    "Диагноз": None,
                    "Вероятность": None
                })
        
        # Process other models (CVD, Liver, etc.)
        for disease, info in models_info.items():
            if disease == "Оценка пролиферативных процессов":
                continue  # Already processed
                
            try:
                # Load model if not already loaded
                if "model" not in info:
                    info["model"] = joblib.load(info["model_path"])
                    info["features"] = info["model"].feature_names_in_
                
                # Prepare input data
                X_row = pd.DataFrame([row[info["features"]]], columns=info["features"])
                X_row = X_row.replace([np.inf, -np.inf], np.nan).fillna(0).clip(-1e10, 1e10)
                X_row = X_row.astype(np.float32)
                
                # Make prediction
                pred_proba = info["model"].predict_proba(X_row)[0][1]
                score = probability_to_score(pred_proba, thresholds.get(disease, 0.5))

                results.append({
                    "Группа риска": disease,
                    "Риск-скор": score,
                    "Метод оценки": "ML модель",
                    "Диагноз": None,
                    "Вероятность": pred_proba
                })

            except Exception as e:
                print(f"Ошибка в модели {disease}: {str(e)}")
                results.append({
                    "Группа риска": disease,
                    "Риск-скор": None,
                    "Метод оценки": f"ML модель (ошибка: {str(e)})"
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



# НЕ ТРОГАТЬ, НУЖНО ДЛЯ ГЕНЕРАЦИИ ОТЧЕТА!!!
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='report_generator.log'
)

def setup_chrome_driver():
    """Configure Chrome WebDriver with extended timeout settings"""
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/chromium" #для корректной работы на сервере
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    # Improved font configuration for Docker/Linux
    chrome_options.add_argument("--disable-font-subpixel-positioning")
    chrome_options.add_argument("--disable-remote-fonts")
    chrome_options.add_argument("--force-color-profile=srgb")
    
    # Set default fonts
    font_prefs = {
        "webkit.webprefs.default_fixed_font_size": 13,
        "webkit.webprefs.default_font_size": 16,
        "webkit.webprefs.minimum_font_size": 12,
        "webkit.webprefs.minimum_logical_font_size": 12,
        "webkit.webprefs.default_font_family": "Calibri",
        "webkit.webprefs.sansserif_font_family": "Calibri",
        "webkit.webprefs.serif_font_family": "Times New Roman",
        "webkit.webprefs.fixed_font_family": "Consolas"
    }
    chrome_options.add_experimental_option("prefs", font_prefs)
    
    service = Service("/usr/bin/chromedriver") #для корректной работы на сервере
    driver = webdriver.Chrome(service=service, options=chrome_options) #для корректной работы на сервере
    
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

