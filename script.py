import subprocess
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options

import base64

url = 'http://localhost:8050'

app_command = 'python main.py'

print('Starting...')

proc = subprocess.Popen(app_command, shell=True)

time.sleep(7)

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
        'paperWidth': 8.3
    }

chrome_options = Options()

chrome_options.add_argument("--headless=new") # for Chrome >= 109

driver = webdriver.Chrome(options=chrome_options)

driver.get(url)

time.sleep(5)


pdf_data = driver.execute_cdp_cmd("Page.printToPDF", print_settings)
with open('output.pdf', 'wb') as file:
    file.write(base64.b64decode(pdf_data['data']))

time.sleep(5)

proc.terminate()

proc.kill()

print('Finished')

