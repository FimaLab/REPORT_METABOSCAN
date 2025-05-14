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
    driver.set_page_load_timeout(45)
    driver.set_script_timeout(30)
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
                time.sleep(1)
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
def calculate_metabolite_ratios(metabolomic_data):
    """Calculate all metabolite ratios from raw metabolomic data"""
    data = pd.read_excel(metabolomic_data)
    
    # Arginine metabolism
    data['Arg/Orn+Cit'] = data['Arginine'] / (data['Ornitine'] + data['Citrulline'])
    data['Arg/Orn'] = data['Arginine'] / data['Ornitine']
    data["Arg/ADMA"] = data['Arginine'] / data['ADMA']
    data['(Arg+HomoArg)/ADMA'] = (data['Arginine'] + data['Homoarginine']) / data['ADMA']
    
    # Acylcarnitines
    data['C0/(C16+C18)'] = data['C0'] / (data['C16'] + data['C18'])
    data['(C16+C18)/C2'] = (data['C16'] + data['C18']) / data['C2']
    data['(C6+C8+C10)/C2'] = (data['C6'] + data['C8'] + data['C10']) / data['C2']
    data['C3/C2'] = data['C3'] / data['C2']
    
    # Tryptophan metabolism
    data['Trp/Kyn'] = data['Tryptophan'] / data['Kynurenine']
    data['Trp/(Kyn+QA)'] = data['Tryptophan'] / (data['Kynurenine'] + data['Quinolinic acid'])
    data['Kyn/Quin'] = data['Kynurenine'] / data['Quinolinic acid']
    data['Quin/HIAA'] = data['Quinolinic acid'] / data['HIAA']
    
    # Amino acids
    data['Aspartate/Asparagine'] = data['Aspartic acid'] / data['Asparagine']
    data['Glutamine/Glutamate'] = data['Glutamine'] / data['Glutamic acid']
    data['Glycine/Serine'] = data['Glycine'] / data['Serine']
    data['GSG_index'] = data['Glutamic acid'] / (data['Serine'] + data['Glycine'])
    data['Phe/Tyr'] = data['Phenylalanine'] / data['Tyrosin']
    data['Phe+Tyr'] = data['Phenylalanine'] + data['Tyrosin']
    data['BCAA'] = data['Summ Leu-Ile'] + data['Valine']
    data['BCAA/AAA'] = (data['Valine'] + data['Summ Leu-Ile']) / (data['Phenylalanine'] + data['Tyrosin'])
    
    # Other ratios
    data['Betaine/choline'] = data['Betaine'] / data['Choline']
    data['Kyn/Trp'] = data['Kynurenine'] / data['Tryptophan']
    data['СДК'] = data['C14'] + data['C14-1'] + data['C14-2'] + data['C14-OH'] + data['C16'] + data['C16-1'] + data['C16-1-OH'] + data['C16-OH'] + data['C18'] + data['C18-1'] + data['C18-1-OH'] + data['C18-2'] + data['C18-OH']
    data['Alanine / Valine'] = data['Alanine'] / data['Valine']
    data['Tryptamine / IAA'] = data['Tryptamine'] / data['Indole-3-acetic acid']
    data['С2/С0'] = data['C2'] / data['C0']
    data['(C2+C3)/C0'] = (data['C2'] + data['C3']) / data['C0']
    data['Kynurenic acid / Kynurenine'] = data['Kynurenic acid'] / data['Kynurenine']
    data['Methionine + Taurine'] = data['Methionine'] + data['Taurine']
    data['Valine / Alanine'] = data['Valine'] / data['Alanine']
    data['Riboflavin / Pantothenic'] = data['Riboflavin'] / data['Pantothenic']
    data['ADMA / NMMA'] = data['ADMA'] / data['NMMA']
    data['DMG / Choline'] = data['DMG'] / data['Choline']
    
    # drop Group column
    data = data.drop('Group', axis=1)

    return data

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
    
    # Initialize Score_Clear with 0 (normal range)
    risk_params['Score_Clear'] = 0
    
    # Convert string representations of infinity to numeric
    risk_params['norm_1'] = risk_params['norm_1'].replace('-inf', -np.inf)
    risk_params['norm_2'] = risk_params['norm_2'].replace('+inf', np.inf)
    
    # Create masks for special cases
    norm1_is_inf = risk_params['norm_1'] == -np.inf
    norm2_is_inf = risk_params['norm_2'] == np.inf
    
    # Case 1: Only norm_2 is valid (norm_1 is -inf)
    mask_case1 = norm1_is_inf & ~norm2_is_inf
    risk_params.loc[mask_case1 & (risk_params['Patient'] >= risk_params['norm_2']) & 
                  (risk_params['Patient'] < risk_params['High_risk_2']), 'Score_Clear'] = 1
    risk_params.loc[mask_case1 & (risk_params['Patient'] >= risk_params['High_risk_2']), 'Score_Clear'] = 2
    
    # Case 2: Only norm_1 is valid (norm_2 is +inf)
    mask_case2 = ~norm1_is_inf & norm2_is_inf
    risk_params.loc[mask_case2 & (risk_params['Patient'] > risk_params['High_risk_1']) & 
                  (risk_params['Patient'] <= risk_params['norm_1']), 'Score_Clear'] = 1
    risk_params.loc[mask_case2 & (risk_params['Patient'] <= risk_params['High_risk_1']), 'Score_Clear'] = 2
    
    # Case 3: Both norms are valid (finite)
    mask_case3 = ~norm1_is_inf & ~norm2_is_inf
    risk_params.loc[mask_case3 & (
        ((risk_params['Patient'] > risk_params['High_risk_1']) & (risk_params['Patient'] <= risk_params['norm_1'])) |
        ((risk_params['Patient'] >= risk_params['norm_2']) & (risk_params['Patient'] < risk_params['High_risk_2']))
    ), 'Score_Clear'] = 1
    risk_params.loc[mask_case3 & (
        (risk_params['Patient'] <= risk_params['High_risk_1']) |
        (risk_params['Patient'] >= risk_params['High_risk_2'])
    ), 'Score_Clear'] = 2
    
    # Calculate weighted scores
    risk_params['Score_Weighted'] = risk_params['Score_Clear'] * risk_params['веса']
    risk_params['Max_score_weighted'] = risk_params['веса'] * 2
    
    return risk_params

def calculate_risks(risk_params_data, metabolomic_data_with_ratios):
    """Calculate risks based on risk parameters and metabolomic data with ratios"""
    risk_params = pd.read_excel(risk_params_data)
    
    # Get values for each marker from metabolomic data
    values_conc = []
    for metabolite in risk_params['Маркер / Соотношение']:
        values_conc.append(float(metabolomic_data_with_ratios.loc[0, metabolite]))
    
    risk_params['Sample'] = values_conc
    risks = []
    
    # Calculate risk levels
    for index, row in risk_params.iterrows():
        if row['norm_1'] <= row['Sample'] <= row['norm_2']:
            risks.append(0)
        elif row['High_risk_1'] <= row['Sample'] < row['norm_1'] or row['norm_2'] < row['Sample'] <= row['High_risk_2']:
            risks.append(1)
        else:
            risks.append(2)
    
    # Apply weights
    risk_params['Risks'] = risks
    risk_params['Corrected_risks'] = risk_params['Risks'] * risk_params['веса']
    risk_params['Weights_for_formula'] = risk_params['веса'] * 2
    
    # Calculate final risk scores per group
    Risk_groups = risk_params['Группа_риска'].unique()
    RISK_values = []
    
    for risk_group in Risk_groups:
        group_data = risk_params[risk_params['Группа_риска'] == risk_group]
        sum_corrected = group_data['Corrected_risks'].sum()
        sum_weights = group_data['Weights_for_formula'].sum()
        risk_score = (sum_corrected / sum_weights) * 10
        RISK_values.append(10 - risk_score)
    
    df_risks = pd.DataFrame({'Группа риска': Risk_groups, 'Риск-скор': RISK_values})
    df_risks['Риск-скор'] = df_risks['Риск-скор'].round(0)
    
    return df_risks

def generate_pdf_report(patient_info, risk_scores, risk_scores_path, risk_params_exp_path, metabolomic_data_with_ratios_path, output_dir):
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
                        
                    risk_scores = calculate_risks(risk_params_path, metabolomic_data_with_ratios)
                    st.write(pd.read_excel(risk_params_exp_path))
                    # Save risk scores as excel in temp_dir
                    risk_scores_path = os.path.join(temp_dir, "risk_scores.xlsx")
                    risk_scores.to_excel(risk_scores_path, index=False)

                    # Generate report
                    report_path = generate_pdf_report(
                        patient_info,
                        risk_scores,
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