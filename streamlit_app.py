import zipfile
import streamlit as st
import os
import tempfile
import pandas as pd
from datetime import datetime
import time
import sys
import subprocess
import base64
import logging
import requests
import shutil

from streamlit_utilit import *

def validate_inputs(name, file1):
    """Validate user inputs before processing"""
    if not name.strip():
        st.error("Please enter a valid patient name")
        return False
    if not file1:
        st.error("Please upload metabolomic data file")
        return False
    return True

def main():
    st.set_page_config(
        page_title="Отчет Metaboscan",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Apply smaller font sizes via custom CSS
    st.markdown("""
        <style>
            body {
                font-size: 14px !important;
            }
            .stTextInput input, .stNumberInput input, .stSelectbox select, .stDateInput input {
                font-size: 14px !important;
            }
            .stDataFrame {
                font-size: 14px !important;
            }
            .stButton button {
                font-size: 14px !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # Path to the reference file
    REF_FILE = "Ref.xlsx"
    
    # Create two columns
    col1, col2 = st.columns([1, 1])
    
    with col1:
        with st.form("report_form"):
            st.write("Информация о пациенте")
            
            cols = st.columns(4)
            with cols[0]:
                name = st.text_input("Полное имя (ФИО)", placeholder="Иванов Иван Иванович")
            with cols[1]:
                age = st.number_input("Возраст", min_value=0, max_value=120, value=47)
            with cols[2]:
                gender = st.selectbox("Пол", ("М", "Ж"), index=0)
            with cols[3]:
                date = st.date_input("Дата отчета", datetime.now(), format="DD.MM.YYYY")
            
            st.write("Загрузите данные")
            
            metabolomic_data = st.file_uploader(
                "Метаболомный профиль пациента (Excel)",
                type=["xlsx", "xls"],
                key="metabolomic_data"
            )
            
            submitted = st.form_submit_button("Сформировать отчет", type="primary")
    
    with col2:
        st.write("Редактирование параметров")
        
        if os.path.exists(REF_FILE):
            try:
                # Initialize session state for both original and edited data
                if 'original_ref' not in st.session_state or 'edited_ref' not in st.session_state:
                    xls = pd.ExcelFile(REF_FILE)
                    st.session_state.original_ref = {
                        sheet_name: xls.parse(sheet_name) 
                        for sheet_name in xls.sheet_names
                    }
                    st.session_state.edited_ref = {
                        sheet_name: df.copy() 
                        for sheet_name, df in st.session_state.original_ref.items()
                    }
                
                # Create tabs for each sheet
                tabs = st.tabs(st.session_state.edited_ref.keys())
                
                for tab, (sheet_name, df) in zip(tabs, st.session_state.edited_ref.items()):
                    with tab:
                        edited_df = st.data_editor(
                            df,
                            num_rows="dynamic",
                            use_container_width=True,
                            height=300,
                            key=f"editor_{sheet_name}"
                        )
                        st.session_state.edited_ref[sheet_name] = edited_df
                
                if st.button("Сбросить изменения", key="reset_button"):
                    st.session_state.edited_ref = {
                        sheet_name: df.copy() 
                        for sheet_name, df in st.session_state.original_ref.items()
                    }
                    st.rerun()
                
            except Exception as e:
                st.error(f"Ошибка при загрузке файла параметров: {str(e)}")
        else:
            st.error(f"Файл параметров не найден: {REF_FILE}")
            st.session_state.edited_ref = None
    
    if submitted:
        if validate_inputs(name, metabolomic_data):
            if not os.path.exists(REF_FILE):
                st.error("Reference file not found. Cannot proceed without Ref.xlsx")
                return
                
            if 'edited_ref' not in st.session_state:
                st.error("Reference data not loaded")
                return

            required_sheets = ['Params_metaboscan', 'Ref_stats']
            for sheet in required_sheets:
                if sheet not in st.session_state.edited_ref:
                    st.error(f"Required sheet '{sheet}' not found in reference file")
                    return

            with st.spinner("🔬 Читаем данные и генерируем отчет. Это займет не больше минуты..."):
                with tempfile.TemporaryDirectory() as temp_dir:
                    try:
                        # Save Params_metaboscan sheet as temporary file
                        risk_params_path = os.path.join(temp_dir, "risk_params.xlsx")
                        st.session_state.edited_ref['Params_metaboscan'].to_excel(risk_params_path, index=False)

                        # Save Ref_stats sheet as temporary file
                        ref_stats_path = os.path.join(temp_dir, "Ref_stats.xlsx")
                        st.session_state.edited_ref['Ref_stats'].to_excel(ref_stats_path, index=False)

                        # Process data
                        metabolomic_data_with_ratios = calculate_metabolite_ratios(metabolomic_data)
                        metabolomic_data_with_ratios_path = os.path.join(temp_dir, "metabolomic_data.xlsx")
                        metabolomic_data_with_ratios.to_excel(metabolomic_data_with_ratios_path, index=False)
                        
                        # Check if input file contains multiple patients (more than 1 row after header)
                        df_metabolomic = pd.read_excel(metabolomic_data)
                        multiple_patients = len(df_metabolomic) > 1
                        
                        if multiple_patients:
                            st.info("Обнаружены данные для нескольких пациентов. Показаны результаты для всех пациентов.")
                            st.warning("Для генерации индивидуальных отчетов, пожалуйста, загружайте данные по одному пациенту за раз.")
                            
                            # Get patient identifiers and groups from file
                            patient_ids = df_metabolomic.get('Код', [f"Пациент {i+1}" for i in range(len(df_metabolomic))])
                            patient_groups = df_metabolomic.get('Группа', ["-" for _ in range(len(df_metabolomic))])
                            
                            # Create tabs for each patient
                            tabs = st.tabs([f"Пациент {i+1}" for i in range(len(patient_ids))])
                            
                            for idx, tab in enumerate(tabs):
                                with tab:
                                    with st.spinner(f"Расчет показателей для пациента {idx+1}/{len(patient_ids)}..."):
                                        # Get individual patient data
                                        patient_data = metabolomic_data_with_ratios.iloc[[idx]]
                                        patient_data_path = os.path.join(temp_dir, f"patient_data_{idx}.xlsx")
                                        patient_data.to_excel(patient_data_path, index=False)
                                        
                                        # Calculate risk parameters for this patient only
                                        patient_risk_params_exp = prepare_final_dataframe(risk_params_path, patient_data_path)
                                        
                                        # Calculate risk scores for this patient only
                                        patient_risk_scores = calculate_risks(patient_risk_params_exp, patient_data)
                                        
                                        # Display results
                                        col1, col2 = st.columns([1, 3])
                                        
                                        with col1:
                                            st.markdown(f"**Код пациента:** {patient_ids[idx]}")
                                            st.markdown(f"**Группа:** {patient_groups[idx]}")
                                            st.markdown("---")
                                            
                                        
                                        with col2:
                                            # Display individual risk scores
                                            st.markdown("**Оценка рисков по заболеваниям:**")
                                            
                                            st.dataframe( 
                                                patient_risk_scores,
                                                use_container_width=True
                                            )
                                            st.dataframe(
                                                patient_risk_params_exp,
                                                use_container_width=True
                                            )
                        else:  # Single patient case (original behavior)
                            patient_info = {
                                "name": name.strip(),
                                "age": age,
                                "date": date.strftime("%d.%m.%Y"),
                                "gender": gender,
                            }
                            
                            risk_params_exp = prepare_final_dataframe(risk_params_path, metabolomic_data_with_ratios_path)
                            risk_params_exp_path = os.path.join(temp_dir, "risk_exp_params.xlsx")
                            risk_params_exp.to_excel(risk_params_exp_path, index=False)
                                
                            risk_scores = calculate_risks(risk_params_exp, metabolomic_data_with_ratios)
                            risk_scores_path = os.path.join(temp_dir, "risk_scores.xlsx")
                            risk_scores.to_excel(risk_scores_path, index=False)
                            
                            metrics_path = os.path.join(temp_dir, "metrics.xlsx")
                            st.session_state.edited_ref['metrics_ml_models'].to_excel(metrics_path, index=False)
                            st.info("✅ Предварительный просмотр рассчитанных значений!")
                            cols = st.columns(2)
                            with cols[0]:
                                st.dataframe(risk_scores)
                            with cols[1]:
                                st.dataframe(risk_params_exp)
                            
                            # Generate report
                            report_path = generate_pdf_report(
                                patient_info,
                                risk_scores_path,
                                risk_params_exp_path,
                                metabolomic_data_with_ratios_path,
                                ref_stats_path,
                                metrics_path,
                                temp_dir
                            )
                            
                            if report_path:
                                st.success("✅ Отчет успешно сформирован!")
                                with open(report_path, "rb") as f:
                                    st.download_button(
                                        label="📥 Скачать отчет",
                                        data=f.read(),
                                        file_name=f"Report_{name.replace(' ', '_')}_{date.strftime('%Y%m%d')}.pdf",
                                        mime="application/pdf",
                                    )
                            else:
                                st.error("Ошибка при генерации отчета")
                                
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
                        logging.error(f"Error in report generation: {str(e)}")

def generate_pdf_report(patient_info, risk_scores_path, risk_params_exp_path, 
                       metabolomic_data_with_ratios_path, ref_stats_path,metrics_path, output_dir):
    """Generate PDF report with proper error handling"""
    dash_process = None
    driver = None
    
    try:
        # Clean up any existing Dash instance
        kill_dash_app(8050)
        time.sleep(2)
        
        # Start Dash process with required data
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
            "--ref_stats", ref_stats_path,  # Add ref_stats parameter
            "--metrics", metrics_path,
        ]
        
        dash_process = subprocess.Popen(
            dash_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if not wait_for_dash_app():
            raise Exception("Dash app failed to start")
        
        # Generate PDF
        driver = setup_chrome_driver()
        driver.get("http://localhost:8050")
        time.sleep(5)
        
        pdf_path = os.path.join(output_dir, "report.pdf")
        print_settings = {
            "printBackground": True,
            "paperWidth": 8.27,
            "paperHeight": 11.69,
            "scale": 0.89,
            "margin": {
                "top": "0.0in",
                "bottom": "0.0in",
                "left": "0.25in",
                "right": "0.25in"
            }
        }
        
        pdf_data = driver.execute_cdp_cmd("Page.printToPDF", print_settings)
        with open(pdf_path, "wb") as f:
            f.write(base64.b64decode(pdf_data['data']))
        
        return pdf_path
        
    except Exception as e:
        st.error(f"Report generation failed: {e}")
        logging.error(f"Report generation error: {e}")
        return None
        
    finally:
        if driver:
            driver.quit()
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

if __name__ == "__main__":
    main()