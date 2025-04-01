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

def generate_pdf_report(patient_info, file1_path, file2_path, output_dir):
    """Generate PDF report with proper error handling"""
    dash_process = None
    driver = None
    
    try:
        # Clean up any existing Dash instance
        kill_dash_app(8050)
        time.sleep(2)  # Allow port to become available
        
        # Start new Dash process
        dash_command = [
            sys.executable,
            "main.py",
            "--name", patient_info['name'],
            "--age", str(patient_info['age']),
            "--gender", patient_info['gender'],
            "--date", patient_info['date'],
            "--file1", file1_path,
            "--file2", file2_path
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
        
        # Initialize WebDriver and generate PDF
        driver = setup_chrome_driver()
        
        try:
            driver.get("http://localhost:8050")
            time.sleep(5)  # Additional time for dynamic content
            
            # Generate PDF
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
            st.error(f"PDF generation error: {str(e)}")
            logging.error(f"PDF generation failed: {str(e)}")
            return None
            
    except Exception as e:
        st.error(f"Report generation failed: {str(e)}")
        logging.error(f"Report generation error: {str(e)}")
        return None
        
    finally:
        # Cleanup resources in order
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
        
        # Final cleanup
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
        
        st.header("Загрузите исходные файлы")
        file1 = st.file_uploader(
            "Данные об АМИНОКИСЛОТАХ (Excel)",
            type=["xlsx", "xls"],
            key="file1"
        )
        file2 = st.file_uploader(
            "Данные об АЦИЛКАРНИТИНАХ (Excel)",
            type=["xlsx", "xls"],
            key="file2"
        )
        
        submitted = st.form_submit_button("Сформировать отчет", type="primary")
    
    if submitted and validate_inputs(name, file1, file2):
        patient_info = {
            "name": name.strip(),
            "age": age,
            "date": date.strftime("%d.%m.%Y"),
            "gender": gender,
        }
        
        with st.spinner("🔬 Читаем данные и генерируем отчет. Это займет не больше минуты..."):
            with tempfile.TemporaryDirectory() as temp_dir:
                try:
                    file1_path = os.path.join(temp_dir, "metabolites.xlsx")
                    file2_path = os.path.join(temp_dir, "ac_metabolites.xlsx")
                    
                    with open(file1_path, "wb") as f:
                        f.write(file1.getbuffer())
                    with open(file2_path, "wb") as f:
                        f.write(file2.getbuffer())
                    
                    report_path = generate_pdf_report(patient_info, file1_path, file2_path, temp_dir)
                    
                    if report_path and os.path.exists(report_path):
                        st.success("✅ Отчет успешно сформирован!")
                        with open(report_path, "rb") as f:
                            st.download_button(
                                label="📥 Скачать отчет",
                                data=f.read(),
                                file_name=f"Report_{name.replace(' ', '_')}_{date.strftime('%Y%m%d')}.pdf",
                                mime="application/pdf",
                            )
                        
                        with st.expander("📄 Report Preview", expanded=True):
                            base64_pdf = base64.b64encode(open(report_path, "rb").read()).decode('utf-8')
                            st.markdown(
                                f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" style="border:none;"></iframe>',
                                unsafe_allow_html=True
                            )
                    else:
                        st.error("Failed to generate report. Please check the console for errors.")
                        
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()