from dash import Dash, html
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
        df = pd.read_excel(file_path, header=None)
        data_start_row = 2
        metabolite_headers = df.iloc[0]
        measurement_types = df.iloc[1]
        metabolite_data = {}
        
        for col_idx in range(len(measurement_types)):
            if measurement_types[col_idx] == 'Final Conc.':
                metabolite_name = str(metabolite_headers[col_idx]).replace(' Results', '').strip()
                if pd.isna(metabolite_name):
                    continue
                
                conc_value = df.iloc[data_start_row, col_idx]
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
    
def parse_AC_metabolite_data(file_path):
    """
    Reads Excel file with two-row headers and extracts metabolite concentrations
    """
    try:
        # Read Excel file without headers initially to inspect structure
        df = pd.read_excel(file_path, header=None)
        
        # Find the row where data actually starts (after headers)
        data_start_row = 2  # Assuming data starts at row 3 (0-based index 2)
        
        # Extract headers - first row has metabolite names, second has measurement types
        metabolite_headers = df.iloc[0]  # First row - metabolite names
        measurement_types = df.iloc[1]   # Second row - 'Final Conc.', 'Area', etc.
        
        # Initialize dictionary to store results
        metabolite_data = {}
        
        # Iterate through columns to find 'Final Conc.' values
        for col_idx in range(len(measurement_types)):
            if measurement_types[col_idx] == 'Final Conc.':
                metabolite_name = metabolite_headers[col_idx]
                if pd.isna(metabolite_name):
                    continue
                
                # Clean metabolite name
                metabolite_name = str(metabolite_name).replace(' Results', '').strip()
                
                # Get concentration value from data row
                conc_value = df.iloc[data_start_row, col_idx]
                
                # Convert to float, handling different formats
                if isinstance(conc_value, str):
                    conc_value = float(conc_value.replace(',', '.'))
                elif pd.isna(conc_value):
                    conc_value = 0.0
                
                metabolite_data[metabolite_name] = conc_value
        
        return metabolite_data

    except Exception as e:
        print(f"Error processing file: {e}")
        return {}

def get_value_1(metabolite_data):
    """
    Processes the parsed metabolite data to extract specific values and rounds to 1 decimal place
    """
    ref_1 = ['35.8 - 76.9', '27.8 - 83.3', '63.6 - 160.2']
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
    ref_2 = ['92.6 - 310.0','133.0 - 317.1','225.6 - 627.1','1.25 - 104.5']
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
        tyrosin = round(float(metabolite_data.get('Tyrosin', 0) or metabolite_data.get('Tyrosine', 0)), 1)

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
    ref_3 = ['60 - 109','< 47.0','67.8 - 211.6','< 6.3','122 - 322','1.6 - 5.0','65 - 138','119 - 233','10 - 97','373 - 701','3.8 - 70.1','0.02 - 0.5']
    value_3 = []
    
    try:
        # Histidine
        histidine = round(float(metabolite_data.get('Histidine', 0)), 1)
        value_3.append(histidine)
        metilhistidine = round(float(metabolite_data.get('Methylhistidine', 0)), 1)
        value_3.append(metilhistidine)
        treonine = round(float(metabolite_data.get('Threonine', 0)), 1)
        value_3.append(treonine)
        carnosine = round(float(metabolite_data.get('Carnosine', 0)), 1)
        value_3.append(carnosine)
        glycine = round(float(metabolite_data.get('Glycine', 0)), 1)
        value_3.append(glycine)
        dymetilglycine = round(float(metabolite_data.get('DMG', 0)), 1)
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
    ref_4 = ['16 - 34','0.5 - 5.0','50 - 139','21 - 71','5.2 - 13.0','< 6.2','0.07 - 0.6']
    value_4 = []
    
    try:
        # metionine
        methionine = round(float(metabolite_data.get('Methionine', 0)), 1)
        value_4.append(methionine)
        Methionine_Sulfoxide = round(float(metabolite_data.get('Methionine-Sulfoxide', 0)), 1)
        value_4.append(Methionine_Sulfoxide)
        Taurine = round(float(metabolite_data.get('Taurine', 0)), 2)
        value_4.append(Taurine)
        Betaine = round(float(metabolite_data.get('Betaine', 0)), 2)
        value_4.append(Betaine)
        Choline = round(float(metabolite_data.get('Choline', 0)), 2)
        value_4.append(Choline)
        TMAO = round(float(metabolite_data.get('TMAO', 0)), 1)
        value_4.append(TMAO)
        indexChl_Bet= round(Choline / Betaine, 2)
        value_4.append(indexChl_Bet)
        return ref_4, value_4
        
    except Exception as e:
        print(f"Error in processing: {e}")
        # Return rounded default values
        return ref_4, [0.0, 0.0, 0.0]

def get_value_5(metabolite_data):
    """
    Processes the parsed metabolite data to extract specific values and rounds to 1 decimal place
    """
    ref_5 = ['40 - 91','< 4.4','< 0.11','0.0049 - 1.1158','0.04 - 0.30','0.0035 - 0.7642','0.002 - 0.037','0.0026 - 10.6']
    value_5 = []
    
    try:
        #Tryptophan
        tryptophan = round(float(metabolite_data.get('Tryptophan', 0)), 1)
        value_5.append(tryptophan)
        kynurenine = round(float(metabolite_data.get('Kynurenine', 0)), 1)
        value_5.append(kynurenine)
        indexKyn_Try = round(round(float(metabolite_data.get('Kynurenine', 0)), 3)/ round(float(metabolite_data.get('Tryptophan', 0)), 3), 3)
        value_5.append(indexKyn_Try)
        antranillic_acid = round(float(metabolite_data.get('Antranillic acid', 0)), 4)
        value_5.append(antranillic_acid)
        quinolinic_acid = round(float(metabolite_data.get('Quinolinic acid', 0)), 2)
        value_5.append(quinolinic_acid)
        Xanthurenic_acid = round(float(metabolite_data.get('Xanthurenic acid', 0)), 4)
        value_5.append(Xanthurenic_acid)
        Kynurenic_acid = round(float(metabolite_data.get('Kynurenic acid', 0)), 3)
        value_5.append(Kynurenic_acid)
        indexKyn_Qnl= round(Kynurenic_acid / quinolinic_acid, 4)
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
    ref_6 = ['0.18 - 1.18','0.04 - 0.30','0.01 - 19.1','0.0153 - 0.0207']
    value_6 = []
    
    try:
        # Serotonine
        serotonine = round(float(metabolite_data.get('Serotonin', 0)), 2)
        value_6.append(serotonine)
        hiaa = round(float(metabolite_data.get('HIAA', 0)), 2)
        value_6.append(hiaa)
        Quinolinic_acid = round(float(metabolite_data.get('Quinolinic acid', 0)), 2)
        indexQnl_hiaa = round(Quinolinic_acid / hiaa, 1)
        value_6.append(indexQnl_hiaa)
        hydroxy_tryptophan = round(float(metabolite_data.get('5-hydroxytryptophan', 0)), 4)
        value_6.append(hydroxy_tryptophan)
        return ref_6, value_6
        
    except Exception as e:
        print(f"Error in processing: {e}")
        
        return ref_6, [0.0, 0.0, 0.0]

def get_value_7(metabolite_data):
    """
    Processes the parsed metabolite data to extract specific values and rounds to 1 decimal place
    """
    ref_7 = ['0.3 - 23','0.08 - 5.0','0.01 - 0.20','0.5 - 12.0','< 0.4','< 0.003']
    value_7 = []
    
    try:
        # 3-indolacetic
        indole_acetic_acid = round(float(metabolite_data.get('Indole-3-acetic acid', 0)), 1)
        value_7.append(indole_acetic_acid)
        indole_lactic_acid = round(float(metabolite_data.get('Indole-3-lactic acid', 0)), 2)
        value_7.append(indole_lactic_acid)
        indole_carboxaldehyde = round(float(metabolite_data.get('Indole-3-carboxaldehyde', 0)), 2)
        value_7.append(indole_carboxaldehyde)
        indole_propionic_acid = round(float(metabolite_data.get('Indole-3-propionic acid', 0)), 1)
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
    ref_8 = ['104 - 383','4.7 - 35.2','0.23 - 0.50','0.20 - 0.67','1.0 - 6.0','32 - 120','16 - 51','38 - 130','29.5 - 84.5','5.4 - 21.5','0.18 - 2.2','0.25 - 3.16','0.06 - 0.7','13 - 57', '0.01 - 0.09']
    value_8 = []
    
    try:
        # Proline
        proline = round(float(metabolite_data.get('Proline', 0)), 1)
        value_8.append(proline)
        hydroxyproline = round(float(metabolite_data.get('Hydroxyproline', 0)), 1)
        value_8.append(hydroxyproline)
        adma = round(float(metabolite_data.get('ADMA', 0)), 2)
        value_8.append(adma)
        sdma = round(float(metabolite_data.get('TotalDMA (SDMA)', 0)), 2)
        value_8.append(sdma)
        homoarginine = round(float(metabolite_data.get('Homoarginine', 0)), 1)
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
        index_gabr = round(arginine / (Orintine + Citrulline), 1)
        value_8.append(index_gabr)
        index_AOR = round(arginine / Orintine, 1)
        value_8.append(index_AOR)
        index_asp_asn = round(asparagine / arginine, 1)
        value_8.append(index_asp_asn)
        creatine = round(float(metabolite_data.get('Creatinine', 0)), 1)
        value_8.append(creatine)
        nmma = round(float(metabolite_data.get('NMMA', 0)), 2)
        value_8.append(nmma)
        return ref_8, value_8
        
    except Exception as e:
        print(f"Error in processing: {e}")
        
        return ref_8, [0.0, 0.0, 0.0]

def get_value_9(metabolite_data, metabolite_ac_data):
    """
    Processes the parsed metabolite data to extract specific values and rounds to 1 decimal place
    """
    ref_9 = ['209 - 516','19 - 48','3.23 - 10.30']
    value_9 = []
    
    try:
        # Alanine
        alanine = round(float(metabolite_data.get('Alanine', 0)), 1)
        value_9.append(alanine)
        # c0
        c0 = round(float(metabolite_ac_data.get('C0', 0)), 2)
        value_9.append(c0)
        c2 = round(float(metabolite_ac_data.get('C2', 0)), 2)
        value_9.append(c2)
        return ref_9, value_9
        
    except Exception as e:
        print(f"Error in processing: {e}")
        
        return ref_9, [0.0, 0.0, 0.0]

def get_value_10(metabolite_ac_data):
    """
    Processes the parsed metabolite data to extract specific values and rounds to 1 decimal place
    """
    ref_10 = ['0.16 - 0.62','0.08 - 0.38','0.04 - 0.61','0.04 - 0.06','< 0.1','< 0.06']
    value_10 = []
    
    try:
        # c3
        c3 = round(float(metabolite_ac_data.get('C3', 0)), 2)
        value_10.append(c3)
        c4 = round(float(metabolite_ac_data.get('C4', 0)), 2)
        value_10.append(c4)
        c5 = round(float(metabolite_ac_data.get('C5', 0)), 2)
        value_10.append(c5)
        c5_1 = round(float(metabolite_ac_data.get('C5-1', 0)), 2)
        value_10.append(c5_1)
        c5_DC = round(float(metabolite_ac_data.get('C5-DC', 0)), 1)
        value_10.append(c5_DC)
        c5_OH = round(float(metabolite_ac_data.get('C5-OH', 0)), 2)
        value_10.append(c5_OH)
        return ref_10, value_10
        
    except Exception as e:
        print(f"Error in processing: {e}")
        
        return ref_10, [0.0, 0.0, 0.0]

def get_value_11(metabolite_ac_data):
    """
    Processes the parsed metabolite data to extract specific values and rounds to 1 decimal place
    """
    ref_11 = ['< 0.1','< 0.02','< 0.27','< 1.26','< 0.38','0.01 - 0.32','< 0.05','< 0.15','< 0.19']
    value_11 = []
    
    try:
        # c6
        c6 = round(float(metabolite_ac_data.get('C6', 0)), 2)
        value_11.append(c6)
        c6_DC = round(float(metabolite_ac_data.get('C6-DC', 0)), 3)
        value_11.append(c6_DC)
        c8 = round(float(metabolite_ac_data.get('C8', 0)), 3)
        value_11.append(c8)
        c8_1 = round(float(metabolite_ac_data.get('C8-1', 0)), 3)
        value_11.append(c8_1)
        c10 = round(float(metabolite_ac_data.get('C10', 0)), 3)
        value_11.append(c10)
        c10_1 = round(float(metabolite_ac_data.get('C10-1', 0)), 3)
        value_11.append(c10_1)
        c10_2 = round(float(metabolite_ac_data.get('C10-2', 0)), 3)
        value_11.append(c10_2)
        c12 = round(float(metabolite_ac_data.get('C12', 0)), 3)
        value_11.append(c12)
        c12_1 = round(float(metabolite_ac_data.get('C12-1', 0)), 3)
        value_11.append(c12_1)
        return ref_11, value_11
        
    except Exception as e:
        print(f"Error in processing: {e}")
        
        return ref_11, [0.0, 0.0, 0.0] 

def get_value_12(metabolite_ac_data):
    """
    Processes the parsed metabolite data to extract specific values and rounds to 1 decimal place
    """
    ref_12 = ['0.01 - 0.22','0.04 - 0.41','< 0.16','0.01 - 0.29','< 0.09','< 0.1','< 0.1','< 0.02','0.03 - 0.13','0.07 - 0.51','< 0.32','0.02 - 0.26','0.3 - 2.3']
    value_12 = []
    
    try:
        # c14
        c14 = round(float(metabolite_ac_data.get('C14', 0)), 3)
        value_12.append(c14)
        c14_1 = round(float(metabolite_ac_data.get('C14-1', 0)), 3)
        value_12.append(c14_1)
        c14_2 = round(float(metabolite_ac_data.get('C14-2', 0)), 3)
        value_12.append(c14_2)
        c14_OH = round(float(metabolite_ac_data.get('C14-OH', 0)), 3)
        value_12.append(c14_OH)
        c16 = round(float(metabolite_ac_data.get('C16', 0)), 3)
        value_12.append(c16)
        c16_1 = round(float(metabolite_ac_data.get('C16-1', 0)), 3)
        value_12.append(c16_1)
        C16_1_OH = round(float(metabolite_ac_data.get('C16-1-OH', 0)), 3)
        value_12.append(C16_1_OH)
        c16_OH = round(float(metabolite_ac_data.get('C16-OH', 0)), 3)
        value_12.append(c16_OH)
        c18 = round(float(metabolite_ac_data.get('C18', 0)), 3)
        value_12.append(c18)
        c18_1 = round(float(metabolite_ac_data.get('C18-1', 0)), 3)
        value_12.append(c18_1)
        c18_1_OH = round(float(metabolite_ac_data.get('C18-1-OH', 0)), 3)
        value_12.append(c18_1_OH)
        c18_2 = round(float(metabolite_ac_data.get('C18-2', 0)), 3)
        value_12.append(c18_2)
        c18_OH = round(float(metabolite_ac_data.get('C18-OH', 0)), 3)
        value_12.append(c18_OH)
        return ref_12, value_12
        
    except Exception as e:
        print(f"Error in processing: {e}")
        
        return ref_12, [0.0, 0.0, 0.0]
    

def get_value_13(metabolite_data):
    """
    Processes the parsed metabolite data to extract specific values and rounds to 1 decimal place
    """
    ref_13 = ['0.30 - 1.80','6.2 - 39.0','0.0002 - 0.0204']
    value_13 = []
    
    try:
        # Pantotenic acid
        pantotenic_acid = round(float(metabolite_data.get('Pantothenic', 0)), 2)
        value_13.append(pantotenic_acid)
        riboflavin = round(float(metabolite_data.get('Riboflavin', 0)), 1)
        value_13.append(riboflavin)
        melatonine = round(float(metabolite_data.get('Melatonin', 0)), 4)
        value_13.append(melatonine)
        return ref_13, value_13
        
    except Exception as e:
        print(f"Error in processing: {e}")
        
        return ref_13, [0.0, 0.0, 0.0]

def get_value_14(metabolite_data):
    """
    Processes the parsed metabolite data to extract specific values and rounds to 1 decimal place
    """
    ref_14 = ['0.23 - 2.58','0.1 - 0.3', '0.06 - 0.44']
    value_14 = []
    
    try:
        # Uridine
        uridine = round(float(metabolite_data.get('Uridine', 0)), 2)
        value_14.append(uridine)
        adenosine = round(float(metabolite_data.get('Adenosin', 0)), 1)
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
    ref_15 = ['0.1 - 0.5','< 0.1329']
    value_15 = []
    
    try:
        # Cortisol
        cortisol = round(float(metabolite_data.get('Cortisol', 0)), 2)
        value_15.append(cortisol)
        # Histamine
        histamine = round(float(metabolite_data.get('Histamine', 0)), 4)
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
    if n < 30:
        return '#50c150'
    elif n < 60:
        return '#9fd047'
    elif n < 80:
        return '#feb61d'
    else:
        return '#de6d54'
    
def get_text_from_procent(n):
    if n < 30:
        return 'Замедленный'
    elif n < 60:
        return 'Нормальный'
    elif n < 80:
        return 'Умеренно ускоренный'
    else:
        return 'Сильно ускоренный'
    
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
            return 0
        elif value > ref_max:
            return 100
        else:
            position = ((value - ref_min) / (ref_max - ref_min)) * 100
            return max(0, min(100, round(position, 2)))  # Clamp and round to 2 decimals
    
    except (ValueError, AttributeError, TypeError):
        # Return middle position if there's any error
        return 50

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
    parser.add_argument('--file1', required=True)
    parser.add_argument('--file2', required=True)
    args = parser.parse_args()
    # Register shutdown handler
    signal.signal(signal.SIGTERM, shutdown_handler)
    
    try:
        # Update global variables from command line args
        name = args.name
        age = args.age
        gender = args.gender
        date = args.date
        
        # Process files with safety checks
        metabolite_data = safe_parse_metabolite_data(args.file1)
        metabolite_ac_data = safe_parse_metabolite_data(args.file2)
        
        # Calculate all values using safe functions
        ref_1, value_1 = get_value_1(metabolite_data)
        ref_2, value_2 = get_value_2(metabolite_data)
        ref_3, value_3 = get_value_3(metabolite_data)
        ref_4, value_4 = get_value_4(metabolite_data)
        ref_5, value_5 = get_value_5(metabolite_data)
        ref_6, value_6 = get_value_6(metabolite_data)
        ref_7, value_7 = get_value_7(metabolite_data)
        ref_8, value_8 = get_value_8(metabolite_data)
        ref_9, value_9 = get_value_9(metabolite_data, metabolite_ac_data)
        ref_10, value_10 = get_value_10(metabolite_ac_data)
        ref_11, value_11 = get_value_11(metabolite_ac_data)
        ref_12, value_12 = get_value_12(metabolite_ac_data)
        ref_13, value_13 = get_value_13(metabolite_data)
        ref_14, value_14 = get_value_14(metabolite_data)
        ref_15, value_15 = get_value_15(metabolite_data)
        def create_layout():
            """Your complete existing layout using all the variables"""
            return html.Div([
            # # 1 страница
            # html.Div([
            #     html.Div([
            #         html.Img(src=app.get_asset_url('logo-sechenov.png'), style={'width':'100%','height':'100%','margin':'0px'})
            #     ],style={'width':'20%','height':'100px', 'margin':'0px'}),
            #     html.Div([
            #         html.Div([
            #             html.Div([
            #                 html.P('ФИО:',style={'margin':'0px'}), html.B(f'{name}',style={'margin':'0px','margin-left':'5px'})
            #             ],style={'margin':'0px','display':'flex', 'justify-content':'left', 'width':'40%'}),
            #             html.Div([
            #                 html.P('Дата:',style={'margin':'0px'}), html.B(f'{date}',style={'margin':'0px','margin-left':'5px'})
            #             ],style={'margin':'0px','display':'flex', 'justify-content':'left', 'width':'40%'}),
            #             html.Div([
            #                 html.P('Возраст:',style={'margin':'0px'}), html.B(f'{age}',style={'margin':'0px','margin-left':'5px'})
            #             ],style={'margin':'0px','display':'flex', 'justify-content':'left', 'width':'40%'}),
            #             html.Div([
            #                 html.P('Пол:',style={'margin':'0px'}), html.B(f'{gender}',style={'margin':'0px','margin-left':'5px'})
            #             ],style={'margin':'0px','display':'flex', 'justify-content':'left', 'width':'40%',}), 
            #         ],style={'margin-top':'10px','margin-left':'25px','color':'black','font-family':'Calibri','font-size':'15px'}),
                    
            #     ],style={'width':'80%','height':'100px', 'color':'white','margin':'0px','background-image':'url("/assets/rHeader.png")','background-repeat':'no-repeat','background-size':'100%','background-position':'center'}),
            # ], style={'display':'flex', 'justify-content':'space-between','width':'100%','height':'100px','margin-bottom':'10px'}),
            # html.Div([
            #     html.H1(children='Панорамный метаболомный обзор', style={'textAlign':'center','margin':'0px'}),]
            #          , style={'width':'100%','background-color':'#0874bc', 'color':'white','font-family':'Calibri','margin':'0px'}),
            # html.P('На графике представлены функциональные группы метаболитов, которые были оценены по уровню риска на основе Ваших результатов метаболомного профилирования',
            #                 style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px'}),
            # html.Div([
            #     html.Div([
            #         html.Div([
            #             html.H3(children='Уровень риска', style={'textAlign':'left', 'color':'#0874bc','font-family':'Calibri','margin':'0px','margin-top':'5px',}),
            #         ],style={'display':'flex', 'width':'100%','height':'30px'}),
            #         html.Div([
            #             html.Img(src=app.get_asset_url('risk_bar.png'), style={'width':'100%','pointer-events':'none', 'margin-left':'3px'}),
            #         ], style={'margin':'0px','height':'50px','margin-right':'10px'}),
            #         html.Div([
            #             html.Img(src=app.get_asset_url(f'{main_plot(part=part)}'), style={'width':'100%','margin-top':'10px'}),
            #         ], style={'display':'flex', 'justify-content':'space-between', 'width':'100%','height':'330px'}),
            #     ], style={ 'width':'65%',}),
            #     html.Div([
            #         html.P('На основании панорамного метаболомного профиля был оценен темп старения организма',style={'color':'black','height':'60px','font-family':'Calibri','font-size':'16px','margin':'0px','margin-left':'10px','text-align':"left ",'margin-top':'100px'}),
            #         html.Div([html.Img(src=app.get_asset_url(f'{normal_dist(N,a,procent_speed)}'), style={'width':'100%','margin-top':'10px'})], style={'height':'150px'}),
            #         html.Div([
            #             html.P("медленно",style={'margin':'0px','margin-left':'10px'}),
            #             html.P("нормально",style={'margin':'0px'}),
            #             html.P("быстро",style={'margin':'0px','margin-right':'10px'}),
            #         ],style={'height':'20px','display':'flex', 'justify-content':'space-between', 'width':'100%','font-family':'Calibri','font-size':'16px','margin':'0px'}),
            #         html.Div([
            #             html.P(f'{get_text_from_procent(procent_speed)}',style={'margin':'0','font-size':'18px','color':'white','font-family':'Calibri','font-weight':'bold','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #         ], style={'height':'47px','background-color':f'{get_color_under_normal_dist(procent_speed)}','line-height':'47px','text-align':'center','margin-left':'40px','margin-right':'40px'}),    
            #     ], style={'width':'35%',}),
            # ], style={'display':'flex', 'justify-content':'space-between', 'width':'100%'}),
            # html.Div([
            #     html.P('Ниже показано, какие классы метаболитов составляют функциональные группы, и как изменение в классе метаболитов повлияло на результат Панорамного метаболомного обзора.',
            #             style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px','text-align':"left"}),
            #     ], style={'width':'100%'}),
            # html.Div([
            #     html.Div([
            #         html.Div([
            #             html.P('1. Обмен веществ – (',style={'margin':'0px','margin-bottom':'1px'}),html.B(f'{obmen_veshestv}%',style={'margin':'0px'}),html.P(')',style={'margin':'0px'}),
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(obmen_veshestv)}','background-color':f'{get_color_under_normal_dist(obmen_veshestv)}','border-radius':'2px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center','margin-left':'5px','margin-top':'6px'}),
            #             ],style={'width':'50px','height':'18px','line-height':'18px'}),
            #         ], style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-bottom':'1px'}),
                    
            #         html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(obmen_veshestv_list[0])}','background-color':f'{get_color(obmen_veshestv_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'23%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Карнитин',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'75%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            #         html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(obmen_veshestv_list[1])}','background-color':f'{get_color(obmen_veshestv_list[1])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'23%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Короткоцепочечные ацилкарнитины',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'77%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            #         html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(obmen_veshestv_list[2])}','background-color':f'{get_color(obmen_veshestv_list[2])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'23%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Среднецепочечные ацилкарнитины',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'77%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            #         html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(obmen_veshestv_list[3])}','background-color':f'{get_color(obmen_veshestv_list[3])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'23%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Длинноцепочечные ацилкарнитины',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'77%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            #         html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(obmen_veshestv_list[4])}','background-color':f'{get_color(obmen_veshestv_list[4])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'23%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Функция эндотелия сосудов',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'77%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),



            #         html.Div([
            #             html.P('3. Нутриентный статус – (',style={'margin':'0px','margin-bottom':'1px'}),html.B(f'{nutrieviy_status}%',style={'margin':'0px'}),html.P(')',style={'margin':'0px'}),
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(nutrieviy_status)}','background-color':f'{get_color_under_normal_dist(nutrieviy_status)}','border-radius':'2px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center','margin-left':'5px','margin-top':'6px'}),
            #             ],style={'width':'50px','height':'18px','line-height':'18px'}),  
            #         ], style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-top':'24px','margin-bottom':'1px'}),
                    
            #         html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(nutrieviy_status_list[0])}','background-color':f'{get_color(nutrieviy_status_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'23%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Витамины',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'77%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            #         html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(nutrieviy_status_list[1])}','background-color':f'{get_color(nutrieviy_status_list[1])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'23%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Метаболизм холина',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'77%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            #         html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(nutrieviy_status_list[2])}','background-color':f'{get_color(nutrieviy_status_list[2])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'23%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Потребление рыбы',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'77%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            #         html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(nutrieviy_status_list[3])}','background-color':f'{get_color(nutrieviy_status_list[3])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'23%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Потребление растительной пищи',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'77%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            #         html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(nutrieviy_status_list[4])}','background-color':f'{get_color(nutrieviy_status_list[4])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'23%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Потребление мяса',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'77%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),



            #         html.Div([
            #             html.P('5. Токсическое воздействие – (',style={'margin':'0px','margin-bottom':'1px'}),html.B(f'{toxicheskie_vosdeystvia}%',style={'margin':'0px'}),html.P(')',style={'margin':'0px'}),
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(toxicheskie_vosdeystvia)}','background-color':f'{get_color_under_normal_dist(toxicheskie_vosdeystvia)}','border-radius':'2px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center','margin-left':'5px','margin-top':'6px'}),
            #             ],style={'width':'50px','height':'18px','line-height':'18px'}),
            #         ], style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-top':'6px','margin-bottom':'1px'}),
                    
            #         html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(toxicheskie_vosdeystvia_list[0])}','background-color':f'{get_color(toxicheskie_vosdeystvia_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'23%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Аллергия',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'77%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            #         html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(toxicheskie_vosdeystvia_list[1])}','background-color':f'{get_color(toxicheskie_vosdeystvia_list[1])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'23%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Окислительный стресс',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'77%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            #         html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(toxicheskie_vosdeystvia_list[2])}','background-color':f'{get_color(toxicheskie_vosdeystvia_list[2])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'23%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Цикл мочевины',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'77%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),



            #         html.Div([
            #             html.P('7. Воспаление – (',style={'margin':'0px','margin-bottom':'1px'}),html.B(f'{vospalenie}%',style={'margin':'0px'}),html.P(')',style={'margin':'0px'}),
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(vospalenie)}','background-color':f'{get_color_under_normal_dist(vospalenie)}','border-radius':'2px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center','margin-left':'5px','margin-top':'5px'}),
            #             ],style={'width':'50px','height':'18px','line-height':'18px'}),
            #         ], style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-top':'6px','margin-bottom':'1px'}),
                    
            #         html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(vospalenie_list[0])}','background-color':f'{get_color(vospalenie_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'23%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Маркеры воспаления',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'77%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),


            #         html.Div([
            #             html.P('9. Функция печени – (',style={'margin':'0px','margin-bottom':'1px'}),html.B(f'{functii_pecheni}%',style={'margin':'0px'}),html.P(')',style={'margin':'0px'}),
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(functii_pecheni)}','background-color':f'{get_color_under_normal_dist(functii_pecheni)}','border-radius':'2px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center','margin-left':'5px','margin-top':'6px'}),
            #             ],style={'width':'50px','height':'18px','line-height':'18px'}),  
            #         ], style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-top':'6px','margin-bottom':'1px'}),
                    
            #         html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(functii_pecheni_list[0])}','background-color':f'{get_color(functii_pecheni_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'23%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Индекс Фишера',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'77%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            #         html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(functii_pecheni_list[1])}','background-color':f'{get_color(functii_pecheni_list[1])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'23%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Индекс Aor',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'77%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            #         html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(functii_pecheni_list[2])}','background-color':f'{get_color(functii_pecheni_list[2])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'23%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Индекс GABR',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'77%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            #         html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(functii_pecheni_list[3])}','background-color':f'{get_color(functii_pecheni_list[3])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'23%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Индекс GSG',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'77%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
                    

            #     ], style={'width':'38%','height':'480px'}),
            #     html.Div([
            #         html.Div([
            #             html.P('2. Обмен аминокислот – (',style={'margin':'0px'}),html.B(f'{obmen_aminokislot}%',style={'margin':'0px'}),html.P(')',style={'margin':'0px'}),
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(obmen_aminokislot)}','background-color':f'{get_color_under_normal_dist(obmen_aminokislot)}','border-radius':'2px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center','margin-left':'5px','margin-top':'6px'}),
            #             ],style={'width':'50px','height':'18px','line-height':'18px'}),  
            #         ], style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-top':'2px'}),
            #         html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(obmen_aminokislot_list[0])}','background-color':f'{get_color(obmen_aminokislot_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'15%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Метаболизм фенилаланина',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'79%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            #         html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(obmen_aminokislot_list[1])}','background-color':f'{get_color(obmen_aminokislot_list[1])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'15%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Метаболизм аминокислот с разветвленной боковой цепью',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'79%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            #         html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(obmen_aminokislot_list[2])}','background-color':f'{get_color(obmen_aminokislot_list[2])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'15%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Метаболизм триптофана',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'79%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            #         html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(obmen_aminokislot_list[3])}','background-color':f'{get_color(obmen_aminokislot_list[3])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'15%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Метионин',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'79%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            #         html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(obmen_aminokislot_list[4])}','background-color':f'{get_color(obmen_aminokislot_list[4])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'15%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Гистидин',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'79%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            #         html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(obmen_aminokislot_list[5])}','background-color':f'{get_color(obmen_aminokislot_list[5])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'15%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Глутаминовая кислота и аспарагиновая кислота',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'79%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),



            #         html.Div([
            #             html.P('4. Стресс и нейромедиаторы – (',style={'margin':'0px'}),html.B(f'{stress_i_neyromoderatory}%',style={'margin':'0px'}),html.P(')',style={'margin':'0px'}),
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(stress_i_neyromoderatory)}','background-color':f'{get_color_under_normal_dist(stress_i_neyromoderatory)}','border-radius':'2px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center','margin-left':'5px','margin-top':'6px'}),
            #             ],style={'width':'50px','height':'18px','line-height':'18px'}),   
            #         ], style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-top':'8px'}),
            #         html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(stress_i_neyromoderatory_list[0])}','background-color':f'{get_color(stress_i_neyromoderatory_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'15%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Стероидные гормоны',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'79%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            #         html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(stress_i_neyromoderatory_list[1])}','background-color':f'{get_color(stress_i_neyromoderatory_list[1])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'15%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Нейромедиаторы',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'79%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            #         html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(stress_i_neyromoderatory_list[2])}','background-color':f'{get_color(stress_i_neyromoderatory_list[2])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'15%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Метаболизм фенилаланина',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'79%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            #         html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(stress_i_neyromoderatory_list[3])}','background-color':f'{get_color(stress_i_neyromoderatory_list[3])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'15%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Синтез серотонина и мелатонина',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'79%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),



            #         html.Div([
            #             html.P('6. Маркеры микробиоты – (',style={'margin':'0px'}),html.B(f'{markery_mikrobioty}%',style={'margin':'0px'}),html.P(')',style={'margin':'0px'}),
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(markery_mikrobioty)}','background-color':f'{get_color_under_normal_dist(markery_mikrobioty)}','border-radius':'2px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center','margin-left':'5px','margin-top':'6px'}),
            #             ],style={'width':'50px','height':'18px','line-height':'18px'}),    
            #         ], style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-top':'26px'}),
                    
            #         html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(markery_mikrobioty_list[0])}','background-color':f'{get_color(markery_mikrobioty_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'15%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('ТМАО (триметиламин-N-оксид)',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'79%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            #         html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(markery_mikrobioty_list[1])}','background-color':f'{get_color(markery_mikrobioty_list[1])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'15%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Индольный путь метаболизма триптофана',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'79%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            #         html.Div([
            #             html.P('8. Функция сердца – (',style={'margin':'0px'}),html.B(f'{funcii_serdca}%',style={'margin':'0px'}),html.P(')',style={'margin':'0px'}),
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(funcii_serdca)}','background-color':f'{get_color_under_normal_dist(funcii_serdca)}','border-radius':'2px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center','margin-left':'5px','margin-top':'6px'}),
            #             ],style={'width':'50px','height':'18px','line-height':'18px'}),    
            #         ], style={'color':'black','font-family':'Calibri','font-size':'16px','margin':'0px','display':'flex', 'justify-content':'left','margin-top':'26px'}),
            #         html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(funcii_serdca_list[0])}','background-color':f'{get_color(funcii_serdca_list[0])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'15%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Метаболизм аминокислот с разветвленной боковой цепью',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'79%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            #                     html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(funcii_serdca_list[1])}','background-color':f'{get_color(funcii_serdca_list[1])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'15%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Окислительный стресс',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'79%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            #                     html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(funcii_serdca_list[2])}','background-color':f'{get_color(funcii_serdca_list[2])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'15%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Функция эндотелия сосудов',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'79%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            #                     html.Div([
            #             html.Div([
            #                 html.Div([],style={'width':f'{procent_validator(funcii_serdca_list[3])}','background-color':f'{get_color(funcii_serdca_list[3])}','border-radius':'5px','height':'10px','line-height':'normal','display':'inline-block','vertical-align':'center'}),
            #             ],style={'width':'15%','height':'18px','line-height':'18px'}),
            #             html.Div([
            #                 html.P('Системные маркеры',style={'margin':'0px','font-size':'14px','font-family':'Calibri','height':'18px','margin-left':'3px'})
            #             ],style={'width':'79%'}),
            #         ],style={'display':'flex', 'justify-content':'left', 'width':'100%','height':'18px'}),
            #     ], style={'width':'57%','height':'480px',})
            # ], style={'display':'flex', 'justify-content':'space-between','height':'480px','margin-top':'5px'}),
            # html.P('Результаты данного отчета не являются диагнозом и должны быть интерпретированы лечащим врачом на основании клинико-лабораторных данных и других диагностических исследований.',
            #        style={'page-break-after': 'always','color':'black','font-family':'Calibri','font-size':'14px','margin':'0px','text-align':"left",'font-style':'italic','margin-top':'5px'}),

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
                                    html.Img(src=app.get_asset_url('progress_left.png'), 
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
                                html.Div([html.B('Индекс Chl / Bet',style={'height':'20px'}),html.P('Соотношение холина к бетаину',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
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
                                    html.Img(src=app.get_asset_url('progress_left.png'), 
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
                                    html.Img(src=app.get_asset_url('progress_left.png'), 
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
                                    html.Img(src=app.get_asset_url('progress.png'), 
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
                                html.Div([html.B('Индекс Kyn / Qnl',style={'height':'20px'}),html.P('Соотношение кинуренина к хинолиновой кислоте',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
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
                                    html.Img(src=app.get_asset_url('progress.png'), 
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
                                html.Div([html.B('Индекс Qnl / 5-HIAA',style={'height':'20px'}),html.P('Соотношение 5-гидроксииндолуксусной кислоты к хинолиновой кислота',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
                                html.Div([html.Div([html.Div([html.B(f'{need_of_plus_minus(value_6[2],ref_6[2])}',style={'width':'30%','text-align':'left'}),html.B(f'{value_6[2]}',style={'text-align':'right','width':'50%'})],style={'width':'100%','display':'flex','justify-content':'space-between','margin-top':f'{need_of_margin(value_6[2],ref_6[2])}'})],style={'height':'20px','line-height':'normal','display':'inline-block','vertical-align':'center','width':'100%'})],style={'width':'8%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':f'{color_text_ref(value_6[2],ref_6[2])}','line-height':'53px'}),
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
                                    html.Img(src=app.get_asset_url('progress.png'), 
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
                                html.Div([html.B('Индекс Asp / Asn',style={'height':'20px'}),html.P('Показывает активность аспарагинсинтетазы',style={'height':'20px','font-size':'12px','font-family':'Calibri','color':'#39507c','margin':'0px','margin-left':'5px','line-height':'0.9em'})],style={'width':'39%','height':'53px','margin':'0px','font-size':'15px','font-family':'Calibri','color':'black','margin-top':'5px'}),
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
                                    html.Img(src=app.get_asset_url('progress.png'), 
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
                                    html.Img(src=app.get_asset_url('progress_left.png'), 
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
                                    html.Img(src=app.get_asset_url('progress_left.png'), 
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
                                    html.Img(src=app.get_asset_url('progress_left.png'), 
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
                                    html.Img(src=app.get_asset_url('progress_left.png'), 
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
                                    html.Img(src=app.get_asset_url('progress_left.png'), 
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
                                    html.Img(src=app.get_asset_url('progress.png'), 
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
                                    html.Img(src=app.get_asset_url('progress.png'), 
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
                        html.H3(children='4. Метаболизм жирных кислот', style={'textAlign':'center','margin':'0px','line-height':'normal','display':'inline-block','vertical-align':'center'}),]
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