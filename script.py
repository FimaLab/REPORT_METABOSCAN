import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import base64
import os
import sys
import requests
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='report_generator.log'
)

def setup_chrome_driver():
    """Configure and return Chrome WebDriver with error handling"""
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize Chrome driver: {str(e)}")
        raise

def verify_dash_app_running(timeout=30):
    """Verify Dash app is running and responding"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get("http://localhost:8050", timeout=5)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            time.sleep(2)
    return False

def generate_pdf_report(patient_info, file1_path, file2_path, output_path='report.pdf'):
    """Generate PDF report with comprehensive error handling"""
    
    # Verify input files exist
    if not all(os.path.exists(f) for f in [file1_path, file2_path]):
        logging.error("Input files not found")
        return False
    
    dash_process = None
    driver = None
    
    try:
        # Build and start Dash app command
        dash_command = [
            sys.executable, 'main.py',
            '--name', patient_info['name'],
            '--age', str(patient_info['age']),
            '--gender', patient_info.get('gender', 'М'),  # Default to 'М' if not provided
            '--date', patient_info['date'],
            '--file1', file1_path,
            '--file2', file2_path
        ]
        
        logging.info("Starting Dash application...")
        dash_process = subprocess.Popen(
            dash_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Verify Dash app started successfully
        if not verify_dash_app_running():
            logging.error("Dash app failed to start")
            return False
        
        # Initialize Chrome driver
        logging.info("Initializing Chrome driver...")
        driver = setup_chrome_driver()
        
        # Configure PDF settings
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
            'scale': 0.8
        }
        
        # Generate PDF
        logging.info("Generating PDF report...")
        driver.get('http://localhost:8050')
        time.sleep(5)  # Wait for page to fully render
        
        # Verify page content loaded
        if "Medical Report" not in driver.title:
            logging.error("Report page didn't load correctly")
            return False
        
        pdf_data = driver.execute_cdp_cmd("Page.printToPDF", print_settings)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'wb') as f:
            f.write(base64.b64decode(pdf_data['data']))
        
        logging.info(f"Successfully generated report at {output_path}")
        return True
        
    except WebDriverException as e:
        logging.error(f"Browser error: {str(e)}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return False
    finally:
        # Cleanup resources
        try:
            if driver:
                driver.quit()
        except Exception as e:
            logging.warning(f"Error closing driver: {str(e)}")
        
        try:
            if dash_process:
                dash_process.terminate()
                dash_process.kill()
        except Exception as e:
            logging.warning(f"Error terminating process: {str(e)}")

if __name__ == "__main__":
    # Example usage with gender parameter
    patient_info = {
        'name': 'Иванов Иван Иванович',
        'age': 47,
        'gender': 'М',  # Now includes gender
        'date': '21.07.2023'
    }
    
    # Generate test report
    success = generate_pdf_report(
        patient_info,
        'Biohaker 1.xlsx',
        'Biohaker_AC 1.xlsx',
        'medical_report.pdf'
    )
    
    if success:
        print("Report generated successfully")
    else:
        print("Failed to generate report - check logs")