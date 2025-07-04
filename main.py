from dash import Dash, html, dash_table
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from typing import List
import matplotlib.colors as mcolors
import os
import pandas as pd

app_pid = os.getpid()

name = 'Иванов Иван Иванович'
date = '21.07.2023'
age = 47
gender = 'М'

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

def get_value_1(metabolite_data):
    """
    Processes the parsed metabolite data to extract specific values and rounds to 1 decimal place
    """
    ref_1 = ['43.5 - 91.7', '36.8 - 98.3', '96.1 - 174.2']
    value_1 = []
    
    try:
        # Get Phenylalanine and round to 1 decimal
        phenylalanine = round(float(metabolite_data.get('Phenylalanine', 0)), 1)
        value_1.append(phenylalanine)
        
        # Get Tyrosin (handle different spellings) and round to 1 decimal
        tyrosin = round(float(metabolite_data.get('Tyrosin', 0)), 1)
        value_1.append(tyrosin)
        
        # Calculate indexAAAs and round to 1 decimal
        indexAAAs = round(phenylalanine + tyrosin, 1)
        value_1.append(indexAAAs)
        
        return ref_1, value_1
        
    except Exception as e:
        print(f"Error in processing: {e}")
        # Return rounded default values
        return ref_1, [0.0, 0.0, 0.0]

def get_value_2(metabolite_data):
    """
    Processes the parsed metabolite data to extract specific values and rounds to 1 decimal place
    """
    ref_2 = ['115.2 - 290.0','137.0 - 288.5','299.7 - 531.0','1.82 - 4.27']
    value_2 = []
    
    try:
        Summ_Leu_Ile = round(float(metabolite_data.get('Summ Leu-Ile', 0)), 1)
        value_2.append(Summ_Leu_Ile)
        
        valine= round(float(metabolite_data.get('Valine', 0)), 1)
        value_2.append(valine)
        
        index_BCAA = round(Summ_Leu_Ile + valine, 1)
        value_2.append(index_BCAA)
        
        # Get Phenylalanine and round to 1 decimal
        phenylalanine = round(float(metabolite_data.get('Phenylalanine', 0)), 1)
        # Get Tyrosin (handle different spellings) and round to 1 decimal
        tyrosin = round(float(metabolite_data.get('Tyrosin', 1) or metabolite_data.get('Tyrosine', 1)), 1)

        # Calculate indexAAAs and round to 1 decimal
        indexAAAs = round(phenylalanine + tyrosin, 1)
        
        # Index fisher is ratio
        index_fisher = round(index_BCAA / indexAAAs  , 2)
        value_2.append(index_fisher)
        
        
        return ref_2, value_2
        
    except Exception as e:
        print(f"Error in processing: {e}")
        # Return rounded default values
        return ref_2, [0.0, 0.0, 0.0]
def get_value_3(metabolite_data):
    """
    Processes the parsed metabolite data to extract specific values and rounds to 1 decimal place
    """
    ref_3 = ['59.9 - 148.4','2.18 - 45.57','55.1 - 136.5','< 0.46','137.7 - 350.8','0.15 - 0.68','78.3 - 216.9','161.7 - 298.0','43.5 - 250.0','196.1 - 405.7','0.44 - 3.66','0.08 - 0.66']
    value_3 = []
    
    try:
        # Histidine
        histidine = round(float(metabolite_data.get('Histidine', 0)), 1)
        value_3.append(histidine)
        metilhistidine = round(float(metabolite_data.get('Methylhistidine', 0)), 2)
        value_3.append(metilhistidine)
        treonine = round(float(metabolite_data.get('Threonine', 0)), 1)
        value_3.append(treonine)
        carnosine = round(float(metabolite_data.get('Carnosine', 0)), 2)
        value_3.append(carnosine)
        glycine = round(float(metabolite_data.get('Glycine', 0)), 1)
        value_3.append(glycine)
        dymetilglycine = round(float(metabolite_data.get('DMG', 0)), 2)
        value_3.append(dymetilglycine)
        serine = round(float(metabolite_data.get('Serine', 0)), 1)
        value_3.append(serine)
        Lysine= round(float(metabolite_data.get('Lysine', 0)), 1)
        value_3.append(Lysine)
        glutaminic_acid = round(float(metabolite_data.get('Glutamic acid', 0)), 1)
        value_3.append(glutaminic_acid)
        glutamine = round(float(metabolite_data.get('Glutamine', 0)), 1)
        value_3.append(glutamine)
        indexGLN_GLU = round(glutamine / glutaminic_acid, 2)
        value_3.append(indexGLN_GLU)
        indexGlu_SerAndGly = round(glutaminic_acid / (serine + glycine), 2)
        value_3.append(indexGlu_SerAndGly)
        
        return ref_3, value_3
        
    except Exception as e:
        print(f"Error in processing: {e}")
        # Return rounded default values
        return ref_3, [0.0, 0.0, 0.0]

def get_value_4(metabolite_data):
    """
    Processes the parsed metabolite data to extract specific values and rounds to 1 decimal place
    """
    ref_4 = ['17.4 - 47.4','0.09 - 0.97','27.7 - 145.8','28.6 - 82.7','5.68 - 19.88','0.26 - 7.17','1.14 - 7.57']
    value_4 = []
    
    try:
        # metionine
        methionine = round(float(metabolite_data.get('Methionine', 0)), 1)
        value_4.append(methionine)
        Methionine_Sulfoxide = round(float(metabolite_data.get('Methionine-Sulfoxide', 2)), 1)
        value_4.append(Methionine_Sulfoxide)
        Taurine = round(float(metabolite_data.get('Taurine', 0)), 1)
        value_4.append(Taurine)
        Betaine = round(float(metabolite_data.get('Betaine', 0)), 1)
        value_4.append(Betaine)
        Choline = round(float(metabolite_data.get('Choline', 0)), 2)
        value_4.append(Choline)
        TMAO = round(float(metabolite_data.get('TMAO', 0)), 2)
        value_4.append(TMAO)
        indexBet_Chl= round(Betaine / Choline, 2)
        value_4.append(indexBet_Chl)
        return ref_4, value_4
        
    except Exception as e:
        print(f"Error in processing: {e}")
        # Return rounded default values
        return ref_4, [0.0, 0.0, 0.0]

def get_value_5(metabolite_data):
    """
    Processes the parsed metabolite data to extract specific values and rounds to 1 decimal place
    """
    ref_5 = ['36.2 - 72.9','1.01 - 2.41','0.01 - 0.05','0.14 - 0.67','0.13 - 0.64','< 0.04','0.02 - 0.08','0.98 - 7.90']
    value_5 = []
    
    try:
        #Tryptophan
        tryptophan = round(float(metabolite_data.get('Tryptophan', 0)), 1)
        value_5.append(tryptophan)
        kynurenine = round(float(metabolite_data.get('Kynurenine', 0)), 2)
        value_5.append(kynurenine)
        indexKyn_Try = round(round(float(metabolite_data.get('Kynurenine', 0)), 3)/ round(float(metabolite_data.get('Tryptophan', 0)), 3), 3)
        value_5.append(indexKyn_Try)
        antranillic_acid = round(float(metabolite_data.get('Antranillic acid', 0)), 4)
        value_5.append(antranillic_acid)
        quinolinic_acid = round(float(metabolite_data.get('Quinolinic acid', 0)), 2)
        value_5.append(quinolinic_acid)
        Xanthurenic_acid = round(float(metabolite_data.get('Xanthurenic acid', 0)), 3)
        value_5.append(Xanthurenic_acid)
        Kynurenic_acid = round(float(metabolite_data.get('Kynurenic acid', 0)), 3)
        value_5.append(Kynurenic_acid)
        indexKyn_Qnl= round(Kynurenic_acid / quinolinic_acid, 2)
        value_5.append(indexKyn_Qnl)
        return ref_5, value_5
        
    except Exception as e:
        print(f"Error in processing: {e}")
        # Return rounded default values
        return ref_5, [0.0, 0.0, 0.0]
    
def get_value_6(metabolite_data):
    """
    Processes the parsed metabolite data to extract specific values and rounds to 1 decimal place
    """
    ref_6 = ['0.02 - 1.45','< 0.09','< 0.26','0.08 - 0.25']
    value_6 = []
    
    try:
        # Serotonine
        serotonine = round(float(metabolite_data.get('Serotonin', 0)), 2)
        value_6.append(serotonine)
        hiaa = round(float(metabolite_data.get('HIAA', 0)), 2)
        value_6.append(hiaa)
        Quinolinic_acid = round(float(metabolite_data.get('Quinolinic acid', 0)), 2)
        indexQnl_hiaa = round(hiaa / Quinolinic_acid, 1)
        value_6.append(indexQnl_hiaa)
        hydroxy_tryptophan = round(float(metabolite_data.get('5-hydroxytryptophan', 0)), 2)
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
        indole_acetic_acid = round(float(metabolite_data.get('Indole-3-acetic acid', 0)), 2)
        value_7.append(indole_acetic_acid)
        indole_lactic_acid = round(float(metabolite_data.get('Indole-3-lactic acid', 0)), 3)
        value_7.append(indole_lactic_acid)
        indole_carboxaldehyde = round(float(metabolite_data.get('Indole-3-carboxaldehyde', 0)), 2)
        value_7.append(indole_carboxaldehyde)
        indole_propionic_acid = round(float(metabolite_data.get('Indole-3-propionic acid', 0)), 2)
        value_7.append(indole_propionic_acid)
        indole_3_butyric = round(float(metabolite_data.get('Indole-3-butyric acid', 0)), 3)
        value_7.append(indole_3_butyric)
        tryptamine = round(float(metabolite_data.get('Tryptamine', 0)), 3)
        value_7.append(tryptamine)
        return ref_7, value_7
        
    except Exception as e:
        print(f"Error in processing: {e}")
        
        return ref_7, [0.0, 0.0, 0.0]

def get_value_8(metabolite_data):
    """
    Processes the parsed metabolite data to extract specific values and rounds to 1 decimal place
    """
    ref_8 = ['106.7 - 358.0','3.16 - 14.09','0.29 - 1.01','0.28 - 1.04','1.31 - 6.42','45.9 - 164.7','26.5 - 58.3','31.1 - 115.8','15.6 - 33.7','13.8 - 101.3','0.29 - 1.53','0.28 - 2.59','0.07 - 0.79','16.8 - 61.8', '< 0.14']
    value_8 = []
    
    try:
        # Proline
        proline = round(float(metabolite_data.get('Proline', 0)), 1)
        value_8.append(proline)
        hydroxyproline = round(float(metabolite_data.get('Hydroxyproline', 0)), 2)
        value_8.append(hydroxyproline)
        adma = round(float(metabolite_data.get('ADMA', 0)), 2)
        value_8.append(adma)
        sdma = round(float(metabolite_data.get('TotalDMA (SDMA)', 0)), 2)
        value_8.append(sdma)
        homoarginine = round(float(metabolite_data.get('Homoarginine', 0)), 2)
        value_8.append(homoarginine)
        arginine = round(float(metabolite_data.get('Arginine', 0)), 1)
        value_8.append(arginine)
        Citrulline = round(float(metabolite_data.get('Citrulline', 0)), 1)
        value_8.append(Citrulline)
        Orintine = round(float(metabolite_data.get('Ornitine', 0)), 1)
        value_8.append(Orintine)
        asparagine = round(float(metabolite_data.get('Asparagine', 0)), 1)
        value_8.append(asparagine)
        asparagine_acid = round(float(metabolite_data.get('Aspartic acid', 0)), 1)
        value_8.append(asparagine_acid)
        index_gabr = round(arginine / (Orintine + Citrulline), 2)
        value_8.append(index_gabr)
        index_AOR = round(arginine / Orintine, 1)
        value_8.append(index_AOR)
        index_asn_asp = round(asparagine / asparagine_acid, 2)
        value_8.append(index_asn_asp)
        creatine = round(float(metabolite_data.get('Creatinine', 0)), 1)
        value_8.append(creatine)
        nmma = round(float(metabolite_data.get('NMMA', 0)), 2)
        value_8.append(nmma)
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
        alanine = round(float(metabolite_data.get('Alanine', 0)), 1)
        value_9.append(alanine)
        # c0
        c0 = round(float(metabolite_data.get('C0', 0)), 1)
        value_9.append(c0)
        c2 = round(float(metabolite_data.get('C2', 0)), 2)
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
        c3 = round(float(metabolite_data.get('C3', 0)), 2)
        value_10.append(c3)
        c4 = round(float(metabolite_data.get('C4', 0)), 2)
        value_10.append(c4)
        c5 = round(float(metabolite_data.get('C5', 0)), 2)
        value_10.append(c5)
        c5_1 = round(float(metabolite_data.get('C5-1', 0)), 2)
        value_10.append(c5_1)
        c5_DC = round(float(metabolite_data.get('C5-DC', 0)), 1)
        value_10.append(c5_DC)
        c5_OH = round(float(metabolite_data.get('C5-OH', 0)), 2)
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
        c6 = round(float(metabolite_data.get('C6', 0)), 2)
        value_11.append(c6)
        c6_DC = round(float(metabolite_data.get('C6-DC', 0)), 3)
        value_11.append(c6_DC)
        c8 = round(float(metabolite_data.get('C8', 0)), 3)
        value_11.append(c8)
        c8_1 = round(float(metabolite_data.get('C8-1', 0)), 3)
        value_11.append(c8_1)
        c10 = round(float(metabolite_data.get('C10', 0)), 3)
        value_11.append(c10)
        c10_1 = round(float(metabolite_data.get('C10-1', 0)), 3)
        value_11.append(c10_1)
        c10_2 = round(float(metabolite_data.get('C10-2', 0)), 3)
        value_11.append(c10_2)
        c12 = round(float(metabolite_data.get('C12', 0)), 3)
        value_11.append(c12)
        c12_1 = round(float(metabolite_data.get('C12-1', 0)), 3)
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
        c14 = round(float(metabolite_data.get('C14', 0)), 3)
        value_12.append(c14)
        c14_1 = round(float(metabolite_data.get('C14-1', 0)), 3)
        value_12.append(c14_1)
        c14_2 = round(float(metabolite_data.get('C14-2', 0)), 3)
        value_12.append(c14_2)
        c14_OH = round(float(metabolite_data.get('C14-OH', 0)), 3)
        value_12.append(c14_OH)
        c16 = round(float(metabolite_data.get('C16', 0)), 3)
        value_12.append(c16)
        c16_1 = round(float(metabolite_data.get('C16-1', 0)), 3)
        value_12.append(c16_1)
        C16_1_OH = round(float(metabolite_data.get('C16-1-OH', 0)), 4)
        value_12.append(C16_1_OH)
        c16_OH = round(float(metabolite_data.get('C16-OH', 0)), 3)
        value_12.append(c16_OH)
        c18 = round(float(metabolite_data.get('C18', 0)), 3)
        value_12.append(c18)
        c18_1 = round(float(metabolite_data.get('C18-1', 0)), 3)
        value_12.append(c18_1)
        c18_1_OH = round(float(metabolite_data.get('C18-1-OH', 0)), 4)
        value_12.append(c18_1_OH)
        c18_2 = round(float(metabolite_data.get('C18-2', 0)), 3)
        value_12.append(c18_2)
        c18_OH = round(float(metabolite_data.get('C18-OH', 0)), 4)
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
        pantotenic_acid = round(float(metabolite_data.get('Pantothenic', 0)), 2)
        value_13.append(pantotenic_acid)
        riboflavin = round(float(metabolite_data.get('Riboflavin', 0)), 2)
        value_13.append(riboflavin)
        melatonine = round(float(metabolite_data.get('Melatonin', 0)), 3)
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
        uridine = round(float(metabolite_data.get('Uridine', 0)), 2)
        value_14.append(uridine)
        adenosine = round(float(metabolite_data.get('Adenosin', 0)), 2)
        value_14.append(adenosine)
        Citidine = round(float(metabolite_data.get('Cytidine', 0)), 2)
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
        cortisol = round(float(metabolite_data.get('Cortisol', 0)), 2)
        value_15.append(cortisol)
        # Histamine
        histamine = round(float(metabolite_data.get('Histamine', 0)), 3)
        value_15.append(histamine)
        return ref_15, value_15
        
    except Exception as e:
        print(f"Error in processing: {e}")
        
        return ref_15, [0.0, 0.0, 0.0]


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

def need_of_plus_minus(value: float, ref: str):
    if ' - ' in ref:
        lower, upper = map(float, ref.split(' - '))
        if value > upper:
            return '+'
        elif value < lower:
            return '-'
        else:
            return ''
    elif ref.startswith('< '):
        upper = float(ref.split('< ')[1])
        if value > upper:
            return '+'
        elif value < 0:  # Assuming <45 means 0-45 as per your note
            return '-'
        else:
            return ''
    else:
        # Handle other cases if needed
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
    if n <= 10:
        return '#50c150'  # Light green (similar to 9-10)
    elif n <= 20:
        return '#9fd047'   # Light yellow (similar to 7-8)
    elif n<= 30:
        return '#feb61d'  # Light orange (similar to 5-6)
    elif n <= 40:
        return '#fe991d'  # Light orange (similar to 5-6)
    elif n <= 50:
        return '#f25708'  # Light orange (similar to 5-6)
    
    elif n <= 70:
        return '#f21e08'  # Light orange (similar to 5-6)
    else:
        return '#c90909' # Orange-red (similar to 3-4)
    
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
    
    labels = df_result['Группа риска'].tolist()
    risk_levels = df_result['Риск-скор'].tolist()

    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # Close the circle
    risk_levels += risk_levels[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    # Gradient background
    colors = [
        'darkred', 'red', 'red', 'darkorange', 'orange', 
        'gold', 'yellow', 'yellowgreen', 'limegreen', 'green', 'green'
    ]

    # Fill between levels
    levels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for i in range(len(levels) - 1):
        ax.fill_between(angles, levels[i], levels[i + 1], color=colors[i], alpha=0.3)
    
    # Plot data
    ax.fill(angles, risk_levels, color='blue', alpha=0.25)
    ax.plot(angles, risk_levels, color='blue', linewidth=2)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=16)
    
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
        if ' - ' in ref_range:
            # Format "23 - 50"
            ref_min, ref_max = map(float, ref_range.split(' - '))
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
            return 50
        elif value > ref_max:
            return 100
        else:
            position = ((value - ref_min) / (ref_max - ref_min)) * 100
            return max(0, min(100, round(position, 2)))  # Clamp and round to 2 decimals
    
    except (ValueError, AttributeError, TypeError):
        # Return middle position if there's any error
        return 50
    
def NO_syntase_Group(file_path, metabolite_data):
    # Initialize scores for each metabolite
    scores = {
        'ADMA': 0,
        'TotalDMA (SDMA)': 0,
        'Arg/ADMA': 0,
        '(Arg+HomoArg)/ADMA': 0
    }
    
    try:
        # Load the risk parameters
        risk_params = pd.read_excel(file_path)
        
        # Convert metabolite_data from dict to Series for consistent access
        metab_data = pd.Series(metabolite_data)
        
        # Calculate ratios if needed
        if 'Arginine' in metab_data and 'ADMA' in metab_data:
            metab_data['Arg/ADMA'] = metab_data['Arginine'] / metab_data['ADMA']
        if 'Arginine' in metab_data and 'Homoarginine' in metab_data and 'ADMA' in metab_data:
            metab_data['(Arg+HomoArg)/ADMA'] = (metab_data['Arginine'] + metab_data['Homoarginine']) / metab_data['ADMA']
        
        # Check each metabolite and assign scores
        metabolites_to_check = [
            ('ADMA', 1),
            ('TotalDMA (SDMA)', 0.5),
            ('Arg/ADMA', 0.5),
            ('(Arg+HomoArg)/ADMA', 0.5)
        ]
        
        for metabolite, score in metabolites_to_check:
            if metabolite in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == metabolite].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[metabolite]
                    
                    if not (norm1 <= value <= norm2):
                        scores[metabolite] = score
                except (IndexError, KeyError):
                    print(f"Warning: {metabolite} not found in risk parameters or missing norms")
                    continue
    
    except Exception as e:
        print(f"Error in NO_syntase_Group: {str(e)}")
        return 50  # Return default score on error
    
    # Calculate the final score
    total_score = (
        scores['ADMA'] + 
        scores['TotalDMA (SDMA)'] + 
        scores['Arg/ADMA'] + 
        scores['(Arg+HomoArg)/ADMA']
    ) * 100 / 2.5
    
    if total_score >= 90:
        return 85
    else:
        return total_score

def Inflammation_Group(file_path, metabolite_data):
    scores = {
        'Kyn/Trp': 0,
        'Quin/HIAA': 0,
        'Quinolinic acid': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        # Calculate ratios if needed
        if 'Kynurenine' in metab_data and 'Tryptophan' in metab_data:
            metab_data['Kyn/Trp'] = metab_data['Kynurenine'] / metab_data['Tryptophan']
        if 'Quinolinic acid' in metab_data and 'HIAA' in metab_data:
            metab_data['Quin/HIAA'] = metab_data['Quinolinic acid'] / metab_data['HIAA']
        
        markers = [
            ('Kyn/Trp', 0.75),
            ('Quin/HIAA', 0.3),
            ('Quinolinic acid', 0.45)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Inflammation_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1.5
    if total_score >= 90:
        return 85
    else:
        return total_score

def Methilation_Group(file_path, metabolite_data):
    scores = {
        'TMAO': 0,
        'Betaine/choline': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        
        markers = [
            ('TMAO', 0.7),
            ('Betaine/choline', 0.3)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Methilation_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1.0
    if total_score >= 90:
        return 85
    else:
        return total_score

def Mitochondrial_Group(file_path, metabolite_data):
    scores = {
        'C0/(C16+C18)': 0,
        '(C16+C18)/C2': 0,
        'СДК': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('C0/(C16+C18)', 0.375),
            ('(C16+C18)/C2', 0.375),
            ('СДК', 0.75)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Mitochondrial_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1.5
    if total_score >= 90:
        return 85
    else:
        return total_score

def Insulin_Resistance_Group(file_path, metabolite_data):
    scores = {
        'BCAA': 0,
        'BCAA/AAA': 0,
        'Alanine/Valine': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        # Calculate ratios
        if 'Valine' in metab_data and 'Leucine' in metab_data and 'Isoleucine' in metab_data:
            metab_data['BCAA'] = metab_data['Valine'] + metab_data['Leucine'] + metab_data['Isoleucine']
        if 'BCAA' in metab_data and 'Phenylalanine' in metab_data and 'Tyrosine' in metab_data:
            metab_data['BCAA/AAA'] = metab_data['BCAA'] / (metab_data['Phenylalanine'] + metab_data['Tyrosine'])
        if 'Alanine' in metab_data and 'Valine' in metab_data:
            metab_data['Alanine/Valine'] = metab_data['Alanine'] / metab_data['Valine']
        
        markers = [
            ('BCAA', 0.75),
            ('BCAA/AAA', 0.45),
            ('Alanine/Valine', 0.3)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Insulin_Resistance_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1.5
    if total_score >= 90:
        return 85
    else:
        return total_score

def Neurovegitative_Group(file_path, metabolite_data):
    scores = {
        'Serotonin': 0,
        'Cortisol': 0,
        'Melatonin': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Serotonin', 0.6),
            ('Cortisol', 0.8),
            ('Melatonin', 0.6)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    # For some markers (like cortisol), only upper limit matters
                    if marker == 'Cortisol':
                        if value > norm2:
                            scores[marker] = weight
                    # For others (like serotonin, melatonin), both limits matter
                    else:
                        if not (norm1 <= value <= norm2):
                            scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Neurovegitative_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 2.0
    if total_score >= 90:
        return 85
    else:
        return total_score

def Methionine_Exchange_Group(file_path, metabolite_data):
    scores = {
        'Methionine': 0,
        'Methionine-Sulfoxide': 0,
        'Betaine': 0,
        'Choline': 0,
        'Betaine/сholine': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Methionine', 0.5),
            ('Methionine-Sulfoxide', 0.5),
            ('Betaine', 0.5),
            ('Choline', 0.5),
            ('Betaine/сholine', 1.0)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Methionine_Exchange_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 3.0  # Weight of this group is 3
    if total_score >= 90:
        return 85
    else:
        return total_score

# def Antoxidant_System_Group(file_path, metabolite_data):
#     scores = {
#         'GSH/GSG_index': 0
#     }
    
#     try:
#         risk_params = pd.read_excel(file_path)
#         metab_data = pd.Series(metabolite_data)
        
#         markers = [
#             ('GSH/GSG_index', 2.0)
#         ]
        
#         for marker, weight in markers:
#             if marker in metab_data:
#                 try:
#                     row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
#                     norm1 = row['norm_1']
#                     norm2 = row['norm_2']
#                     value = metab_data[marker]
                    
#                     if not (norm1 <= value <= norm2):
#                         scores[marker] = weight
#                 except (IndexError, KeyError):
#                     continue
    
#     except Exception as e:
#         print(f"Error in Antoxidant_System_Group: {str(e)}")
#         return 50
    
#     total_score = sum(scores.values()) * 100 / 2.0  # Weight of this group is 2
#     if total_score >= 90:
#         return 85
#     else:
#         return total_score

def Protein_Exchange_Group(file_path, metabolite_data):
    scores = {
        'BCAA': 0,
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('BCAA', 1.0),
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Protein_Exchange_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1.0  # Weight of this group is 2
    if total_score >= 90:
        return 85
    else:
        return total_score

def Aminoacid_Profile(file_path, metabolite_data):
    scores = {
        'Phe/Tyr': 0,
        'BCAA/AAA': 0,
        'Ornitine': 0,
        'Citrulline': 0  
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Phe/Tyr', 1),
            ('BCAA/AAA', 1),
            ('Ornitine', 0.5),
            ('Citrulline', 0.5)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Aminoacid_Profile: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 3.0  # Weight of this group is 1
    if total_score >= 90:
        return 85
    else:
        return total_score

# def Conjugation_Detoxication(file_path, metabolite_data):
#     scores = {
#         'Hippuric acid': 0,
#         'Indoxyl sulfate / IAA': 0,
#         'Ornithine': 0,
#         'Citrulline': 0
#     }
    
#     try:
#         risk_params = pd.read_excel(file_path)
#         metab_data = pd.Series(metabolite_data)
        
#         markers = [
#             ('Hippuric acid', 0.5),
#             ('Indoxyl sulfate / IAA', 0.5),
#             ('Ornithine', 0.5),
#             ('Citrulline', 0.5)
#         ]
        
#         for marker, weight in markers:
#             if marker in metab_data:
#                 try:
#                     row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
#                     norm1 = row['norm_1']
#                     norm2 = row['norm_2']
#                     value = metab_data[marker]
                    
#                     if not (norm1 <= value <= norm2):
#                         scores[marker] = weight
#                 except (IndexError, KeyError):
#                     continue
    
#     except Exception as e:
#         print(f"Error in Conjugation_Detoxication: {str(e)}")
#         return 50
    
#     total_score = sum(scores.values()) * 100 / 2.0  # Weight of this group is 2
#     if total_score >= 90:
#         return 85
#     else:
#         return total_score

def Oxidative_Stress_Group(file_path, metabolite_data):
    scores = {
        'Methionine-Sulfoxide': 0,
        'GSG_index': 0,
        'Taurine': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Methionine-Sulfoxide', 1.75),
            ('GSG_index', 1.75),
            ('Taurine', 1.25)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Oxidative_Stress_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 4.75  # Total weight is already 4.75
    if total_score >= 90:
        return 85
    else:
        return total_score  # Cap at 10
    

def Inflammation_and_Microbial_Group(file_path, metabolite_data):
    scores = {
        'Indole-3-propionic acid': 0,
        'Indole-3-acetic acid': 0,
        'Indole-3-carboxaldehyde': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Indole-3-propionic acid', 0.75),
            ('Indole-3-acetic acid', 0.75),
            ('Indole-3-carboxaldehyde', 0.50)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Inflammation_and_Microbial_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 2.0  # Total weight is 2.0
    if total_score >= 90:
        return 85
    else:
        return total_score

# def Aromatic_Toxic_Group(file_path, metabolite_data):
#     scores = {
#         'Hippuric acid': 0,
#         'Phenylacetic acid': 0
#     }
    
#     try:
#         risk_params = pd.read_excel(file_path)
#         metab_data = pd.Series(metabolite_data)
        
#         markers = [
#             ('Hippuric acid', 0.50),
#             ('Phenylacetic acid', 0.50)
#         ]
        
#         for marker, weight in markers:
#             if marker in metab_data:
#                 try:
#                     row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
#                     norm1 = row['norm_1']
#                     norm2 = row['norm_2']
#                     value = metab_data[marker]
                    
#                     if not (norm1 <= value <= norm2):
#                         scores[marker] = weight
#                 except (IndexError, KeyError):
#                     continue
    
#     except Exception as e:
#         print(f"Error in Aromatic_Toxic_Group: {str(e)}")
#         return 50
    
#     total_score = sum(scores.values()) * 100 / 1.0  # Total weight is 1.0
#     return min(total_score, 10)

def Nitrogen_Toxic_Group(file_path, metabolite_data):
    scores = {
        'ADMA': 0,
        'TotalDMA (SDMA)': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('ADMA', 0.75),
            ('TotalDMA (SDMA)', 0.50)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Nitrogen_Toxic_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1.25  # Total weight is 1.25
    if total_score >= 90:
        return 85
    else:
        return total_score

def Lipid_Toxic_Group(file_path, metabolite_data):
    scores = {
        '(C16+C18)/C2': 0,
        'СДК': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        # Calculate ratios if needed
        if 'C16' in metab_data and 'C18' in metab_data and 'C2' in metab_data:
            metab_data['(C16+C18)/C2'] = (metab_data['C16'] + metab_data['C18']) / metab_data['C2']
        
        markers = [
            ('(C16+C18)/C2', 0.50),
            ('СДК', 0.50)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Lipid_Toxic_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1
    if total_score >= 90:
        return 85
    else:
        return total_score

def Collagen_Group(file_path, metabolite_data):
    scores = {
        'Proline': 0,
        'Hydroxyproline': 0,
        'Glycine/Serine': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Proline', 1.3),
            ('Hydroxyproline', 1.3),
            ('Glycine/Serine', 0.6)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Collagen_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 3.2  # Total weight is 3.2
    if total_score >= 90:
        return 85
    else:
        return total_score

def Regeneration_Group(file_path, metabolite_data):
    scores = {
        'Methionine': 0,
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Methionine', 0.6),
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Regeneration_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 0.6 # Total weight is 1.2
    if total_score >= 90:
        return 85
    else:
        return total_score

def Dream_Group(file_path, metabolite_data):
    scores = {
        'Melatonin': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Melatonin', 1.6)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Dream_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1.6  # Total weight is 1.6
    if total_score >= 90:
        return 85
    else:
        return total_score

def Inflammation_and_Stress_Group(file_path, metabolite_data):
    scores = {
        'Serotonin': 0,
        'Cortisol': 0,
        'Indole-3-acetic acid': 0,
        'Tryptamine / IAA': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Serotonin', 0.6),
            ('Cortisol', 0.6),
            ('Indole-3-acetic acid', 0.3),
            ('Tryptamine / IAA', 0.3)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Inflammation_and_Stress_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1.8 # Total weight is 1.8
    if total_score >= 90:
        return 85
    else:
        return total_score

def Exchange_Serum_Group(file_path, metabolite_data):
    scores = {
        'Taurine': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Taurine', 1.3)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Exchange_Serum_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1.3  # Total weight is 1.3
    
    if total_score >= 90:
        return 85
    else:
        return total_score

def Neuroinflammation_Group(file_path, metabolite_data):
    scores = {
        'Kynurenine': 0,
        'Kyn/Trp': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        # Calculate ratios if needed
        if 'Kynurenine' in metab_data and 'Tryptophan' in metab_data:
            metab_data['Kyn/Trp'] = metab_data['Kynurenine'] / metab_data['Tryptophan']
        
        markers = [
            ('Kynurenine', 0.3),
            ('Kyn/Trp', 0.6)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Neuroinflammation_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 0.9  # Total weight is 0.9
    if total_score >= 90:
        return 85
    else:
        return total_score
    
def Energy_Exchange_Group(file_path, metabolite_data):
    scores = {
        'C0': 0,
        'C2': 0,
        'C2/C0': 0,
        '(C2+C3)/C0': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('C0', 1.2),
            ('C2', 0.75),
            ('C2/C0', 0.5),
            ('(C2+C3)/C0', 0.5)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Energy_Exchange_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 2.95  # Total weight is 2.95
    if total_score >= 90:
        return 85
    else:
        return total_score
    
def Energy_Exchange_Carnitine_Group(file_path, metabolite_data):
    scores = {
        'C0': 0,
        'C2': 0,
        'C2/C0': 0,
        '(C2+C3)/C0': 0,
        'C0/(C16+C18)': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('C0', 1),
            ('C2', 1),
            ('C2/C0', 0.75),
            ('(C2+C3)/C0', 0.625),
            ('C0/(C16+C18)', 0.625)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Energy_Exchange_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 4  # Total weight is 2.95
    if total_score >= 90:
        return 85
    else:
        return total_score

def Neuroadaptation_Group(file_path, metabolite_data):
    scores = {
        'Cortisol': 0,
        'Serotonin': 0,
        'Melatonin': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Cortisol', 1.2),
            ('Serotonin', 0.8),
            ('Melatonin', 0.75)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Neuroadaptation_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 2.75  # Total weight is 2.75
    if total_score >= 90:
        return 85
    else:
        return total_score

def Stress_Aminoacid_Group(file_path, metabolite_data):
    scores = {
        'Tyrosin': 0,
        'Histidine': 0,
        'Arginine': 0,
        '(Arg+HomoArg)/ADMA': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Tyrosin', 0.5),
            ('Histidine', 0.5),
            ('Arginine', 0.5),
            ('(Arg+HomoArg)/ADMA', 0.75)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Stress_Aminoacid_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 2.25  # Total weight is 2.25
    if total_score >= 90:
        return 85
    else:
        return total_score

def Metochondria_Creatinine_Group(file_path, metabolite_data):
    scores = {
        'Creatinine': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Creatinine', 0.5)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Metochondria_Creatinine_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 0.5  # Total weight is 0.5
    if total_score >= 90:
        return 85
    else:
        return total_score

def Glutamate_Exchange_Group(file_path, metabolite_data):
    scores = {
        'Glutamine/Glutamate': 0,
        'GSG_index': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Glutamine/Glutamate', 0.75),
            ('GSG_index', 0.75)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Glutamate_Exchange_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1.5  # Total weight is 1.55
    if total_score >= 90:
        return 85
    else:
        return total_score

def Tryptophan_Metabolism_Group(file_path, metabolite_data):
    scores = {
        'Indole-3-acetic acid': 0,
        'Indole-3-propionic acid': 0,
        'Indole-3-lactic acid': 0,
        'Tryptamine': 0,
        'Tryptophan': 0,
        'Indole-3-carboxaldehyde': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Indole-3-acetic acid', 1.5),
            ('Indole-3-propionic acid', 1.5),
            ('Indole-3-lactic acid', 1.0),
            ('Tryptamine', 0.5),
            ('Tryptophan', 0.5),
            ('Indole-3-carboxaldehyde', 0.75)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Tryptophan_Metabolism_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 5.75  # Total weight is 5.0
    if total_score >= 90:
        return 85
    else:
        return total_score

# def Microbial_Stress_Group(file_path, metabolite_data):
#     scores = {
#         'Hippuric acid': 0,
#         'Phenylacetic acid': 0,
#         'p-Cresol sulfate': 0,
#         'Indole-3-carboxaldehyde': 0
#     }
    
#     try:
#         risk_params = pd.read_excel(file_path)
#         metab_data = pd.Series(metabolite_data)
        
#         markers = [
#             ('Hippuric acid', 1.0),
#             ('Phenylacetic acid', 0.5),
#             ('p-Cresol sulfate', 1.5),
#             ('Indole-3-carboxaldehyde', 0.75)
#         ]
        
#         for marker, weight in markers:
#             if marker in metab_data:
#                 try:
#                     row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
#                     norm1 = row['norm_1']
#                     norm2 = row['norm_2']
#                     value = metab_data[marker]
                    
#                     if not (norm1 <= value <= norm2):
#                         scores[marker] = weight
#                 except (IndexError, KeyError):
#                     continue
    
#     except Exception as e:
#         print(f"Error in Microbial_Stress_Group: {str(e)}")
#         return 50
    
#     total_score = sum(scores.values()) * 100 / 3.75  # Total weight is 3.75
#         if total_score >= 90:
    #     return 85
    # else:
    #     return total_score

def Inflammation_and_Immune_Group(file_path, metabolite_data):
    scores = {
        'Kyn/Trp': 0,
        'Quin/HIAA': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Kyn/Trp', 0.75),
            ('Quin/HIAA', 0.5)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Inflammation_and_Immune_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1.25  # Total weight is 1.25
    if total_score >= 90:
        return 85
    else:
        return total_score
    
def Tryptophan_Inflammation_Group(file_path, metabolite_data):
    scores = {
        'Kyn/Trp': 0,
        'Trp/(Kyn+QA)': 0,
        'Quin/HIAA': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Kyn/Trp', 1.3),
            ('Trp/(Kyn+QA)', 1.3),
            ('Quin/HIAA', 0.6)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Tryptophan_Inflammation_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 3.2  # Total weight is 3.2
    if total_score >= 90:
        return 85
    else:
        return total_score

def Neuroendocrine_Group(file_path, metabolite_data):
    scores = {
        'Melatonin': 0,
        'Serotonin': 0,
        'Cortisol': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Melatonin', 0.8),
            ('Serotonin', 0.45),
            ('Cortisol', 0.55)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Neuroendocrine_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1.8  # Total weight is 1.8
    if total_score >= 90:
        return 85
    else:
        return total_score

def Integrative_Index_Group(file_path, metabolite_data):
    scores = {
        'ADMA': 0,
        'TMAO': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('ADMA', 0.65),
            ('TMAO', 0.45)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Integrative_Index_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1.1  # Total weight is 1.1
    if total_score >= 90:
        return 85
    else:
        return total_score

def Ido_Path_Tryptophan_Group(file_path, metabolite_data):
    scores = {
        'Kyn/Trp': 0,
        'Trp/(Kyn+QA)': 0,
        'Quin/HIAA': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Kyn/Trp', 1.88),
            ('Trp/(Kyn+QA)', 1.50),
            ('Quin/HIAA', 0.75)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Ido_Path_Tryptophan_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 4.13  # Total weight is 4.13
    if total_score >= 90:
        return 85
    else:
        return total_score

def Neuromediators_Group(file_path, metabolite_data):
    scores = {
        'Serotonin': 0,
        'HIAA': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Serotonin', 0.88),
            ('HIAA', 0.38)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Neuromediators_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1.26  # Total weight is 1.26
    if total_score >= 90:
        return 85
    else:
        return total_score
    
def Neuromediators_Neuro_Group(file_path, metabolite_data):
    scores = {
        'Serotonin': 0,
        'Melatonin': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Serotonin', 0.625),
            ('Melatonin', 0.625)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Neuromediators_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1.25  # Total weight is 1.26
    if total_score >= 90:
        return 85
    else:
        return total_score

def Indols_and_Phenols_Group(file_path, metabolite_data):
    scores = {
        'Indole-3-acetic acid': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Indole-3-acetic acid', 1.00),
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Indols_and_Phenols_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1  # Total weight is 1.75
    if total_score >= 90:
        return 85
    else:
        return total_score

def General_Stress_Immune_Group(file_path, metabolite_data):
    scores = {
        'Cortisol': 0,
        'ADMA': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Cortisol', 0.63),
            ('ADMA', 0.75)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in General_Stress_Immune_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1.38  # Total weight is 1.38
    if total_score >= 90:
        return 85
    else:
        return total_score

def Complex_Index_Group(file_path, metabolite_data):
    scores = {
        'Quinolinic acid': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Quinolinic acid', 1.50)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Complex_Index_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1.50  # Total weight is 1.50
    if total_score >= 90:
        return 85
    else:
        return total_score
    
def Amiac_Detox_Group(file_path, metabolite_data):
    scores = {
        'Ornitine': 0,
        'Citrulline': 0,
        'Arginine': 0
    }
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Ornitine', 0.78),
            ('Citrulline', 0.56),
            ('Arginine', 0.56)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Amiac_Detox_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1.88 
    if total_score >= 90:
        return 85
    else:
        return total_score
    
def Vitamine_B2_Group(file_path, metabolite_data):
    scores = {
        'Riboflavin': 0,
        'Glutamine/Glutamate': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Riboflavin', 1.76),
            ('Glutamine/Glutamate', 0.59)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Vitamine_B2_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 2.35  # Total weight is 2.35
    if total_score >= 90:
        return 85
    else:
        return total_score

def Vitamine_B5_Group(file_path, metabolite_data):
    scores = {
        'Pantothenic acid': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Pantothenic acid', 1.18)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Vitamine_B5_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1.18  # Total weight is 1.18
    if total_score >= 90:
        return 85
    else:
        return total_score

def Vitamine_B6_Group(file_path, metabolite_data):
    scores = {
        'Kynurenine': 0,
        'Kynurenic acid / Kynurenine': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Kynurenine', 0.59),
            ('Kynurenic acid / Kynurenine', 0.59)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Vitamine_B6_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1.18  # Total weight is 1.18
    if total_score >= 90:
        return 85
    else:
        return total_score

def Vitamine_B9_B12_Group(file_path, metabolite_data):
    scores = {
        'Methionine': 0,
        'Methionine-Sulfoxide': 0,
        'Betaine/сholine': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Methionine', 0.59),
            ('Methionine-Sulfoxide', 0.59),
            ('Betaine/сholine', 1.18)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Vitamine_B9_B12_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 2.36  # Total weight is 2.36
    if total_score >= 90:
        return 85
    else:
        return total_score

def Vitamine_B3_NAD_Group(file_path, metabolite_data):
    scores = {
        'Quinolinic acid': 0,
        'Trp/(Kyn+QA)': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        # Calculate ratio if needed
        if 'Tryptophan' in metab_data and 'Kynurenine' in metab_data and 'Quinolinic acid' in metab_data:
            metab_data['Trp/(Kyn+QA)'] = metab_data['Tryptophan'] / (metab_data['Kynurenine'] + metab_data['Quinolinic acid'])
        
        markers = [
            ('Quinolinic acid', 0.35),
            ('Trp/(Kyn+QA)', 0.35)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Vitamine_B3_NAD_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 0.70  # Total weight is 0.70
    if total_score >= 90:
        return 85
    else:
        return total_score

def Serum_Aminoacids_Group(file_path, metabolite_data):
    scores = {
        'Methionine + Taurine': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Methionine + Taurine', 1.18)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Serum_Aminoacids_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1.18  # Total weight is 1.18
    if total_score >= 90:
        return 85
    else:
        return total_score

def Neurotroph_Reserv_Group(file_path, metabolite_data):
    scores = {
        'Tyrosin': 0,
        'Tryptophan': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Tyrosin', 0.24),
            ('Tryptophan', 0.24)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Neurotroph_Reserv_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 0.48  # Total weight is 0.48
    if total_score >= 90:
        return 85
    else:
        return total_score
    
def Over_Sugar_Group(file_path, metabolite_data):
    scores = {
        'Alanine': 0,
        'Glutamine/Glutamate': 0,
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Alanine', 1.11),
            ('Glutamine/Glutamate', 0.89),
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Over_Sugar_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 2  # Total weight is 2.78
    if total_score >= 90:
        return 85
    else:
        return total_score

def Over_Lipid_Group(file_path, metabolite_data):
    scores = {
        'СДК': 0,
        '(C16+C18)/C2': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('СДК', 1.11),
            ('(C16+C18)/C2', 0.89)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Over_Lipid_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 2.00  # Total weight is 2.00
    if total_score >= 90:
        return 85
    else:
        return total_score

def Over_Protein_Group(file_path, metabolite_data):
    scores = {
        'BCAA': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('BCAA', 0.89)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Over_Protein_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 0.89  # Total weight is 1.45
    if total_score >= 90:
        return 85
    else:
        return total_score

def Deficit_Nutrients_Group(file_path, metabolite_data):
    scores = {
        'Methionine': 0,
        'Tryptophan': 0,
        'Riboflavin/Pantothenic': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        # Calculate ratio if needed
        if 'Riboflavin' in metab_data and 'Pantothenic acid' in metab_data:
            metab_data['Riboflavin/Pantothenic'] = metab_data['Riboflavin'] / metab_data['Pantothenic acid']
        
        markers = [
            ('Methionine', 0.67),
            ('Tryptophan', 0.67),
            ('Riboflavin/Pantothenic', 0.56)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Deficit_Nutrients_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1.90  # Total weight is 1.90
    if total_score >= 90:
        return 85
    else:
        return total_score

def Supply_Group(file_path, metabolite_data):
    scores = {
        'Serotonin': 0,
        'Cortisol': 0,
        'Betaine/choline': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Serotonin', 0.56),
            ('Cortisol', 0.56),
            ('Betaine/choline', 0.78)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Supply_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1.90  # Total weight is 1.90
    if total_score >= 90:
        return 85
    else:
        return total_score
    
def AA_Exchange_Group(file_path, metabolite_data):
    scores = {
        'BCAA': 0,
        'BCAA/AAA': 0,
        'Phe/Tyr': 0,
        'Glycine/Serine': 0,
        'Glutamine/Glutamate': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('BCAA', 1.25),
            ('BCAA/AAA', 1.0),
            ('Phe/Tyr', 0.75),
            ('Glycine/Serine', 0.625),
            ('Glutamine/Glutamate', 0.625)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in AA_Exchange_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 4.25  # Total weight is 4.25
    if total_score >= 90:
        return 85
    else:
        return total_score

def Sug_Exchange_Group(file_path, metabolite_data):
    scores = {
        'Alanine': 0,
        'Valine / Alanine': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Alanine', 1.0),
            ('Valine / Alanine', 0.5)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Sug_Exchange_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1.5  # Total weight is 1.5
    if total_score >= 90:
        return 85
    else:
        return total_score

def Lip_Exchange_Group(file_path, metabolite_data):
    scores = {
        '(C16+C18)/C2': 0,
        'СДК': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('(C16+C18)/C2', 1.0),
            ('СДК', 0.75)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Lip_Exchange_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1.75  # Total weight is 1.75
    if total_score >= 90:
        return 85
    else:
        return total_score

def Insulin_Exchange_Group(file_path, metabolite_data):
    scores = {
        'Tyrosin': 0,
        'Trp/Kyn': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Tyrosin', 0.75),
            ('Trp/Kyn', 0.5)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Insulin_Exchange_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1.25  # Total weight is 1.25
    if total_score >= 90:
        return 85
    else:
        return total_score

def Hormone_Exchange_Group(file_path, metabolite_data):
    scores = {
        'Cortisol': 0,
        'Serotonin': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Cortisol', 0.625),
            ('Serotonin', 0.625)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер / Соотношение'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Hormone_Exchange_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1.25  # Total weight is 1.25
    if total_score >= 90:
        return 85
    else:
        return total_score
    
def Chronic_Inflammation_Group(file_path, metabolite_data):
    scores = {
        'Kyn/Trp': 0,
        'Quinolinic acid': 0,
        'Quin/HIAA': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Kyn/Trp', 1.05),
            ('Quinolinic acid', 1.05),
            ('Quin/HIAA', 0.74)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Chronic_Inflammation_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 2.84  # Total weight is 2.84
    if total_score >= 90:
        return 85
    else:
        return total_score

def Ox_Stress_Group(file_path, metabolite_data):
    scores = {
        'Methionine-Sulfoxide': 0,
        'ADMA / NMMA': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Methionine-Sulfoxide', 0.74),
            ('ADMA / NMMA', 0.84)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Ox_Stress_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1.58  # Total weight is 1.58
    if total_score >= 90:
        return 85
    else:
        return total_score

def Metil_Epigen_Group(file_path, metabolite_data):
    scores = {
        'Betaine/сholine': 0,
        'DMG / Choline': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Betaine/сholine', 0.74),
            ('DMG / Choline', 0.74)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Metil_Epigen_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1.48  # Total weight is 1.48
    if total_score >= 90:
        return 85
    else:
        return total_score

def Microbiota_Detox_Group(file_path, metabolite_data):
    scores = {
        'Indole-3-carboxaldehyde': 0,
        'Indole-3-propionic acid': 0,
        'Indole-3-acetic acid': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Indole-3-carboxaldehyde', 0.53),
            ('Indole-3-propionic acid', 0.53),
            ('Indole-3-acetic acid', 0.53)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Microbiota_Detox_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1.59  # Total weight is 1.59
    if total_score >= 90:
        return 85
    else:
        return total_score

def Metabolic_Stress_Group(file_path, metabolite_data):
    scores = {
        'Glutamine/Glutamate': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Glutamine/Glutamate', 0.74)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Metabolic_Stress_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 0.74  # Total weight is 0.74
    if total_score >= 90:
        return 85
    else:
        return total_score

def Neuroendocrine_Controle_Group(file_path, metabolite_data):
    scores = {
        'Serotonin': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Serotonin', 0.53)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Neuroendocrine_Controle_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 0.53  # Total weight is 0.53
    if total_score >= 90:
        return 85
    else:
        return total_score

def Prolifiration_Mitosis_Group(file_path, metabolite_data):
    scores = {
        'Tryptamine': 0,
        'Melatonin': 0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Tryptamine', 0.53),
            ('Melatonin', 0.74)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Prolifiration_Mitosis_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1.27  # Total weight is 1.27
    if total_score >= 90:
        return 85
    else:
        return total_score
    
def Ido_Neuroinflam_Group(file_path, metabolite_data):
    scores = {
        'Kyn/Trp': 0,
        'Quin/HIAA': 0,
        'Quinolinic acid': 0,
        'Kynurenic acid': 0,
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Kyn/Trp', 1.25),
            ('Quin/HIAA', 1),
            ('Quinolinic acid', 1.25),
            ('Kynurenic acid', 0.75)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Ido_Neuroinflam_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 4.5  # Total weight is 4.5
    if total_score >= 90:
        return 85
    else:
        return total_score
    
def Disbalance_Metabolites_Group(file_path, metabolite_data):
    scores = {
        'Kynurenine': 0,
        'Xanthurenic acid': 0,
        'Trp/(Kyn+QA)': 0,
        'Kyn/Quin': 0,
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Kynurenine', 0.75),
            ('Xanthurenic acid', 0.625),
            ('Trp/(Kyn+QA)', 0.625),
            ('Kyn/Quin', 0.625)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Disbalance_Metabolites_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 2.625  # Total weight is 2.625
    if total_score >= 90:
        return 85
    else:
        return total_score
    
def Mitochondria_Stress_Group(file_path, metabolite_data):
    scores = {
        'Cortisol': 0,
        'Methionine-Sulfoxide':0
    }
    
    try:
        risk_params = pd.read_excel(file_path)
        metab_data = pd.Series(metabolite_data)
        
        markers = [
            ('Cortisol', 0.625),
            ('Methionine-Sulfoxide', 0.625)
        ]
        
        for marker, weight in markers:
            if marker in metab_data:
                try:
                    row = risk_params[risk_params['Маркер'] == marker].iloc[0]
                    norm1 = row['norm_1']
                    norm2 = row['norm_2']
                    value = metab_data[marker]
                    
                    if not (norm1 <= value <= norm2):
                        scores[marker] = weight
                except (IndexError, KeyError):
                    continue
    
    except Exception as e:
        print(f"Error in Mitochondria_Stress_Group: {str(e)}")
        return 50
    
    total_score = sum(scores.values()) * 100 / 1.25  # Total weight is 1.875
    if total_score >= 90:
        return 85
    else:
        return total_score

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
        
        # РИСК ССЗ
        no_syntase_score = NO_syntase_Group(risk_params_path, metabolite_data)
        inflammation_score = Inflammation_Group(risk_params_path, metabolite_data)
        methilation_score = Methilation_Group(risk_params_path, metabolite_data)
        mitochondrial_score = Mitochondrial_Group(risk_params_path, metabolite_data)
        insuline_resistance_score = Insulin_Resistance_Group(risk_params_path, metabolite_data)
        neurovegitative_score = Neurovegitative_Group(risk_params_path, metabolite_data)
        
        # Печеночные функции
        Methionine_exchange = Methionine_Exchange_Group(risk_params_path, metabolite_data)
        # antoxidant_system = Antoxidant_System_Group(risk_params_path, metabolite_data)
        protein_exchange = Protein_Exchange_Group(risk_params_path, metabolite_data)
        aminoacid_profile = Aminoacid_Profile(risk_params_path, metabolite_data)
        # conjugation_detoxication = Conjugation_Detoxication(risk_params_path, metabolite_data)
        
        # Влияние факторов среды
        oxidative_stress_score = Oxidative_Stress_Group(risk_params_path, metabolite_data)
        inflam_and_microbiotic_score = Inflammation_and_Microbial_Group(risk_params_path, metabolite_data)
        # aromatic_toxic_score = Aromatic_Toxic_Group(risk_params_path, metabolite_data)
        nitrogen_toxic_score = Nitrogen_Toxic_Group(risk_params_path, metabolite_data)
        lipid_toxic_score = Lipid_Toxic_Group(risk_params_path, metabolite_data)
        
        
        #состояние кожи и волос
        collagen_score = Collagen_Group(risk_params_path, metabolite_data)
        regeneration_score = Regeneration_Group(risk_params_path, metabolite_data)
        dream_score = Dream_Group(risk_params_path, metabolite_data)
        inflam_stress_score = Inflammation_and_Stress_Group(risk_params_path, metabolite_data)
        exchange_serum_score = Exchange_Serum_Group(risk_params_path, metabolite_data)
        neuro_inflammation_score = Neuroinflammation_Group(risk_params_path, metabolite_data)
        
        # Адаптивные возможности организма
        energy_exchange_score = Energy_Exchange_Group(risk_params_path, metabolite_data)
        neuroadaptation_score = Neuroadaptation_Group(risk_params_path, metabolite_data)
        stress_aminoacid_score = Stress_Aminoacid_Group(risk_params_path, metabolite_data)
        metochondria_creatinine_score = Metochondria_Creatinine_Group(risk_params_path, metabolite_data)
        glutamate_exchange_score = Glutamate_Exchange_Group(risk_params_path, metabolite_data)
        
        # Здоровье микробиоты
        tryptophan_metabolism_score = Tryptophan_Metabolism_Group(risk_params_path, metabolite_data)
        # microbial_stress_score = Microbial_Stress_Group(risk_params_path, metabolite_data)
        inflam_immune_score = Inflammation_and_Immune_Group(risk_params_path, metabolite_data)
        
        # Темп биологического старения
        tryptophan_inflam_score = Tryptophan_Inflammation_Group(risk_params_path, metabolite_data)
        # оксидативный стресс уже существует
        # метахондрии уже есть
        neuro_endocrine_score = Neuroendocrine_Group(risk_params_path, metabolite_data)
        integrative_index_score = Integrative_Index_Group(risk_params_path, metabolite_data)
        
        # Степень воспалительных процессов
        ido_path_tryptophan_score = Ido_Path_Tryptophan_Group(risk_params_path, metabolite_data)
        neuromediators_score = Neuromediators_Group(risk_params_path, metabolite_data)
        indols_phenols_score = Indols_and_Phenols_Group(risk_params_path, metabolite_data)
        general_stress_immune_score = General_Stress_Immune_Group(risk_params_path, metabolite_data)
        complex_index = Complex_Index_Group(risk_params_path, metabolite_data)
        
        # Токсическая нагрузка и детоксикация
        amiac_detox_score =  Amiac_Detox_Group(risk_params_path, metabolite_data)
        # оксидативная нагрузка уже есть
        # азотистая нагрузка тоже есть
        
        # Митохондриальное здоровье
        energy_exchange_carnitine_score = Energy_Exchange_Carnitine_Group(risk_params_path, metabolite_data)
        
        # Нутриентный статус организма
        vitamine_b2_score = Vitamine_B2_Group(risk_params_path, metabolite_data)
        vitamine_b5_score = Vitamine_B5_Group(risk_params_path, metabolite_data)
        vitamine_b6_score = Vitamine_B6_Group(risk_params_path, metabolite_data)
        vitamine_b9_b12_score = Vitamine_B9_B12_Group(risk_params_path, metabolite_data)
        vitamine_b3_nad_score = Vitamine_B3_NAD_Group(risk_params_path, metabolite_data)
        serum_aminoacids_score = Serum_Aminoacids_Group(risk_params_path, metabolite_data)
        # energy exchange
        neurotroph_reserv_score = Neurotroph_Reserv_Group(risk_params_path, metabolite_data)
        
        # # Риск алиментарно-зависимых заболеваний
        over_sugar_score = Over_Sugar_Group(risk_params_path, metabolite_data)
        over_lipid_score = Over_Lipid_Group(risk_params_path, metabolite_data)
        over_protein_score = Over_Protein_Group(risk_params_path, metabolite_data)
        deficit_nutrients_score = Deficit_Nutrients_Group(risk_params_path, metabolite_data)
        supply_score = Supply_Group(risk_params_path, metabolite_data)
        
        # Обмен веществ
        aa_exchange = AA_Exchange_Group(risk_params_path, metabolite_data)
        sug_exchange = Sug_Exchange_Group(risk_params_path, metabolite_data)
        lip_exchange = Lip_Exchange_Group(risk_params_path, metabolite_data)
        insulin_exchange = Insulin_Exchange_Group(risk_params_path, metabolite_data)
        hormone_exchange = Hormone_Exchange_Group(risk_params_path, metabolite_data)
        
        # Риск онкологических заболеваний
        chronic_inflamm_score = Chronic_Inflammation_Group(risk_params_path, metabolite_data)
        ox_stress_score = Ox_Stress_Group(risk_params_path, metabolite_data)
        metil_epigen_score = Metil_Epigen_Group(risk_params_path, metabolite_data)
        microbiota_detox_score = Microbiota_Detox_Group(risk_params_path, metabolite_data)
        metabolic_stress_score = Metabolic_Stress_Group(risk_params_path, metabolite_data)
        neuro_endocrine_controle_score = Neuroendocrine_Controle_Group(risk_params_path, metabolite_data)
        prolifiration_mitosis_score = Prolifiration_Mitosis_Group(risk_params_path, metabolite_data)
        
        # риска нейродегенеративных заболеваний
        ido_neuroinflam_score = Ido_Neuroinflam_Group(risk_params_path, metabolite_data)
        disbalance_metabolites_score = Disbalance_Metabolites_Group(risk_params_path, metabolite_data)
        neuromediators_neuro_score = Neuromediators_Neuro_Group(risk_params_path, metabolite_data)
        mitochondria_stress_score = Mitochondria_Stress_Group(risk_params_path, metabolite_data)
        
        def create_layout():
            """Your complete existing layout using all the variables"""
            return html.Div([
            # 1 страница
            html.Div([
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
                    ],style={'margin-top':'10px','margin-left':'25px','color':'black','font-family':'Calibri','font-size':'15px'}),
                    
                ],style={'width':'80%','height':'100px', 'color':'white','margin':'0px','background-image':'url("/assets/rHeader.png")','background-repeat':'no-repeat','background-size':'100%','background-position':'center'}),
            ], style={'display':'flex', 'justify-content':'right','width':'100%','height':'100px','margin-bottom':'10px'}),
            html.Div([
                html.H1(children='Панорамный метаболомный обзор', style={'textAlign':'center','margin':'0px'}),]
                     , style={'width':'100%','background-color':'#0874bc', 'color':'white','font-family':'Calibri','margin':'0px'}),

            html.Img(src=app.get_asset_url('radial_diagram.png'), style={'width':'100%','height':'auto','margin-top':'12px', 'margin-bottom':'2px'}),
            #  Make table with columns Балл and Интерпретация
            dash_table.DataTable(
                    columns=[
                        {"name": "Балл", "id": "Балл"},
                        {"name": "Интерпретация", "id": "Интерпретация"},
                    ],
                    data=[
                        {"Балл": "9-10", "Интерпретация": "Метаболческая ось в хорошем или оптимальном состоянии"},
                        {"Балл": "7-8", "Интерпретация": "Незначительные отклонения, компенсаторные механизмы работают"},
                        {"Балл": "5-6", "Интерпретация": "Умеренные нарушения — не критично, но уже требует коррекции"},
                        {"Балл": "3-4", "Интерпретация": "Существенные изменения — снижен резерв, хроническая нагрузка"},
                        {"Балл": "1-2", "Интерпретация": "Выраженные патологии, декомпенсация, высокий риск"},
                    ],
                    style_header={
                        'backgroundColor': '#3990c9',
                        'color': 'white',
                        'font-family': 'Calibri',
                        'fontSize': '15px',
                        'fontWeight': 'bold',
                        'textAlign': 'center',
                        'padding': '0px 10px',
                    },
                    style_cell={
                        'font-family': 'Calibri',
                        'fontSize': '13px',
                        'color': 'black !important',
                        'textAlign': 'center',
                        'padding': '0px 20px',
                    },
                    style_table={
                        'width': 'auto',
                        'align': 'center',
                        'padding': '0px 60px',
                        'border-collapse': 'collapse'
                    },
                    style_data_conditional=[
                        {
                            'if': {
                                'filter_query': '{Балл} eq "9-10"',
                                'column_id': 'Балл'
                            },
                            'background-color': 'rgba(190,235,190,255)'
                        },
                        {
                            'if': {
                                'filter_query': '{Балл} eq "7-8"',
                                'column_id': 'Балл'
                            },
                            'background-color': 'rgba(255,255,175,255)',
                        },
                        {
                            'if': {
                                'filter_query': '{Балл} eq "5-6"',
                                'column_id': 'Балл'
                            },
                            'background-color': 'rgba(255,225,175,255)'
                        },
                        {
                            'if': {
                                'filter_query': '{Балл} eq "3-4"',
                                'column_id': 'Балл'
                            },
                            'background-color': 'rgb(234, 102, 25, 0.3)',
                        },
                        {
                            'if': {
                                'filter_query': '{Балл} eq "1-2"',
                                'column_id': 'Балл'
                            },
                            'background-color': 'rgb(234, 25, 25, 0.3)'
                        },
                    ]
                ),
            
            html.Div([
            # ADD info icon
            
            html.Img(src=app.get_asset_url('info_icon.png'), style={'width':'20px','height':'20px','margin-right':'15px'}),
            
            html.P('Ниже показано, какие классы метаболитов составляют функциональные группы, и как изменение в классе метаболитов повлияло на результат Панорамного метаболомного обзора.',
                    style={'color':'black','font-family':'Calibri','font-size':'16px','text-align':"left"}),
            ], style={'display': 'flex','margin-top':'10px','margin-bottom':'10px', 'flex-direction': 'row','align-items': 'center', 'width':'fit-content', 'border-radius': '5px', 'padding': '0px 0px 0px 15px', 'background-color': '#fffede'}),
            
            # Plot risk_scores table
            html.Div([
                html.Div([
                    html.Div([
                        html.P('1. Сердечно-сосудистые заболевания', style={'margin': '0px', 'margin-bottom': '1px'}),
                        html.Div([
                            html.Div([
                                html.Div([], style={
                                    'width': f"{risk_scores.loc[risk_scores['Группа риска'] == 'Риск ССЗ', 'Риск-скор'].values[0] * 10}%",
                                    'background-color': get_color_under_normal_dist(
                                        100-(risk_scores.loc[risk_scores['Группа риска'] == 'Риск ССЗ', 'Риск-скор'].values[0] * 10)
                                    ),
                                    'border-radius': '2px',
                                    'height': '13px',
                                    'line-height': 'normal',
                                    'display': 'inline-block',
                                    'vertical-align': 'center',
                                }),
                            ], style={'display': 'flex', 'align-self': 'center','width': '70px', 'height': '13px','line-height': 'normal', 'border-radius': '2px','background-color':  'lightgrey', 'margin-left':'5px', 'margin-right':'5px'}),
                            html.B(
                                f"{risk_scores.loc[risk_scores['Группа риска'] == 'Риск ССЗ', 'Риск-скор'].values[0]} из 10",
                                style={'margin': '0px'}
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
                        'margin-top': '5px'
                    }),
                    
                    html.Div([], style={
                        'width': "100%",
                        'background-color': "#0874bc",
                        'height': '2px',
                        'line-height': 'normal',
                        'display': 'inline-block',
                        'vertical-align': 'center',
                        'margin-bottom':'2px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 - no_syntase_score}%',
                                'background-color': get_color(no_syntase_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('NO-синтаза / Эндотелий', style={
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
                                'width': f'{100 -  inflammation_score}%',
                                'background-color': get_color(inflammation_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Воспаление / IDO путь', style={
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
                                'width': f'{100 -  methilation_score}%',
                                'background-color': get_color(methilation_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Метилирование / холин', style={
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
                                'background-color': get_color(mitochondrial_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Митохондрии / β-окисление', style={
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
                                'width': f'{100 -  insuline_resistance_score}%',
                                'background-color': get_color(insuline_resistance_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Инсулинорезистентность', style={
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
                                'width': f'{100 -  neurovegitative_score}%',
                                'background-color': get_color(neurovegitative_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Нейровегетативный стресс', style={
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
                        html.P('3. Устойчивость к внешним факторам', style={'margin': '0px', 'margin-bottom': '1px'}),
                        html.Div([
                            html.Div([
                                html.Div([], style={
                                    'width': f"{risk_scores.loc[risk_scores['Группа риска'] == 'Резистентность к внешним факторам', 'Риск-скор'].values[0] * 10}%",
                                    'background-color': get_color_under_normal_dist(
                                        100-(risk_scores.loc[risk_scores['Группа риска'] == 'Резистентность к внешним факторам', 'Риск-скор'].values[0] * 10)
                                    ),
                                    'border-radius': '2px',
                                    'height': '13px',
                                    'line-height': 'normal',
                                    'display': 'inline-block',
                                    'vertical-align': 'center',
                                }),
                            ], style={'display': 'flex', 'align-self': 'center','width': '70px', 'height': '13px','line-height': 'normal', 'border-radius': '2px','background-color':  'lightgrey', 'margin-left':'5px', 'margin-right':'5px'}),
                            html.B(
                                f"{risk_scores.loc[risk_scores['Группа риска'] == 'Резистентность к внешним факторам', 'Риск-скор'].values[0]} из 10",
                                style={'margin': '0px'}
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
                        'background-color': "#0874bc",
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
                                'background-color': get_color(oxidative_stress_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                                'background-color': get_color(inflam_and_microbiotic_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                    #             'background-color': get_color(aromatic_toxic_score),
                    #             'border-radius': '5px',
                    #             'height': '10px',
                    #             'line-height': 'normal',
                    #             'display': 'inline-block',
                    #             'vertical-align': 'center'
                    #         }),
                    #     ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                                'background-color': get_color(nitrogen_toxic_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                                'background-color': get_color(lipid_toxic_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                
            # колонка 222222222222222222222222222222222
            
            html.Div([
                    html.Div([
                        html.P('2. Печеночные функции', style={'margin': '0px', 'margin-bottom': '1px'}),
                        html.Div([
                            html.Div([
                                html.Div([], style={
                                    'width': f"{risk_scores.loc[risk_scores['Группа риска'] == 'Печеночные функции', 'Риск-скор'].values[0] * 10}%",
                                    'background-color': get_color_under_normal_dist(
                                        100-(risk_scores.loc[risk_scores['Группа риска'] == 'Печеночные функции', 'Риск-скор'].values[0] * 10)
                                    ),
                                    'border-radius': '2px',
                                    'height': '13px',
                                    'line-height': 'normal',
                                    'display': 'inline-block',
                                    'vertical-align': 'center',
                                }),
                            ], style={'display': 'flex', 'align-self': 'center','width': '70px', 'height': '13px','line-height': 'normal', 'border-radius': '2px','background-color':  'lightgrey', 'margin-left':'5px', 'margin-right':'5px'}),
                            html.B(
                                f"{risk_scores.loc[risk_scores['Группа риска'] == 'Печеночные функции', 'Риск-скор'].values[0]} из 10",
                                style={'margin': '0px'}
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
                        'margin-top': '5px'
                    }),
                    
                    html.Div([], style={
                        'width': "100%",
                        'background-color': "#0874bc",
                        'height': '2px',
                        'line-height': 'normal',
                        'display': 'inline-block',
                        'vertical-align': 'center',
                        'margin-bottom':'2px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 -  Methionine_exchange}%',
                                'background-color': get_color(Methionine_exchange),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Обмен метионина и метилирование', style={
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
                    #             'width': f'{100 -  antoxidant_system}%',
                    #             'background-color': get_color(antoxidant_system),
                    #             'border-radius': '5px',
                    #             'height': '10px',
                    #             'line-height': 'normal',
                    #             'display': 'inline-block',
                    #             'vertical-align': 'center'
                    #         }),
                    #     ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                    #     html.Div([
                    #         html.P('Антиоксидантная система', style={
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
                                'width': f'{100 -  protein_exchange}%',
                                'background-color': get_color(protein_exchange),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Белковый обмен', style={
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
                                'width': f'{100 -  aminoacid_profile}%',
                                'background-color': get_color(aminoacid_profile),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Аминокислотный профиль', style={
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
                    #             'width': f'{100 -  conjugation_detoxication}%',
                    #             'background-color': get_color(conjugation_detoxication),
                    #             'border-radius': '5px',
                    #             'height': '10px',
                    #             'line-height': 'normal',
                    #             'display': 'inline-block',
                    #             'vertical-align': 'center'
                    #         }),
                    #     ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                    #     html.Div([
                    #         html.P('Конъюгация и детоксикация', style={
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
                        html.P('4. Состояние кожи и волос', style={'margin': '0px', 'margin-bottom': '1px'}),
                        html.Div([
                            html.Div([
                                html.Div([], style={
                                    'width': f"{risk_scores.loc[risk_scores['Группа риска'] == 'Состояние кожи и волос', 'Риск-скор'].values[0] * 10}%",
                                    'background-color': get_color_under_normal_dist(
                                        100-(risk_scores.loc[risk_scores['Группа риска'] == 'Состояние кожи и волос', 'Риск-скор'].values[0] * 10)
                                    ),
                                    'border-radius': '2px',
                                    'height': '13px',
                                    'line-height': 'normal',
                                    'display': 'inline-block',
                                    'vertical-align': 'center',
                                }),
                            ], style={'display': 'flex', 'align-self': 'center','width': '70px', 'height': '13px','line-height': 'normal', 'border-radius': '2px','background-color':  'lightgrey', 'margin-left':'5px', 'margin-right':'5px'}),
                            html.B(
                                f"{risk_scores.loc[risk_scores['Группа риска'] == 'Состояние кожи и волос', 'Риск-скор'].values[0]} из 10",
                                style={'margin': '0px'}
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
                        'margin-top': '28px'
                    }),
                    
                    html.Div([], style={
                        'width': "100%",
                        'background-color': "#0874bc",
                        'height': '2px',
                        'line-height': 'normal',
                        'display': 'inline-block',
                        'vertical-align': 'center',
                        'margin-bottom':'2px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 -  collagen_score}%',
                                'background-color': get_color(collagen_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Коллаген и соединительная ткань', style={
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
                                'width': f'{100 -  regeneration_score}%',
                                'background-color': get_color(regeneration_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Регенерация и рост', style={
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
                                'width': f'{100 - dream_score}%',
                                'background-color': get_color(dream_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Сон и гормональный фон', style={
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
                                'width': f'{100 - inflam_stress_score}%',
                                'background-color': get_color(inflam_stress_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Воспаление и стресс', style={
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
                                'width': f'{100 -  exchange_serum_score}%',
                                'background-color': get_color(exchange_serum_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Обмен серы и кожи', style={
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
                                'width': f'{100 - neuro_inflammation_score}%',
                                'background-color': get_color(neuro_inflammation_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Нейровоспаление', style={
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
                'margin-top': '5px'
            }),
            html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
                   style={'page-break-after': 'always','color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"left",'font-style':'italic','margin-top':'20px'}),
            
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
            ], style={'display':'flex', 'justify-content':'space-between','width':'100%','height':'54px','color':'#0874bc'}),
            # Страница 1.2
            # Plot risk_scores table
            html.Div([
                html.Div([
                    html.Div([
                        html.P('5. Адаптивность организма', style={'margin': '0px', 'margin-bottom': '1px'}),
                        html.Div([
                            html.Div([
                                html.Div([], style={
                                    'width': f"{risk_scores.loc[risk_scores['Группа риска'] == 'Адаптивные возможности организма', 'Риск-скор'].values[0] * 10}%",
                                    'background-color': get_color_under_normal_dist(
                                        100-(risk_scores.loc[risk_scores['Группа риска'] == 'Адаптивные возможности организма', 'Риск-скор'].values[0] * 10)
                                    ),
                                    'border-radius': '2px',
                                    'height': '13px',
                                    'line-height': 'normal',
                                    'display': 'inline-block',
                                    'vertical-align': 'center',
                                }),
                            ], style={'display': 'flex', 'align-self': 'center','width': '70px', 'height': '13px','line-height': 'normal', 'border-radius': '2px','background-color':  'lightgrey', 'margin-left':'5px', 'margin-right':'5px'}),
                            html.B(
                                f"{risk_scores.loc[risk_scores['Группа риска'] == 'Адаптивные возможности организма', 'Риск-скор'].values[0]} из 10",
                                style={'margin': '0px'}
                            )
                        ], style ={'display': 'flex', 'flex-direction': 'row', 'flex-wrap': 'nowrap'})
                    ],  style={
                        'color': 'black',
                        'font-family': 'Calibri',
                        'font-size': '16px',
                        'margin': '0px',
                        'display': 'flex',
                        'justify-content': 'space-between',
                        'margin-bottom': '0px'
                    }),
                    
                    html.Div([], style={
                        'width': "100%",
                        'background-color': "#0874bc",
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
                                'background-color': get_color(energy_exchange_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                                'background-color': get_color(neuroadaptation_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                                'background-color': get_color(stress_aminoacid_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                                'background-color': get_color(metochondria_creatinine_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                                'background-color': get_color(glutamate_exchange_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                    
                    html.Div([
                        html.P('7. Темп биологического старения', style={'margin': '0px', 'margin-bottom': '1px'}),
                        html.Div([
                            html.Div([
                                html.Div([], style={
                                    'width': f"{risk_scores.loc[risk_scores['Группа риска'] == 'Темп биологического старения', 'Риск-скор'].values[0] * 10}%",
                                    'background-color': get_color_under_normal_dist(
                                        100-(risk_scores.loc[risk_scores['Группа риска'] == 'Темп биологического старения', 'Риск-скор'].values[0] * 10)
                                    ),
                                    'border-radius': '2px',
                                    'height': '13px',
                                    'line-height': 'normal',
                                    'display': 'inline-block',
                                    'vertical-align': 'center',
                                }),
                            ], style={'display': 'flex', 'align-self': 'center','width': '70px', 'height': '13px','line-height': 'normal', 'border-radius': '2px','background-color':  'lightgrey', 'margin-left':'5px', 'margin-right':'5px'}),
                            html.B(
                                f"{risk_scores.loc[risk_scores['Группа риска'] == 'Темп биологического старения', 'Риск-скор'].values[0]} из 10",
                                style={'margin': '0px'}
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
                        'background-color': "#0874bc",
                        'height': '2px',
                        'line-height': 'normal',
                        'display': 'inline-block',
                        'vertical-align': 'center',
                        'margin-bottom':'2px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 -  tryptophan_inflam_score}%',
                                'background-color': get_color(tryptophan_inflam_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Триптофан / воспаление', style={
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
                                'width': f'{100 -  oxidative_stress_score}%',
                                'background-color': get_color(oxidative_stress_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                                'width': f'{100 -  mitochondrial_score}%',
                                'background-color': get_color(mitochondrial_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Митохондрии', style={
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
                                'width': f'{100 -  neuro_endocrine_score}%',
                                'background-color': get_color(neuro_endocrine_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Нейроэндокринная ось', style={
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
                                'width': f'{100 -  integrative_index_score}%',
                                'background-color': get_color(integrative_index_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Интегративные индексы', style={
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
                        html.P('6. Здоровье микробиоты', style={'margin': '0px', 'margin-bottom': '1px'}),
                        html.Div([
                            html.Div([
                                html.Div([], style={
                                    'width': f"{risk_scores.loc[risk_scores['Группа риска'] == 'Здоровье микробиоты', 'Риск-скор'].values[0] * 10}%",
                                    'background-color': get_color_under_normal_dist(
                                        100-(risk_scores.loc[risk_scores['Группа риска'] == 'Здоровье микробиоты', 'Риск-скор'].values[0] * 10)
                                    ),
                                    'border-radius': '2px',
                                    'height': '13px',
                                    'line-height': 'normal',
                                    'display': 'inline-block',
                                    'vertical-align': 'center',
                                }),
                            ], style={'display': 'flex', 'align-self': 'center','width': '70px', 'height': '13px','line-height': 'normal', 'border-radius': '2px','background-color':  'lightgrey', 'margin-left':'5px', 'margin-right':'5px'}),
                            html.B(
                                f"{risk_scores.loc[risk_scores['Группа риска'] == 'Здоровье микробиоты', 'Риск-скор'].values[0]} из 10",
                                style={'margin': '0px'}
                            )
                        ], style ={'display': 'flex', 'flex-direction': 'row', 'flex-wrap': 'nowrap'})
                    ],  style={
                        'color': 'black',
                        'font-family': 'Calibri',
                        'font-size': '16px',
                        'margin': '0px',
                        'display': 'flex',
                        'justify-content': 'space-between',
                        'margin-bottom': '0px'
                    }),
                    
                    html.Div([], style={
                        'width': "100%",
                        'background-color': "#0874bc",
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
                                'background-color': get_color(tryptophan_metabolism_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                                'background-color': get_color(inflam_immune_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                        'height': '18px'
                    }),       
                    
                    html.Div([
                        html.P('8. Воспалительные процессы', style={'margin': '0px', 'margin-bottom': '1px'}),
                        html.Div([
                            html.Div([
                                html.Div([], style={
                                    'width': f"{risk_scores.loc[risk_scores['Группа риска'] == 'Степень воспалительных процессов', 'Риск-скор'].values[0] * 10}%",
                                    'background-color': get_color_under_normal_dist(
                                        100-(risk_scores.loc[risk_scores['Группа риска'] == 'Степень воспалительных процессов', 'Риск-скор'].values[0] * 10)
                                    ),
                                    'border-radius': '2px',
                                    'height': '13px',
                                    'line-height': 'normal',
                                    'display': 'inline-block',
                                    'vertical-align': 'center',
                                }),
                            ], style={'display': 'flex', 'align-self': 'center','width': '70px', 'height': '13px','line-height': 'normal', 'border-radius': '2px','background-color':  'lightgrey', 'margin-left':'5px', 'margin-right':'5px'}),
                            html.B(
                                f"{risk_scores.loc[risk_scores['Группа риска'] == 'Степень воспалительных процессов', 'Риск-скор'].values[0]} из 10",
                                style={'margin': '0px'}
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
                        'margin-top': '64px'
                    }),
                    
                    html.Div([], style={
                        'width': "100%",
                        'background-color': "#0874bc",
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
                                'background-color': get_color(ido_path_tryptophan_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                                'background-color': get_color(neuromediators_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                                'background-color': get_color(indols_phenols_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                                'background-color': get_color(general_stress_immune_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                                'background-color': get_color(complex_index),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
            
            ], style={
                'display': 'flex',
                'justify-content': 'space-between',
                'height': 'fit-content',
                'margin-top': '30px'}),
            
            # Plot risk_scores table
            html.Div([
                html.Div([
                    html.Div([
                        html.P('9. Токсическая нагрузка', style={'margin': '0px', 'margin-bottom': '1px'}),
                        html.Div([
                            html.Div([
                                html.Div([], style={
                                    'width': f"{risk_scores.loc[risk_scores['Группа риска'] == 'Токсическая нагрузка и детоксикация', 'Риск-скор'].values[0] * 10}%",
                                    'background-color': get_color_under_normal_dist(
                                        100-(risk_scores.loc[risk_scores['Группа риска'] == 'Токсическая нагрузка и детоксикация', 'Риск-скор'].values[0] * 10)
                                    ),
                                    'border-radius': '2px',
                                    'height': '13px',
                                    'line-height': 'normal',
                                    'display': 'inline-block',
                                    'vertical-align': 'center',
                                }),
                            ], style={'display': 'flex', 'align-self': 'center','width': '70px', 'height': '13px','line-height': 'normal', 'border-radius': '2px','background-color':  'lightgrey', 'margin-left':'5px', 'margin-right':'5px'}),
                            html.B(
                                f"{risk_scores.loc[risk_scores['Группа риска'] == 'Токсическая нагрузка и детоксикация', 'Риск-скор'].values[0]} из 10",
                                style={'margin': '0px'}
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
                        'background-color': "#0874bc",
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
                                'background-color': get_color(amiac_detox_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                                'background-color': get_color(oxidative_stress_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                                'background-color': get_color(nitrogen_toxic_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                        html.P('11. Нутриентный статус', style={'margin': '0px', 'margin-bottom': '1px'}),
                        html.Div([
                            html.Div([
                                html.Div([], style={
                                    'width': f"{risk_scores.loc[risk_scores['Группа риска'] == 'Нутриентный статус организма', 'Риск-скор'].values[0] * 10}%",
                                    'background-color': get_color_under_normal_dist(
                                        100-(risk_scores.loc[risk_scores['Группа риска'] == 'Нутриентный статус организма', 'Риск-скор'].values[0] * 10)
                                    ),
                                    'border-radius': '2px',
                                    'height': '13px',
                                    'line-height': 'normal',
                                    'display': 'inline-block',
                                    'vertical-align': 'center',
                                }),
                            ], style={'display': 'flex', 'align-self': 'center','width': '70px', 'height': '13px','line-height': 'normal', 'border-radius': '2px','background-color':  'lightgrey', 'margin-left':'5px', 'margin-right':'5px'}),
                            html.B(
                                f"{risk_scores.loc[risk_scores['Группа риска'] == 'Нутриентный статус организма', 'Риск-скор'].values[0]} из 10",
                                style={'margin': '0px'}
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
                        'margin-top': '47px'
                    }),
                    
                    html.Div([], style={
                        'width': "100%",
                        'background-color': "#0874bc",
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
                                'background-color': get_color(vitamine_b2_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                                'background-color': get_color(vitamine_b5_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                                'background-color': get_color(vitamine_b6_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                                'background-color': get_color(vitamine_b9_b12_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                                'background-color': get_color(vitamine_b3_nad_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                                'background-color': get_color(serum_aminoacids_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                                'background-color': get_color(energy_exchange_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                                'background-color': get_color(neurotroph_reserv_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                        html.P('10. Митохондриальное здоровье', style={'margin': '0px', 'margin-bottom': '1px'}),
                        html.Div([
                            html.Div([
                                html.Div([], style={
                                    'width': f"{risk_scores.loc[risk_scores['Группа риска'] == 'Митохондриальное здоровье', 'Риск-скор'].values[0] * 10}%",
                                    'background-color': get_color_under_normal_dist(
                                        100-(risk_scores.loc[risk_scores['Группа риска'] == 'Митохондриальное здоровье', 'Риск-скор'].values[0] * 10)
                                    ),
                                    'border-radius': '2px',
                                    'height': '13px',
                                    'line-height': 'normal',
                                    'display': 'inline-block',
                                    'vertical-align': 'center',
                                }),
                            ], style={'display': 'flex', 'align-self': 'center','width': '70px', 'height': '13px','line-height': 'normal', 'border-radius': '2px','background-color':  'lightgrey', 'margin-left':'5px', 'margin-right':'5px'}),
                            html.B(
                                f"{risk_scores.loc[risk_scores['Группа риска'] == 'Митохондриальное здоровье', 'Риск-скор'].values[0]} из 10",
                                style={'margin': '0px'}
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
                        'background-color': "#0874bc",
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
                                'background-color': get_color(energy_exchange_carnitine_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                                'background-color': get_color(mitochondrial_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                    
                    # html.Div([
                    #     html.Div([
                    #         html.Div([], style={
                    #             'width': f'{100 -  antoxidant_system}%',
                    #             'background-color': get_color(antoxidant_system),
                    #             'border-radius': '5px',
                    #             'height': '10px',
                    #             'line-height': 'normal',
                    #             'display': 'inline-block',
                    #             'vertical-align': 'center'
                    #         }),
                    #     ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                    #     html.Div([
                    #         html.P('Антиоксидантная защита', style={
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
                                'width': f'{100 -   complex_index}%',
                                'background-color': get_color(complex_index),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                        html.P('12. ', style={'margin': '0px', 'margin-bottom': '1px'} ),
                        html.P('Алиментарно-зависимые заболевания', style={'margin': '0px', 'margin-bottom': '1px', 'width':'200px'}),
                        html.Div([
                            html.Div([
                                html.Div([], style={
                                    'width': f"{risk_scores.loc[risk_scores['Группа риска'] == 'Риск алиментарно-зависимых заболеваний', 'Риск-скор'].values[0] * 10}%",
                                    'background-color': get_color_under_normal_dist(
                                        100-(risk_scores.loc[risk_scores['Группа риска'] == 'Риск алиментарно-зависимых заболеваний', 'Риск-скор'].values[0] * 10)
                                    ),
                                    'border-radius': '2px',
                                    'height': '13px',
                                    'line-height': 'normal',
                                    'display': 'inline-block',
                                    'vertical-align': 'center',
                                }),
                            ], style={'display': 'flex', 'align-self': 'center','width': '70px', 'height': '13px','line-height': 'normal', 'border-radius': '2px','background-color':  'lightgrey', 'margin-left':'5px', 'margin-right':'5px'}),
                            html.B(
                                f"{risk_scores.loc[risk_scores['Группа риска'] == 'Риск алиментарно-зависимых заболеваний', 'Риск-скор'].values[0]} из 10",
                                style={'margin': '0px'}
                            )
                        ], style ={'display': 'flex', 'flex-direction': 'row', 'flex-wrap': 'nowrap', 'align-items': 'center'})
                    ],  style={
                        'color': 'black',
                        'font-family': 'Calibri',
                        'font-size': '16px',
                        'margin': '0px',
                        'display': 'flex',
                        'justify-content': 'space-between',
                        'margin-bottom': '0px',
                        'margin-top': '28px'
                    }),
                    
                    html.Div([], style={
                        'width': "100%",
                        'background-color': "#0874bc",
                        'height': '2px',
                        'line-height': 'normal',
                        'display': 'inline-block',
                        'vertical-align': 'center',
                        'margin-bottom':'2px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 -  over_sugar_score}%',
                                'background-color': get_color(over_sugar_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Избыток сахара / углеводов', style={
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
                                'width': f'{100 -  over_lipid_score}%',
                                'background-color': get_color(over_lipid_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Избыток жиров / липидов', style={
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
                                'width': f'{100 - over_protein_score}%',
                                'background-color': get_color(over_protein_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Избыток белка / аминокислот', style={
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
                                'width': f'{100 - deficit_nutrients_score}%',
                                'background-color': get_color(deficit_nutrients_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Дефицит нутриентов', style={
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
                                'width': f'{100 -  supply_score}%',
                                'background-color': get_color(supply_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Нарушение пищевого поведения', style={
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
                        html.P('13. Обмен веществ', style={'margin': '0px', 'margin-bottom': '1px'}),
                        html.Div([
                            html.Div([
                                html.Div([], style={
                                    'width': f"{risk_scores.loc[risk_scores['Группа риска'] == 'Обмен веществ', 'Риск-скор'].values[0] * 10}%",
                                    'background-color': get_color_under_normal_dist(
                                        100-(risk_scores.loc[risk_scores['Группа риска'] == 'Обмен веществ', 'Риск-скор'].values[0] * 10)
                                    ),
                                    'border-radius': '2px',
                                    'height': '13px',
                                    'line-height': 'normal',
                                    'display': 'inline-block',
                                    'vertical-align': 'center',
                                }),
                            ], style={'display': 'flex', 'align-self': 'center','width': '70px', 'height': '13px','line-height': 'normal', 'border-radius': '2px','background-color':  'lightgrey', 'margin-left':'5px', 'margin-right':'5px'}),
                            html.B(
                                f"{risk_scores.loc[risk_scores['Группа риска'] == 'Обмен веществ', 'Риск-скор'].values[0]} из 10",
                                style={'margin': '0px'}
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
                        'background-color': "#0874bc",
                        'height': '2px',
                        'line-height': 'normal',
                        'display': 'inline-block',
                        'vertical-align': 'center',
                        'margin-bottom':'2px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 -  aa_exchange }%',
                                'background-color': get_color( aa_exchange ),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Аминокислотный обмен', style={
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
                                'width': f'{100 -  sug_exchange}%',
                                'background-color': get_color(sug_exchange),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Углеводный обмен', style={
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
                                'width': f'{100 -  lip_exchange}%',
                                'background-color': get_color(lip_exchange),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Липидный обмен', style={
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
                                'width': f'{100 -  insulin_exchange}%',
                                'background-color': get_color(insulin_exchange),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Инсулинорезистентность', style={
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
                                'width': f'{100 -  insuline_resistance_score}%',
                                'background-color': get_color(insuline_resistance_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Инсулинорезистентность', style={
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
                                'width': f'{100 -  hormone_exchange}%',
                                'background-color': get_color(hormone_exchange),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Гормональные связи', style={
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
                        html.P('15. ', style={'margin': '0px', 'margin-bottom': '1px'} ),
                        html.P('Нейродегенеративные заболевания', style={'margin': '0px', 'margin-bottom': '1px', 'width':'200px'}),
                        html.Div([
                            html.Div([
                                html.Div([], style={
                                    'width': f"{risk_scores.loc[risk_scores['Группа риска'] == 'Риск нейродегенеративных заболеваний', 'Риск-скор'].values[0] * 10}%",
                                    'background-color': get_color_under_normal_dist(
                                        100-(risk_scores.loc[risk_scores['Группа риска'] == 'Риск нейродегенеративных заболеваний', 'Риск-скор'].values[0] * 10)
                                    ),
                                    'border-radius': '2px',
                                    'height': '13px',
                                    'line-height': 'normal',
                                    'display': 'inline-block',
                                    'vertical-align': 'center',
                                }),
                            ], style={'display': 'flex', 'align-self': 'center','width': '70px', 'height': '13px','line-height': 'normal', 'border-radius': '2px','background-color':  'lightgrey', 'margin-left':'5px', 'margin-right':'5px'}),
                            html.B(
                                f"{risk_scores.loc[risk_scores['Группа риска'] == 'Риск нейродегенеративных заболеваний', 'Риск-скор'].values[0]} из 10",
                                style={'margin': '0px'}
                            )
                        ], style ={'display': 'flex', 'flex-direction': 'row', 'flex-wrap': 'nowrap', 'align-items': 'center'})
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
                        'background-color': "#0874bc",
                        'height': '2px',
                        'line-height': 'normal',
                        'display': 'inline-block',
                        'vertical-align': 'center',
                        'margin-bottom':'2px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 -  ido_neuroinflam_score}%',
                                'background-color': get_color(ido_neuroinflam_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Обмен метионина и метилирование', style={
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
                    #             'width': f'{100 -  antoxidant_system}%',
                    #             'background-color': get_color(antoxidant_system),
                    #             'border-radius': '5px',
                    #             'height': '10px',
                    #             'line-height': 'normal',
                    #             'display': 'inline-block',
                    #             'vertical-align': 'center'
                    #         }),
                    #     ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                    #     html.Div([
                    #         html.P('Антиоксидантная система', style={
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
                                'width': f'{100 -  disbalance_metabolites_score}%',
                                'background-color': get_color(disbalance_metabolites_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Дисбаланс метаболитов', style={
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
                                'width': f'{100 -  neuromediators_neuro_score}%',
                                'background-color': get_color(neuromediators_neuro_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                                'width': f'{100 -  mitochondria_stress_score}%',
                                'background-color': get_color(mitochondria_stress_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Митохондрии и стресс', style={
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
                        html.P('14. Онкологические заболевания', style={'margin': '0px', 'margin-bottom': '1px'}),
                        html.Div([
                            html.Div([
                                html.Div([], style={
                                    'width': f"{risk_scores.loc[risk_scores['Группа риска'] == 'Риск онкологических заболеваний', 'Риск-скор'].values[0] * 10}%",
                                    'background-color': get_color_under_normal_dist(
                                        100-(risk_scores.loc[risk_scores['Группа риска'] == 'Риск онкологических заболеваний', 'Риск-скор'].values[0] * 10)
                                    ),
                                    'border-radius': '2px',
                                    'height': '13px',
                                    'line-height': 'normal',
                                    'display': 'inline-block',
                                    'vertical-align': 'center',
                                }),
                            ], style={'display': 'flex', 'align-self': 'center','width': '70px', 'height': '13px','line-height': 'normal', 'border-radius': '2px','background-color':  'lightgrey', 'margin-left':'5px', 'margin-right':'5px'}),
                            html.B(
                                f"{risk_scores.loc[risk_scores['Группа риска'] == 'Риск онкологических заболеваний', 'Риск-скор'].values[0]} из 10",
                                style={'margin': '0px'}
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
                        'margin-top': '10px'
                    }),
                    
                    html.Div([], style={
                        'width': "100%",
                        'background-color': "#0874bc",
                        'height': '2px',
                        'line-height': 'normal',
                        'display': 'inline-block',
                        'vertical-align': 'center',
                        'margin-bottom':'2px'
                    }),
                    
                    html.Div([
                        html.Div([
                            html.Div([], style={
                                'width': f'{100 - chronic_inflamm_score}%',
                                'background-color': get_color(chronic_inflamm_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Хроническое воспаление', style={
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
                                'width': f'{100 -  ox_stress_score}%',
                                'background-color': get_color(ox_stress_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
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
                                'width': f'{100 -   metil_epigen_score}%',
                                'background-color': get_color( metil_epigen_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Метилирование / эпигенетика', style={
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
                                'width': f'{100 -    microbiota_detox_score }%',
                                'background-color': get_color( microbiota_detox_score ),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Микробиота и детоксикация', style={
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
                                'width': f'{100 -     metabolic_stress_score }%',
                                'background-color': get_color(  metabolic_stress_score ),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Метаболический стресс', style={
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
                                'width': f'{100 - neuro_endocrine_controle_score }%',
                                'background-color': get_color(neuro_endocrine_controle_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Нейроэндокринный контроль', style={
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
                                'width': f'{100 - prolifiration_mitosis_score}%',
                                'background-color': get_color(prolifiration_mitosis_score),
                                'border-radius': '5px',
                                'height': '10px',
                                'line-height': 'normal',
                                'display': 'inline-block',
                                'vertical-align': 'center'
                            }),
                        ], style={'width': '23%', 'height': '18px', 'line-height': '18px'}),
                        html.Div([
                            html.P('Пролиферация и митоз', style={
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
                    
               
                html.Div(
                style={'maxWidth': 'auto'},
                children=[
                    # Header
                    html.Div(
                        style={
                            'backgroundColor': '#0874bc',
                            'color': 'white',
                            'padding': '5px 15px',
                            'borderTopLeftRadius': '4px',
                            'borderTopRightRadius': '4px',
                            'margin-top': '20px'
                        },
                        children=[
                            html.H2('Общая оценка метаболизма', style={'margin': '0', 'font-family': 'Calibri', 'font-size': '16px'})
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
                                style={'display': 'flex', 'marginBottom': '7px'},
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
                                                    'font-family': 'Calibri', 
                                                    'font-size': '14px'
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
                                                    'font-family': 'Calibri', 
                                                    'font-size': '14px'
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
                                                    'font-family': 'Calibri', 
                                                    'font-size': '14px'
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
                                                    'font-family': 'Calibri', 
                                                    'font-size': '14px'
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
                                                            'font-family': 'Calibri' 
                                                        },
                                                        children=[
                                                            # Corrected sum calculation
                                                            f"{int(round(pd.to_numeric(risk_scores['Риск-скор'], errors='coerce').sum() * 100 / 150, 0))}",
                                                            html.Span(
                                                                '/100%',
                                                                style={
                                                                    'fontSize': '16px',
                                                                    'color': '#666',
                                                                    'marginLeft': '5px',
                                                                    'font-family': 'Calibri' 
                                                                }
                                                            )
                                                        ]
                                                    ),
                                                    html.Div(
                                                        # Dynamic status based on score
                                                        children=[
                                                            html.Span(
                                                                'Отлично' if (pd.to_numeric(risk_scores['Риск-скор'], errors='coerce').sum()* 100 / 150) >= 90
                                                                else 'Хорошо' if (pd.to_numeric(risk_scores['Риск-скор'], errors='coerce').sum()* 100 / 150) >= 67
                                                                else 'Требуется коррекция' if (pd.to_numeric(risk_scores['Риск-скор'], errors='coerce').sum()* 100 / 150) >= 50
                                                                else 'Серьезные нарушения'
                                                            )
                                                        ],
                                                        style={
                                                            'backgroundColor': '#e8f5e9' if (pd.to_numeric(risk_scores['Риск-скор'], errors='coerce').sum()* 100 / 150) >= 90
                                                            else '#fff3e0' if (pd.to_numeric(risk_scores['Риск-скор'], errors='coerce').sum()* 100 / 150 ) >= 67
                                                            else '#ffebee' if (pd.to_numeric(risk_scores['Риск-скор'], errors='coerce').sum()) >= 50
                                                            else '#ffcdd2',
                                                            'color':'#50c150' if (pd.to_numeric(risk_scores['Риск-скор'], errors='coerce').sum()* 100 / 150) >= 100
                                                            else '#fe991d' if (pd.to_numeric(risk_scores['Риск-скор'], errors='coerce').sum())* 100 / 150 >= 67
                                                            else '#f25708' if (pd.to_numeric(risk_scores['Риск-скор'], errors='coerce').sum())* 100 / 150 >= 50
                                                            else '#f21f08',
                                                            'padding': '5px 15px',
                                                            'borderRadius': '15px',
                                                            'display': 'inline-block',
                                                            'font-family': 'Calibri',
                                                            'font-weight': 'bold',
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
                    
                ], style={'width': '48%', 'height': 'fit-content'}),
            
            
            
            ], style={
                'display': 'flex',
                'justify-content': 'space-between',
                'height': 'fit-content',
                'margin-top': '5px'}),
            
            html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
                   style={'page-break-after': 'always','color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"left",'font-style':'italic','margin-top':'20px'}),
            
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
                ], style={'display':'flex', 'justify-content':'space-between','width':'100%','height':'54px','color':'#0874bc'}),    
                html.Div([
                html.H3(children='1. Аминокислоты', style={'textAlign':'left','margin':'0px','line-height':'normal','display':'inline-block','vertical-align':'center'}),]
                    , style={'width':'100%','background-color':'#0874bc', 'color':'white','font-family':'Calibri','margin':'0px','height':'35px','line-height':'35px','text-align':'center','margin-top':'5px'}),
                html.Div([
                    html.Div([
                    html.Div([
                        html.Div([html.B('Метаболизм фенилаланина',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'40px'}),
                        html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'black','text-align':'center'}),
                    ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Фенилаланин (Phe)',style={'height':'20px'}),html.P('Незаменимая глюко-, кетогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_1[0],ref_1[0])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_1[0]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_1[0],ref_1[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_1[0],ref_1[0])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_1[0], ref_1[0])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_1[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Тирозин (Tyr)',style={'height':'20px'}),html.P('Заменимая глюко-, кетогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_1[1],ref_1[1])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_1[1]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_1[1],ref_1[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_1[1],ref_1[1])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_1[1], ref_1[1])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_1[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Индекс ААAs [Phe + Tyr]',style={'height':'20px'}),html.P('Запас ароматических аминокислот ',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_1[2],ref_1[2])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_1[2]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_1[2],ref_1[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_1[2],ref_1[2])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_1[2], ref_1[2])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_1[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.B('Лейцин + Изолейцин (Leu+Ile)', style={'height': '20px'}),
                                    html.P('Незаменимая глюко-, кетогенная аминокислота', 
                                        style={'height': '20px', 'font-size': '12px', 'font-family': 'Calibri', 
                                                'color': '#39507c', 'margin': '0px', 'margin-left': '5px', 
                                                'line-height': '0.9em'})
                                ], style={'width': '39%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': 'black', 'margin-top': '5px'}),
                                
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            html.B(f'{need_of_plus_minus(value_2[0],ref_2[0])}', 
                                                style={'width': '30%', 'text-align': 'left'}),
                                            html.B(f'{value_2[0]}', 
                                                style={'text-align': 'right', 'width': '50%'})
                                        ], style={'width': '100%', 'display': 'flex', 'justify-content': 'space-between', 
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_2[1], ref_2[1])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
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
                                html.Div([html.B('Валин (Val)',style={'height':'20px'}),html.P('Незаменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_2[1],ref_2[1])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_2[1]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_2[1],ref_2[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_2[1],ref_2[1])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_2[1], ref_2[1])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_2[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Индекс ВСААs [Leu + Ile + Val]',style={'height':'20px'}),html.P('Запас аминокислот с разветвленной боковой цепью',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_2[2],ref_2[2])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_2[2]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_2[2],ref_2[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_2[2],ref_2[2])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_2[2], ref_2[2])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_2[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Индекс Фишера FR [BCAAs / AAAs]',style={'height':'20px'}),html.P('Отношение запаса аминокислот с разветвленной цепью к запасу ароматических аминокислот',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_2[3],ref_2[3])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_2[3]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_2[3],ref_2[3])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_2[3],ref_2[3])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_2[3], ref_2[3])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_2[3]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    
                    html.Div([
                    html.Div([
                        html.Div([html.B('Метаболизм гистидина',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'40px'}),
                        html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'black','text-align':'center'}),
                    ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Гистидин (His)',style={'height':'20px'}),html.P('Незаменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_3[0],ref_3[0])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_3[0]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_3[0],ref_3[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_3[0],ref_3[0])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_3[0], ref_3[0])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_3[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Метилгистидин (MH)',style={'height':'20px'}),html.P('Метаболит карнозина',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_3[1],ref_3[1])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_3[1]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_3[1],ref_3[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_3[1],ref_3[1])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_3[1], ref_3[1])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_3[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Треонин (Thr)',style={'height':'20px'}),html.P('Незаменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_3[2],ref_3[2])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_3[2]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_3[2],ref_3[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_3[2],ref_3[2])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_3[2], ref_3[2])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_3[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Карнозин (Car)',style={'height':'20px'}),html.P('Дипептид, состоящий из аланина и гистидина',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_3[3],ref_3[3])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_3[3]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_3[3],ref_3[3])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_3[3],ref_3[3])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_3[3], ref_3[3])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_3[3]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Глицин (Gly)',style={'height':'20px'}),html.P('Заменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_3[4],ref_3[4])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_3[4]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_3[4],ref_3[4])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_3[4],ref_3[4])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_3[4], ref_3[4])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_3[4]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Диметилглицин (DMG)',style={'height':'20px'}),html.P('Промежуточный продукт синтеза глицина',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_3[5],ref_3[5])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_3[5]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_3[5],ref_3[5])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_3[5],ref_3[5])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_3[5], ref_3[5])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_3[5]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Серин (Ser)',style={'height':'20px'}),html.P('Заменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_3[6],ref_3[6])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_3[6]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_3[6],ref_3[6])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_3[6],ref_3[6])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_3[6], ref_3[6])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_3[6]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Лизин (Lys)',style={'height':'20px'}),html.P('Незаменимая кетогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_3[7],ref_3[7])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_3[7]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_3[7],ref_3[7])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_3[7],ref_3[7])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_3[7], ref_3[7])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_3[7]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Глутаминовая кислота (Glu)',style={'height':'20px'}),html.P('Заменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_3[8],ref_3[8])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_3[8]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_3[8],ref_3[8])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_3[8],ref_3[8])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_3[8], ref_3[8])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_3[8]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                ], style={'margin':'0px'}),
                html.Div([
                    html.Div([
                        html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
                            style={'color':'black', 'font-family':'Calibri', 'font-size':'14px', 
                                    'margin':'0px', 'text-align':"left", 'font-style':'italic',
                                    'margin-top':'5px', 'width':'85%'}),
                        html.P('|1',
                            style={'color':'black', 'font-family':'Calibri', 'font-size':'14px', 
                                    'margin':'0px', 'text-align':"right", 'font-style':'italic',
                                    'margin-top':'5px', 'width':'10%'}),
                    ], style={'display':'flex', 'justify-content':'space-between', 'width':'100%', 
                            'position': 'absolute', 'left': '0', 'padding': '0'})
                ], style={'position': 'relative', 'height': '60px', 'width': '100%', 'margin-top': '20px'}),
            
            
            
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
                ], style={'display':'flex', 'justify-content':'space-between','width':'100%','height':'53px','color':'#0874bc'}),    
                
                html.Div([
                    html.Div([
                    html.Div([
                        html.Div([html.B('Метаболизм гистидина',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'40px'}),
                        html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'black','text-align':'center'}),
                    ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Глутамин (Gln)',style={'height':'20px'}),html.P('Заменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_3[9],ref_3[9])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_3[9]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_3[9],ref_3[9])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_3[9],ref_3[9])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_3[9], ref_3[9])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_3[9]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Индекс [Gln / Glu]',style={'height':'20px'}),html.P('Активность глутаминсинтетазы',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_3[10],ref_3[10])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_3[10]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_3[10],ref_3[10])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_3[10],ref_3[10])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_3[10], ref_3[10])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_3[10]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Индекс GSG [Glu / (Ser + Gly)]',style={'height':'20px'}),html.P('Запас аминокислот для синтеза глутатиона',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_3[11],ref_3[11])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_3[11]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_3[11],ref_3[11])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_3[11],ref_3[11])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_3[11], ref_3[11])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_3[11]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    # html.Div([
                    #     html.Div([
                    #         html.Div([
                    #             html.Div([html.B('Индекс [Gly / Ser]',style={'height':'20px'}),html.P('Активность глутаминсинтетазы',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                    #             html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_3[12],ref_3[12])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_3[10]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_3[10],ref_3[10])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_3[10],ref_3[10])}','line-height':'53px'}),
                    #                                     # Progress bar with pointer
                    #             html.Div([
                    #                 # Progress bar
                    #                 html.Img(src=app.get_asset_url('progress.png'), 
                    #                         style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                    #                             'display': 'inline-block', 'vertical-align': 'center'}),
                    #                 # Pointer (arrow)
                    #                 html.Img(src=app.get_asset_url('pointer.png'), 
                    #                         style={
                    #                             'position': 'absolute',
                    #                             'height': '12px',
                    #                             'width': '12px',
                    #                             'left': f'{calculate_pointer_position(value_3[12], ref_3[12])}%',
                    #                             'top': '8px',
                    #                             'transform': 'translateX(-50%)'
                    #                         })
                    #             ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                    #                     'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                    #                     'position': 'relative'}),
                    #             html.Div([html.P(f'{ref_3[10]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                    #         ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                    #     ], style={'margin':'0px','margin-left':'20px'}),
                    # ],style={'margin':'0px',}),
                    
                    html.Div([
                    html.Div([
                        html.Div([html.B('Метаболизм метионина',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'40px'}),
                        html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'black','text-align':'center'}),
                    ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Метионин (Met)',style={'height':'20px'}),html.P('Незаменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_4[0],ref_4[0])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_4[0]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_4[0],ref_4[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_4[0],ref_4[0])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_4[0],ref_4[0])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_4[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Метионин сульфоксид (MetSO4)',style={'height':'20px'}),html.P('Продукт окисления метионина',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_4[1],ref_4[1])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_4[1]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_4[1],ref_4[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_4[1],ref_4[1])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_4[1],ref_4[1])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_4[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    # html.Div([
                    #     html.Div([
                    #         html.Div([
                    #             html.Div([html.B('Цистатионин (Cys)',style={'height':'20px'}),html.P('Серосодержащая аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                    #             html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_4[2],ref_4[2])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_4[2]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_4[2],ref_4[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_4[2],ref_4[2])}','line-height':'53px'}),
                    #                                     # Progress bar with pointer
                                # html.Div([
                                #     # Progress bar
                                #     html.Img(src=app.get_asset_url('progress.png'), 
                                #             style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                #                 'display': 'inline-block', 'vertical-align': 'center'}),
                                #     # Pointer (arrow)
                                #     html.Img(src=app.get_asset_url('pointer.png'), 
                                #             style={
                                #                 'position': 'absolute',
                                #                 'height': '12px',
                                #                 'width': '12px',
                                #                 'left': f'{calculate_pointer_position(value_15[0], ref_15[0])}%',
                                #                 'top': '8px',
                                #                 'transform': 'translateX(-50%)'
                                #             })
                                # ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                #         'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                #         'position': 'relative'}),
                    #             html.Div([html.P(f'{ref_4[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                    #         ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                    #     ], style={'margin':'0px','margin-left':'20px'}),
                    # ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Таурин (Tau)',style={'height':'20px'}),html.P('Заменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_4[2],ref_4[2])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_4[2]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_4[2],ref_4[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_4[2],ref_4[2])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_4[2],ref_4[2])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_4[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Бетаин (Bet)',style={'height':'20px'}),html.P('Продукт метаболизма холина',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_4[3],ref_4[3])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_4[3]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_4[3],ref_4[3])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_4[3],ref_4[3])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_4[3],ref_4[3])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_4[3]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Холин (Chl)',style={'height':'20px'}),html.P('Компонент мембран клеток, источник ацетилхолина',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_4[4],ref_4[4])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_4[4]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_4[4],ref_4[4])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_4[4],ref_4[4])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_4[4],ref_4[4])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_4[4]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Триметиламин-N-оксид (TMAO)',style={'height':'20px'}),html.P('Продукт метаболизма холина, бетаина и др. бактериями ЖКТ',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_4[5],ref_4[5])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_4[5]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_4[5],ref_4[5])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_4[5],ref_4[5])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_4[5],ref_4[5])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_4[5]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Индекс Bet / Chl',style={'height':'20px'}),html.P('Соотношение бетаина к холину',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_4[6],ref_4[6])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_4[6]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_4[6],ref_4[6])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_4[6],ref_4[6])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_4[6],ref_4[6])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_4[6]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    html.Div([
                html.H3(children='2. Метаболизм триптофана', style={'textAlign':'center','margin':'0px','line-height':'normal','display':'inline-block','vertical-align':'center'}),]
                    , style={'width':'100%','background-color':'#0874bc', 'color':'white','font-family':'Calibri','margin':'0px','height':'35px','line-height':'35px','text-align':'center','margin-top':'5px'}),
                    html.Div([
                    html.Div([
                        html.Div([html.B('Кинурениновый путь',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'40px'}),
                        html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'black','text-align':'center'}),
                    ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Триптофан (Trp)',style={'height':'20px'}),html.P('Незаменимая глюко-, кетогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_5[0],ref_5[0])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_5[0]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_5[0],ref_5[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_5[0],ref_5[0])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_5[0],ref_5[0])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_5[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Кинуренин (Kyn)',style={'height':'20px'}),html.P('Продукт метаболизма триптофана по кинурениновому пути',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_5[1],ref_5[1])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_5[1]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_5[1],ref_5[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_5[1],ref_5[1])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_5[1],ref_5[1])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_5[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Индекс Kyn / Trp',style={'height':'20px'}),html.P('Показывает активность ферментов, метаболизирующих триптофан до кинуренина',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_5[2],ref_5[2])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_5[2]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_5[2],ref_5[5])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_5[2],ref_5[2])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_5[2],ref_5[2])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_5[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Антраниловая кислота (Ant)',style={'height':'20px'}),html.P('Продукт метаболизма кинуренина',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_5[3],ref_5[3])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_5[3]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_5[3],ref_5[3])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_5[3],ref_5[3])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_5[3],ref_5[3])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_5[3]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    # html.Div([
                    #     html.Div([
                    #         html.Div([
                    #             html.Div([html.B('3-Гидроксиантраниловая кислота',style={'height':'20px'}),html.P('Продукт метаболизма антраниловой кислоты',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                    #             html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_5[4],ref_5[4])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_5[4]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_5[4],ref_5[4])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_5[4],ref_5[4])}','line-height':'53px'}),
                    #                                     # Progress bar with pointer
                                # html.Div([
                                #     # Progress bar
                                #     html.Img(src=app.get_asset_url('progress.png'), 
                                #             style={'width': '100%', 'height': '18px', 'line-height': 'normal', 
                                #                 'display': 'inline-block', 'vertical-align': 'center'}),
                                #     # Pointer (arrow)
                                #     html.Img(src=app.get_asset_url('pointer.png'), 
                                #             style={
                                #                 'position': 'absolute',
                                #                 'height': '12px',
                                #                 'width': '12px',
                                #                 'left': f'{calculate_pointer_position(value_15[0], ref_15[0])}%',
                                #                 'top': '8px',
                                #                 'transform': 'translateX(-50%)'
                                #             })
                                # ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                #         'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                #         'position': 'relative'}),
                    #             html.Div([html.P(f'{ref_5[4]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                    #         ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                    #     ], style={'margin':'0px','margin-left':'20px'}),
                    # ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Хинолиновая кислота (Qnl)',style={'height':'20px'}),html.P('Продукт метаболизма 3-гидроксиантраниловой кислоты',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_5[4],ref_5[4])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_5[4]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_5[4],ref_5[4])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_5[4],ref_5[4])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_5[4],ref_5[4])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_5[4]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                                html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Ксантуреновая кислота (Xnt)',style={'height':'20px'}),html.P('Продукт метаболизма кинуренина',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_5[5],ref_5[5])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_5[5]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_5[5],ref_5[5])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_5[5],ref_5[5])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_5[5],ref_5[5])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_5[5]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                ], style={'margin':'0px'}),
            ]),
            html.Div([
                html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
                style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"left",'font-style':'italic','margin-top':'5px','width':'85%'}),
                html.P('|2',
                    style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"right",'font-style':'italic','margin-top':'5px','width':'10%','margin-top':'20px'}),
            ], style={'page-break-after': 'always','margin':'0px','display':'flex','justify-content':'space-between','width':'100%','margin-top':'5px'}),
            
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
                ], style={'display':'flex', 'justify-content':'space-between','width':'100%','height':'53px','color':'#0874bc'}),    
                
                html.Div([
                    html.Div([
                    html.Div([
                        html.Div([html.B('Кинурениновый путь',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'40px'}),
                        html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'black','text-align':'center'}),
                    ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    

                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Кинуреновая кислота (Kyna)',style={'height':'20px'}),html.P('Продукт метаболизма кинуренина',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_5[6],ref_5[6])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_5[6]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_5[6],ref_5[6])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_5[6],ref_5[6])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_5[6],ref_5[6])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_5[6]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Индекс Kyna / Qnl',style={'height':'20px'}),html.P('Соотношение кинуренина к хинолиновой кислоте',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_5[7],ref_5[7])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_5[7]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_5[7],ref_5[7])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_5[7],ref_5[7])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_5[7],ref_5[7])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_5[7]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    
                    html.Div([
                    html.Div([
                        html.Div([html.B('Серотониновый путь',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'40px'}),
                        html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'black','text-align':'center'}),
                    ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Серотонин',style={'height':'20px'}),html.P('Нейромедиатор',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_6[0],ref_6[0])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_6[0]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_6[0],ref_6[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_6[0],ref_6[0])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_6[0],ref_6[0])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_6[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('5-Гидроксииндолуксусная кислота (5-HIAA)',style={'height':'20px'}),html.P('Метаболит серотонина',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_6[1],ref_6[1])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_6[1]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_6[1],ref_6[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_6[1],ref_6[1])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_6[1],ref_6[1])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_6[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Индекс 5-HIAA / Qnl',style={'height':'20px'}),html.P('Соотношение 5-гидроксииндолуксусной кислоты к хинолиновой кислоте',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_6[2],ref_6[2])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_6[2]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_6[2],ref_6[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_6[2],ref_6[2])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_6[2],ref_6[2])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_6[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('5-Гидрокситриптофан (5-HTP)',style={'height':'20px'}),html.P('Прекурсор серотонина',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_6[3],ref_6[3])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_6[3]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_6[3],ref_6[3])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_6[3],ref_6[3])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_6[3],ref_6[3])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_6[3]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    
                    html.Div([
                    html.Div([
                        html.Div([html.B('Индоловый путь',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'40px'}),
                        html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'black','text-align':'center'}),
                    ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('3-Индолуксусная кислота (I3A)',style={'height':'20px'}),html.P('Продукт катаболизма триптофана кишечной микробиотой',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_7[0],ref_7[0])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_7[0]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_7[0],ref_7[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_7[0],ref_7[0])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_7[0],ref_7[0])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_7[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('3-Индолмолочная кислота (I3L)',style={'height':'20px'}),html.P('Продукт катаболизма триптофана кишечной микробиотой',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_7[1],ref_7[1])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_7[1]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_7[1],ref_7[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_7[1],ref_7[1])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_7[1],ref_7[1])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_7[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('3-Индолкарбоксальдегид (I3Al)',style={'height':'20px'}),html.P('Продукт катаболизма триптофана кишечной микробиотой',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_7[2],ref_7[2])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_7[2]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_7[2],ref_7[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_7[2],ref_7[2])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_7[2],ref_7[2])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_7[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('3-Индолпропионовая кислота (I3P)',style={'height':'20px'}),html.P('Продукт катаболизма триптофана кишечной микробиотой',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_7[3],ref_7[3])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_7[3]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_7[3],ref_7[3])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_7[3],ref_7[3])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_7[3],ref_7[3])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_7[3]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('3-Индолмасляная кислота (I3B)',style={'height':'20px'}),html.P('Продукт катаболизма триптофана кишечной микробиотой',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_7[4],ref_7[4])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_7[4]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_7[4],ref_7[4])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_7[4],ref_7[4])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_7[4],ref_7[4])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_7[4]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Триптамин',style={'height':'20px'}),html.P('Продукт катаболизма триптофана кишечной микробиотой, прекурсор для нейромедиаторов',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_7[5],ref_7[5])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_7[5]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_7[5],ref_7[5])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_7[5],ref_7[5])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_7[5],ref_7[5])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_7[5]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    html.Div([
                html.H3(children='3. Метаболизм аргинина', style={'textAlign':'center','margin':'0px','line-height':'normal','display':'inline-block','vertical-align':'center'}),]
                    , style={'width':'100%','background-color':'#0874bc', 'color':'white','font-family':'Calibri','margin':'0px','height':'35px','line-height':'35px','text-align':'center','margin-top':'5px'}),
                    html.Div([
                    html.Div([
                        html.Div([html.B('Метаболизм аргинина',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'40px'}),
                        html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'black','text-align':'center'}),
                    ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Пролин (Pro)',style={'height':'20px'}),html.P('Заменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_8[0],ref_8[0])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_8[0]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_8[0],ref_8[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_8[0],ref_8[0])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_8[0],ref_8[0])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_8[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Гидроксипролин (Hyp)',style={'height':'20px'}),html.P('Источник коллагена',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_8[1],ref_8[1])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_8[1]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_8[1],ref_8[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_8[1],ref_8[1])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_8[1],ref_8[1])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_8[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Асимметричный диметиларгинин (ADMA)',style={'height':'20px'}),html.P('Эндогенный ингибитор синтазы оксида азота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_8[2],ref_8[2])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_8[2]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_8[2],ref_8[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_8[2],ref_8[2])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_8[2],ref_8[2])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_8[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    
                ], style={'margin':'0px'}),
            ]),
            html.Div([
                html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
                style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"left",'font-style':'italic','margin-top':'5px','width':'85%'}),
                html.P('|3',
                    style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"right",'font-style':'italic','margin-top':'5px','width':'10%','margin-top':'20px'}),
            ], style={'page-break-after': 'always','margin':'0px','display':'flex','justify-content':'space-between','width':'100%','margin-top':'15px'}),
            
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
                ], style={'display':'flex', 'justify-content':'space-between','width':'100%','height':'53px','color':'#0874bc'}),    
                
                html.Div([
                    html.Div([
                    html.Div([
                        html.Div([html.B('Метаболизм аргинина',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'40px'}),
                        html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'black','text-align':'center'}),
                    ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Монометиларгинин (MMA)',style={'height':'20px'}),html.P('Эндогенный ингибитор синтазы оксида азота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_8[14],ref_8[14])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_8[14]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_8[14],ref_8[14])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_8[14],ref_8[14])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_8[14],ref_8[14])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_8[14]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Симметричный диметиларгинин (SDMA)',style={'height':'20px'}),html.P('Продукт метаболизма аргинина, выводится с почками',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_8[3],ref_8[3])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_8[3]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_8[3],ref_8[3])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_8[3],ref_8[3])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_8[3],ref_8[3])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_8[3]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Гомоаргинин',style={'height':'20px'}),html.P('Субстрат для синтазы оксида азота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_8[4],ref_8[4])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_8[4]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_8[4],ref_8[4])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_8[4],ref_8[4])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_8[4],ref_8[4])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_8[4]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Аргинин',style={'height':'20px'}),html.P('Незаменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_8[5],ref_8[5])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_8[5]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_8[5],ref_8[5])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_8[5],ref_8[5])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_8[5],ref_8[5])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_8[5]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Цитруллин (Cit)',style={'height':'20px'}),html.P('Метаболит цикла мочевины',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_8[6],ref_8[6])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_8[6]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_8[6],ref_8[6])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_8[6],ref_8[6])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_8[6],ref_8[6])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_8[6]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Орнитин (Orn)',style={'height':'20px'}),html.P('Метаболит цикла мочевины',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_8[7],ref_8[7])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_8[7]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_8[7],ref_8[7])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_8[7],ref_8[7])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_8[7],ref_8[7])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_8[7]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Аспарагин (Asn)',style={'height':'20px'}),html.P('Заменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_8[8],ref_8[8])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_8[8]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_8[8],ref_8[8])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_8[8],ref_8[8])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_8[8],ref_8[8])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_8[8]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Аспарагиновая кислота (Asp)',style={'height':'20px'}),html.P('Заменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_8[9],ref_8[9])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_8[9]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_8[9],ref_8[9])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_8[9],ref_8[9])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_8[9],ref_8[9])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_8[9]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Индекс GABR [Arg / (Orn + Cit)]',style={'height':'20px'}),html.P('Общая биодоступность аргинина',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_8[10],ref_8[10])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_8[10]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_8[10],ref_8[10])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_8[10],ref_8[10])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_8[10],ref_8[10])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_8[10]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Индекс AOR [Arg / Orn]',style={'height':'20px'}),html.P('Показывает активность аргиназы',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_8[11],ref_8[11])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_8[11]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_8[11],ref_8[11])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_8[11],ref_8[11])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_8[11],ref_8[11])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_8[11]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Индекс Asn / Asp',style={'height':'20px'}),html.P('Показывает активность аспарагинсинтетазы',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_8[12],ref_8[12])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_8[12]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_8[12],ref_8[12])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_8[12],ref_8[12])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_8[12],ref_8[12])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_8[12]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Креатинин',style={'height':'20px'}),html.P('Продукт метаболизма аргинина',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_8[13],ref_8[13])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_8[13]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_8[13],ref_8[13])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_8[13],ref_8[13])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_8[13],ref_8[13])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_8[13]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    html.Div([
                html.H3(children='4. Метаболизм жирных кислот', style={'textAlign':'center','margin':'0px','line-height':'normal','display':'inline-block','vertical-align':'center'}),]
                    , style={'width':'100%','background-color':'#0874bc', 'color':'white','font-family':'Calibri','margin':'0px','height':'35px','line-height':'35px','text-align':'center','margin-top':'5px'}),
                    html.Div([
                    html.Div([
                        html.Div([html.B('Метаболизм ацилкарнитинов',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'40px'}),
                        html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'black','text-align':'center'}),
                    ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Аланин',style={'height':'20px'}),html.P('Заменимая глюкогенная аминокислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_9[0],ref_9[0])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_9[0]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_9[0],ref_9[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_9[0],ref_9[0])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_9[0],ref_9[0])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_9[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Карнитин (C0)',style={'height':'20px'}),html.P('Основа для ацилкарнитинов, транспорт жирных кислот',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_9[1],ref_9[1])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_9[1]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_9[1],ref_9[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_9[1],ref_9[1])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_9[1],ref_9[1])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_9[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Ацетилкарнитин (C2)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_9[2],ref_9[2])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_9[2]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_9[2],ref_9[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_9[2],ref_9[2])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_9[2],ref_9[2])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_9[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    
                    html.Div([
                    html.Div([
                        html.Div([html.B('Короткоцепочечные ацилкарнитины',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'40px'}),
                        html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'black','text-align':'center'}),
                    ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Пропионилкарнитин (С3)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_10[0],ref_10[0])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_10[0]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_10[0],ref_10[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_10[0],ref_10[0])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_10[0],ref_10[0])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_10[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    
                ], style={'margin':'0px'}),
            ]),
            html.Div([
                html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
                style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"left",'font-style':'italic','margin-top':'5px','width':'85%'}),
                html.P('|4',
                    style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"right",'font-style':'italic','margin-top':'5px','width':'10%','margin-top':'20px'}),
            ], style={'page-break-after': 'always','margin':'0px','display':'flex','justify-content':'space-between','width':'100%','margin-top':'5px'}),
            
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
                ], style={'display':'flex', 'justify-content':'space-between','width':'100%','height':'54px','color':'#0874bc'}),    
                html.Div([
                    html.Div([
                    html.Div([
                        html.Div([html.B('Короткоцепочечные ацилкарнитины',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'40px'}),
                        html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'black','text-align':'center'}),
                    ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Бутирилкарнитин (C4)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_10[1],ref_10[1])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_10[1]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_10[1],ref_10[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_10[1],ref_10[1])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_10[1],ref_10[1])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_10[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Изовалерилкарнитин (С5)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_10[2],ref_10[2])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_10[2]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_10[2],ref_10[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_10[2],ref_10[2])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_10[2],ref_10[2])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_10[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Тиглилкарнитин (C5-1)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_10[3],ref_10[3])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_10[3]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_10[3],ref_10[3])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_10[3],ref_10[3])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_10[3],ref_10[3])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_10[3]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Глутарилкарнитин (C5-DC)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_10[4],ref_10[4])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_10[4]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_10[4],ref_10[4])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_10[4],ref_10[4])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_10[4],ref_10[4])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_10[4]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Гидроксиизовалерилкарнитин (C5-OH)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_10[5],ref_10[5])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_10[5]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_10[5],ref_10[5])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_10[5],ref_10[5])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_10[5],ref_10[5])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_10[5]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    
                    html.Div([
                    html.Div([
                        html.Div([html.B('Среднецепочечные ацилкарнитины',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'40px'}),
                        html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'black','text-align':'center'}),
                    ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Гексаноилкарнитин (C6)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_11[0],ref_11[0])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_11[0]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_11[0],ref_11[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_11[0],ref_11[0])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_11[0],ref_11[0])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_11[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Адипоилкарнитин (C6-DC)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_11[1],ref_11[1])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_11[1]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_11[1],ref_11[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_11[1],ref_11[1])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_11[1],ref_11[1])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_11[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Октаноилкарнитин (C8)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_11[2],ref_11[2])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_11[2]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_11[2],ref_11[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_11[2],ref_11[2])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_11[2],ref_11[2])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_11[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Октеноилкарнитин (C8-1)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_11[3],ref_11[3])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_11[3]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_11[3],ref_11[3])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_11[3],ref_11[3])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_11[3],ref_11[3])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_11[3]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Деканоилкарнитин (C10)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_11[4],ref_11[4])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_11[4]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_11[4],ref_11[4])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_11[4],ref_11[4])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_11[4],ref_11[4])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_11[4]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Деценоилкарнитин (C10-1)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_11[5],ref_11[5])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_11[5]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_11[5],ref_11[5])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_11[5],ref_11[5])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_11[5],ref_11[5])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_11[5]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Декадиеноилкарнитин (C10-2)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_11[6],ref_11[6])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_11[6]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_11[6],ref_11[6])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_11[6],ref_11[6])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_11[6],ref_11[6])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_11[6]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Додеканоилкарнитин (C12)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_11[7],ref_11[7])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_11[7]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_11[7],ref_11[7])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_11[7],ref_11[7])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_11[7],ref_11[7])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_11[7]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Додеценоилкарнитин (C12-1)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_11[8],ref_11[8])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_11[8]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_11[8],ref_11[8])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_11[8],ref_11[8])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_11[8],ref_11[8])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_11[8]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    
                    html.Div([
                    html.Div([
                        html.Div([html.B('Длинноцепочечные ацилкарнитины',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'40px'}),
                        html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'black','text-align':'center'}),
                    ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Тетрадеканоилкарнитин (C14)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_12[0],ref_12[0])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_12[0]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_12[0],ref_12[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_12[0],ref_12[0])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_12[0],ref_12[0])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_12[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Тетрадеценоилкарнитин (С14-1)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_12[1],ref_12[1])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_12[1]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_12[1],ref_12[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_12[1],ref_12[1])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_12[1],ref_12[1])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_12[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Тетрадекадиеноилкарнитин (C14-2)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_12[2],ref_12[2])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_12[2]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_12[2],ref_12[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_12[2],ref_12[2])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_12[2],ref_12[2])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_12[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    
                    
                ], style={'margin':'0px'}),
            ]),
            html.Div([
                html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
                style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"left",'font-style':'italic','margin-top':'5px','width':'85%'}),
                html.P('|5',
                    style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"right",'font-style':'italic','margin-top':'5px','width':'10%','margin-top':'20px'}),
            ], style={'page-break-after': 'always','margin':'0px','display':'flex','justify-content':'space-between','width':'100%','margin-top':'0px'}),
            
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
                ], style={'display':'flex', 'justify-content':'space-between','width':'100%','height':'53px','color':'#0874bc'}),    
                
                html.Div([
                    html.Div([
                    html.Div([
                        html.Div([html.B('Длинноцепочечные ацилкарнитины',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'40px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'40px'}),
                        html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'black','text-align':'center'}),
                    ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Гидрокситетрадеканоилкарнитин (C14-OH)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_12[3],ref_12[3])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_12[3]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_12[3],ref_12[3])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_12[3],ref_12[3])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_12[3],ref_12[3])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_12[3]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Пальмитоилкарнитин (C16)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_12[4],ref_12[4])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_12[4]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_12[4],ref_12[4])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_12[4],ref_12[4])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_12[4],ref_12[4])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_12[4]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Гексадецениолкарнитин (C16-1)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_12[5],ref_12[5])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_12[5]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_12[5],ref_12[5])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_12[5],ref_12[5])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_12[5],ref_12[5])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_12[5]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Гидроксигексадецениолкарнитин (C16-1-OH)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_12[6],ref_12[6])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_12[6]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_12[6],ref_12[6])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_12[6],ref_12[6])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_12[6],ref_12[6])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_12[6]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px',}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Гидроксигексадеканоилкарнитин (C16-OH)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_12[7],ref_12[7])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_12[7]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_12[7],ref_12[7])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_12[7],ref_12[7])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_12[7],ref_12[7])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_12[7]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Стеароилкарнитин (С18)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_12[8],ref_12[8])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_12[8]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_12[8],ref_12[8])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_12[8],ref_12[8])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_12[8],ref_12[8])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_12[8]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Олеоилкарнитин (C18-1)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_12[9],ref_12[9])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_12[9]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_12[9],ref_12[9])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_12[9],ref_12[9])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_12[9],ref_12[9])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_12[9]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Гидроксиоктадеценоилкарнитин (C18-1-OH)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_12[10],ref_12[10])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_12[10]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_12[10],ref_12[10])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_12[10],ref_12[10])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_12[10],ref_12[10])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_12[10]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Линолеоилкарнитин (C18-2)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_12[11],ref_12[11])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_12[11]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_12[11],ref_12[11])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_12[11],ref_12[11])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_12[11],ref_12[11])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_12[11]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Гидроксиоктадеканоилкарнитин (C18-OH)',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_12[12],ref_12[12])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_12[12]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_12[12],ref_12[12])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_12[12],ref_12[12])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_12[12],ref_12[12])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_12[12]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    html.Div([
                        html.H3(children='5. Метаболический баланс', style={'textAlign':'center','margin':'0px','line-height':'normal','display':'inline-block','vertical-align':'center'}),]
                    , style={'width':'100%','background-color':'#0874bc', 'color':'white','font-family':'Calibri','margin':'0px','height':'35px','line-height':'35px','text-align':'center','margin-top':'5px'}),
                    html.Div([
                    html.Div([
                        html.Div([html.B('Витамины и нейромедиаторы',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'40px'}),
                        html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'black','text-align':'center'}),
                    ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Пантотеновая кислота',style={'height':'20px'}),html.P('Витамин B5',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_13[0],ref_13[0])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_13[0]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_13[0],ref_13[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_13[0],ref_13[0])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_13[0],ref_13[0])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_13[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Рибофлавин',style={'height':'20px'}),html.P('Витамин B2',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_13[1],ref_13[1])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_13[1]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_13[1],ref_13[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_13[1],ref_13[1])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_13[1],ref_13[1])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_13[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Мелатонин',style={'height':'20px'}),html.P('Регулирует циркадные ритмы',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_13[2],ref_13[2])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_13[2]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_13[2],ref_13[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_13[2],ref_13[2])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_13[2],ref_13[2])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_13[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                    
                    html.Div([
                    html.Div([
                        html.Div([html.B('Нуклеозиды',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'40px'}),
                        html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'black','text-align':'center'}),
                    ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Уридин',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_14[0],ref_14[0])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_14[0]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_14[0],ref_14[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_14[0],ref_14[0])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_14[0],ref_14[0])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_14[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Аденозин',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_14[1],ref_14[1])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_14[1]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_14[1],ref_14[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_14[1],ref_14[1])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_14[1],ref_14[1])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_14[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),
                                html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Цитидин',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_14[2],ref_14[2])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_14[2]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_14[2],ref_14[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_14[2],ref_14[2])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_14[2],ref_14[2])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_14[2]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px'}),

                    
                    html.Div([
                        html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
                        style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"left",'font-style':'italic','margin-top':'5px','width':'85%'}),
                        html.P('|6',
                            style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"right",'font-style':'italic','margin-top':'5px','width':'10%','margin-top':'20px'}),
                    ], style={'page-break-after': 'always','margin':'0px','display':'flex','justify-content':'space-between','width':'100%','margin-top':'5px'}),      
                ], style={'margin':'0px'}),
            ]),
            
                html.Div([
                    # Header section
                    html.Div([
                    html.Div([
                        html.Div([html.B('Аллергия и стресс',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Результат',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center'})],style={'width':'8%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'40px'}),
                        html.Div([html.Img(src=app.get_asset_url('procent_head.png'),style={'width':'100%','height':'15px','line-height':'normal','display':'inline-block','vertical-align':'center'}),],style={'width':'27%','height':'20px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'#0874bc','line-height':'40px'}),
                        html.Div([html.B('Референсные значения, мкмоль/л')],style={'width':'21%','height':'20px','margin':'0px','font-size':'14px','font-family':'Calibri','color':'black','text-align':'center'}),
                    ], style={'width':'100%','display':'flex', 'justify-content':'space-between','height':'40px',}), 
                    ], style={'margin':'0px','margin-left':'20px'}),
                    
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Кортизол',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_15[0],ref_15[0])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_15[0]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_15[0],ref_15[0])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_15[0],ref_15[0])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_15[0],ref_15[0])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_15[0]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.B('Гистамин',style={'height':'20px'}),html.P('',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_15[1],ref_15[1])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_15[1]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_15[1],ref_15[1])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_15[1],ref_15[1])}','line-height':'53px'}),
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
                                                'height': '12px',
                                                'width': '12px',
                                                'left': f'{calculate_pointer_position(value_15[1],ref_15[1])}%',
                                                'top': '8px',
                                                'transform': 'translateX(-50%)'
                                            })
                                ], style={'width': '27%', 'height': '53px', 'margin': '0px', 'font-size': '15px', 
                                        'font-family': 'Calibri', 'color': '#0874bc', 'align-content': 'center',
                                        'position': 'relative'}),
                                html.Div([html.P(f'{ref_15[1]}',style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','margin':'0'})],style={'width':'21%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','text-align':'center','line-height':'53px'}),
                            ], style={'width':'99.2%','display':'flex', 'justify-content':'space-between','height':'53px','margin-left':'5px'}),
                        ], style={'margin':'0px','margin-left':'20px'}),
                    ],style={'margin':'0px','background-color':'#FFFFFF'}),
                    # Spacer to push footer to bottom
                    html.Div(style={'flex-grow':'1'}),
                    html.Div([
                        html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
                        style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"left",'font-style':'italic','margin-top':'5px','width':'85%'}),
                        html.P('|7',
                            style={'color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"right",'font-style':'italic','margin-top':'5px','width':'10%','margin-top':'20px'}),
                    ], id = 'ending', style={'margin':'0px','display':'flex','justify-content':'space-between','width':'100%','bottom':'0px'}),  
                    
                ], style={
                    'min-height': '297mm',  # Leave space for footer
                    'display': 'flex',
                    'flex-direction': 'column',
                    'padding': '0px',
                }),
                
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