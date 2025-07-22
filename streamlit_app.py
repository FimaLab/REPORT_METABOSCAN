import streamlit as st
import os
import tempfile
import pandas as pd
from datetime import datetime

from streamlit_utilit import *

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
            "paperWidth": 8.27,      # A4 width in inches (210mm)
            "paperHeight": 11.69,    # A4 height in inches (297mm) 
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
            "paperWidth": 8.27,      # A4 width in inches (210mm)
            "paperHeight": 11.69,    # A4 height in inches (297mm) 
        'scale': 1.0
    }
    
    pdf_data = driver.execute_cdp_cmd("Page.printToPDF", print_settings)
    pdf_path = os.path.join(output_dir, "report.pdf")
    
    with open(pdf_path, "wb") as f:
        f.write(base64.b64decode(pdf_data['data']))
    
    return pdf_path

if __name__ == "__main__":
    main()